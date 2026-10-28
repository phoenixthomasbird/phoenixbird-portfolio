# Agent SDK experiment

A first run of the Claude Agent SDK. `utils.py` contains small functions with crash bugs; `agent.py` asks Claude to find and fix them, allowing only the Read, Edit and Glob tools and auto-approving edits.

What I took from it: the tool allowlist and the permission mode are the real safety controls. "Accept edits" is fine on a throwaway file and not something I'd point at a real project without review.

## Run it

```bash
pip install claude-agent-sdk
export ANTHROPIC_API_KEY=...   # or a .env file you never commit
python agent.py
```

## How it was built

Written with Claude while learning the SDK; I ran it and checked the edits it made.
