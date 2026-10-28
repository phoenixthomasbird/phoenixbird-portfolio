# Research agent

A desktop app that answers a question by running a Claude tool-use loop: the model decides when to search the web and which pages to read, and the app shows each step as it happens.

- `agent.py`: the loop. Claude gets two tools, calls them as it sees fit, and stops when it has an answer. A hard cap of 10 iterations means it can never loop forever.
- `tools.py`: `search_web` (DuckDuckGo's instant-answer API, no key needed) and `read_url` (fetches a page as plain text).
- `ui.py`: a PyQt5 window. The agent runs on a worker thread and reports progress through Qt signals, so the window never freezes.
- `prompts.py`: the system prompt. The original held a personal profile; this public copy has a neutral research prompt.

## Run it

```bash
pip install anthropic python-dotenv PyQt5
echo "ANTHROPIC_API_KEY=..." > .env   # never commit this file
python ui.py
```

## Known gap

`read_url` opens any URL the model chooses, including `file://` paths and local network addresses. A web page could use prompt injection to steer the agent there and pass local files to the model. The fix is to allow only `http`/`https` and refuse private and loopback addresses. Run it only on your own machine until that's in.

## How it was built

Written by Claude from my direction; I designed what it should do and tested it. For publication I fixed a missing parenthesis on the last line of `ui.py` and replaced the system prompt.
