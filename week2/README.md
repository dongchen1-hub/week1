# Week 2 lab portfolio

The log experiments used one local Ollama model, `qwen2.5:3b`. Part B supplied the five events in `logs.txt`. Part D added the two lines from `notes.txt`.

## How the notes changed the summary

Without the notes, the model listed all five events, including the successful login, and described the database timeout as a problem. With the notes, it treated the 08:05 timeout as expected during the nightly restart and singled out the report worker's memory leak under ticket IT-142.

## Prompt-injection test and defence

The workbook's extra line was an 08:09 INFO entry. The helper's filter removed it before inference and kept both errors and the retry warning. In a separate control with a harmless green-dashboard message at 08:09, both protected runs still reported the 08:07 memory error, although their wording differed. The unfiltered model's reaction to the workbook's original instruction was not measured.

## Critique

The baseline listed the successful 08:02 login among the problems, even though the log marks it as INFO. The summary with notes said ticket IT-142 was “being actively addressed.” The only status in the notes is “open,” so there is no evidence that someone had started a fix. Likewise, the worker's memory error is recorded at 08:07, but confirming the known leak caused this particular error would need more evidence.

## Evidence and reproduction

- `part-b.jpg` shows the original output of `python helper.py` on the local machine. `repository.jpg` shows the public course repository.
- `model-output.txt` contains the local model's original replies, including its one-sentence answer about compilers. The headings identify the inputs for each run.
- Start Ollama, then run the following commands in the folder that contains `helper.py`.

```powershell
ollama pull qwen2.5:3b
python -m pip install openai
python helper.py
python helper.py rag
python helper.py defended
```

The model used temperature 0 and seed 42. Its local API is at `127.0.0.1:11434`.

## AI assistance

ChatGPT (Codex) helped write and test the helper, run the local model, capture its output and draft the comparisons above. The sample logs and background notes came from the Week 2 Lab Workbook.
