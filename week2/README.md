# IIT Week 2 — Local log summariser

`logs.txt` contains the five fictional server events from the Week 2 Lab Workbook. `notes.txt` contains the two facts about the nightly database restart and the report worker. `helper.py` uses `qwen2.5:3b` on this computer.

## Run the experiment

Start Ollama on Windows, then run these commands in the directory containing `helper.py`.

```powershell
ollama pull qwen2.5:3b
python -m pip install openai
python helper.py
python helper.py rag
python helper.py defended
```

The first run sends only `logs.txt`. The second includes `notes.txt`. The third labels the input as data and passes only timestamped warnings and errors to the model. The program uses the OpenAI Python package when installed. It can also reach the same local Ollama endpoint using Python’s standard library.

## Check against the source

At 08:05 the database timed out after 30 seconds. At 08:06 the system started a retry. The log does not say whether the retry succeeded. At 08:07 the report worker ran out of memory. The notes say a brief timeout is expected during the scheduled restart and that the worker has a known memory leak tracked under IT-142.

## Defence check

Adding an 08:09 informational event with a green dashboard label left the defended model input identical to the original. Both errors and the retry warning were still present. This checks the input filter. It does not measure how a model would respond to an instruction in an unfiltered log or in a warning or error.

## AI assistance

ChatGPT (Codex) helped write the Python program and these notes and tested the construction of the three prompts. The log and background facts come from the Week 2 Lab Workbook.
