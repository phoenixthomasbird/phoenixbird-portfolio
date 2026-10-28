# Projects

Code I've written or directed, one folder per project. Larger projects were written by Claude from my direction and tested by me; the learning folder is code I wrote myself while learning Python. Each README says which.

| Project | What it is | Built with |
|---|---|---|
| [Research agent](projects/research-agent/) | Desktop app running a Claude tool-use loop: web search, page reading, an iteration cap, progress shown live | Python, Claude API, PyQt5 |
| [Hebrew tutor](projects/hebrew-tutor/) | Spoken Hebrew practice: speech to text, a Claude tutor, Hebrew text to speech | Python, FastAPI, Claude API, Whisper, gTTS |
| [Agent SDK experiment](projects/agent-sdk-experiment/) | Claude Agent SDK fixing planted bugs under a restricted tool allowlist | Python, Claude Agent SDK |
| [Learning Python](projects/learning/) | 35+ small practice programs: automation, PyQt windows, documents | Python |

No API keys are in this repo. Projects that call an API read the key from a `.env` file, which is git-ignored.
