"""Run the Week 2 workbook on Windows and save the local model's original replies."""

import hashlib
import http.client
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from contextlib import closing
from datetime import datetime
from zipfile import ZipFile

LAB = Path(__file__).resolve().parents[1] / "week2"
sys.path.insert(0, str(LAB))
from helper import MODEL, ask_ollama, build_messages

VERSION = "0.40.17"
ARCHIVE = "ollama-windows-amd64.zip"
URL = f"https://github.com/ollama/ollama/releases/download/v{VERSION}/{ARCHIVE}"
SHA256 = "3dd80f6e3a9699f2eadf4ac418f00529cee594df9557541806eda1f1f3f5588a"


def installed_models():
    with closing(http.client.HTTPConnection("127.0.0.1", 11434, timeout=4)) as conn:
        conn.request("GET", "/api/tags")
        reply = conn.getresponse()
        if reply.status != 200:
            raise RuntimeError(f"The local model service returned HTTP {reply.status}.")
        return {item["name"]: item for item in json.load(reply)["models"]}


def find_cli():
    standard = Path(os.environ["LOCALAPPDATA"]) / "Programs" / "Ollama" / "ollama.exe"
    existing = shutil.which("ollama.exe")
    if existing or standard.is_file():
        return Path(existing) if existing else standard

    cache = Path(os.environ["LOCALAPPDATA"]) / "IIT-Week2"
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / f"ollama-{VERSION}-amd64"
    if (target / "ollama.exe").is_file():
        return target / "ollama.exe"

    print("Downloading the official Windows x64 Ollama CLI (1.62 GB).", flush=True)
    with tempfile.TemporaryDirectory(dir=cache) as temp:
        archive = Path(temp) / ARCHIVE
        subprocess.run(["curl.exe", "--fail", "--location", "--retry", "2",
                        "--output", str(archive), URL], check=True)
        with archive.open("rb") as stream:
            digest = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        if digest.hexdigest() != SHA256:
            raise RuntimeError("The Ollama download failed the release checksum.")
        extracted = Path(temp) / "extracted"
        with ZipFile(archive) as bundle:
            bundle.extractall(extracted)
        if not (extracted / "ollama.exe").is_file():
            raise RuntimeError("ollama.exe is missing from the extracted archive.")
        try:
            extracted.rename(target)
        except OSError:
            if not (target / "ollama.exe").is_file():
                raise
    return target / "ollama.exe"


def ensure_model():
    if MODEL in installed_models():
        return
    print(f"Pulling {MODEL} to this computer (about 1.9 GB).", flush=True)
    with closing(http.client.HTTPConnection("127.0.0.1", 11434, timeout=300)) as conn:
        conn.request("POST", "/api/pull", json.dumps({"model": MODEL, "stream": True}),
                     {"Content-Type": "application/json"})
        reply = conn.getresponse()
        if reply.status != 200:
            raise RuntimeError(f"Model download returned HTTP {reply.status}.")
        previous = ""
        for line in reply:
            event = json.loads(line)
            if event.get("error"):
                raise RuntimeError(event["error"])
            message = event.get("status", "")
            if event.get("total") and event.get("completed") is not None:
                percent = 100 * event["completed"] // event["total"]
                message += f" {percent // 10 * 10}%"
            if message != previous:
                print(message, flush=True)
                previous = message
    if MODEL not in installed_models():
        raise RuntimeError(f"The local model list does not contain {MODEL}.")


def run_experiment():
    ensure_model()
    record = installed_models()[MODEL]
    folder = LAB / "results"
    folder.mkdir(exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix=datetime.now().strftime("%Y%m%d-%H%M%S-"), dir=folder))
    (run / "model.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"Saving this run to {run}", flush=True)
    logs = (LAB / "logs.txt").read_text(encoding="utf-8-sig")
    notes = (LAB / "notes.txt").read_text(encoding="utf-8-sig")
    question = "What does a compiler do, in one sentence?"
    cases = [
        ("part-a", [{"role": "user", "content": question}]),
        ("part-b", build_messages("baseline", logs)),
        ("part-d", build_messages("rag", logs, notes)),
        ("defended", build_messages("defended", logs, notes)),
    ]
    for name, messages in cases:
        print(f"\n{name} | local model {MODEL}", flush=True)
        reply = ask_ollama(messages)
        if not reply:
            raise RuntimeError(f"The local model returned no text for {name}.")
        (run / f"{name}.txt").write_text(reply + "\n", encoding="utf-8")
        print(reply, flush=True)
    print(f"\nPart B is ready for a screenshot. Original replies are in {run}.\n", flush=True)
    print(f"Part B | local model {MODEL}\n" + (run / "part-b.txt").read_text(encoding="utf-8"))


def main():
    if sys.platform != "win32":
        raise RuntimeError("This launcher is for Windows. Run helper.py directly on other systems.")
    server = None
    try:
        try:
            installed_models()
        except OSError:
            cli = find_cli()
            env = dict(os.environ, OLLAMA_HOST="127.0.0.1:11434")
            server = subprocess.Popen([str(cli), "serve"], env=env,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
            for _ in range(45):
                try:
                    installed_models()
                    break
                except OSError:
                    if server.poll() is not None:
                        raise RuntimeError("The local Ollama process exited during startup.")
                    time.sleep(1)
            else:
                raise RuntimeError("The local Ollama server did not start within 45 seconds.")
        run_experiment()
    finally:
        if server is not None and server.poll() is None:
            server.terminate()
            server.wait(timeout=20)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, KeyError, http.client.HTTPException, subprocess.SubprocessError) as error:
        print(f"\nWeek 2 stopped: {error}", file=sys.stderr)
        sys.exit(1)
