# Hebrew tutor

A small web app for practising spoken Hebrew: talk to it, read the reply, hear it spoken back.

- `app.py`: a FastAPI server with three endpoints. `/chat` sends the conversation to Claude with a tutoring system prompt; `/transcribe` turns recorded speech into text with Whisper; `/speak` turns a reply into Hebrew audio with gTTS.
- `templates/index.html`: the page you talk to.

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env    # add your Anthropic API key; never commit .env
uvicorn app:app --reload
```

Browsers only allow microphone access over HTTPS or on localhost. To use it from another device, generate your own self-signed certificate; none is included here.

## Known gaps

There's no login, no rate limit and no upload size limit. Anyone who can reach the server can run up your API bill. Keep it on your own machine or home network.

## How it was built

Written by Claude from my direction; I designed what it should do and tested it.
