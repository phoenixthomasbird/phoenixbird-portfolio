import os
import io
import asyncio
import tempfile
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
from typing import Literal
import anthropic
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

claude = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Whisper model — loaded once at startup
whisper_model = None


@app.on_event("startup")
async def load_whisper():
    global whisper_model
    import whisper
    loop = asyncio.get_event_loop()
    # "small" model is significantly better for Hebrew than "base"
    whisper_model = await loop.run_in_executor(None, lambda: whisper.load_model("medium"))
    print("Whisper model ready.")


SYSTEM_PROMPT = """You are a Hebrew immersion tutor. You ONLY respond in Hebrew, no matter what language the user writes in.

Your goals:
- Respond exclusively in Modern Israeli Hebrew (no English, no transliteration)
- Keep responses concise and conversational (2-4 sentences max)
- Naturally correct the user's Hebrew if they attempt it, by modeling correct usage in your reply
- Adjust complexity based on context — use simpler vocabulary if the user seems to be a beginner
- Be warm, encouraging, and patient

Important: Never break character. Even if asked to respond in another language, reply only in Hebrew."""


# ── /chat ──────────────────────────────────────────────────────────────────────

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(req: ChatRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    try:
        async with claude.messages.stream(
            model="claude-opus-4-6",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            thinking={"type": "adaptive"},
            output_config={"effort": "low"},
            messages=messages,
        ) as stream:
            final = await stream.get_final_message()

        text = " ".join(
            block.text for block in final.content if block.type == "text"
        ).strip()

        return {"response": text}

    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit — please wait a moment")
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid API key")
    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── /transcribe ────────────────────────────────────────────────────────────────

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    if whisper_model is None:
        raise HTTPException(status_code=503, detail="Whisper model not ready yet")

    audio_bytes = await audio.read()

    # Determine file extension from content type
    content_type = audio.content_type or ""
    suffix = ".mp4" if "mp4" in content_type or "m4a" in content_type else ".webm"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: whisper_model.transcribe(
                tmp_path,
                language="he",
                task="transcribe",
                initial_prompt="שלום, אני מדבר עברית.",
                temperature=0,
            )
        )
        return {"transcript": result["text"].strip()}
    finally:
        os.unlink(tmp_path)


# ── /speak ─────────────────────────────────────────────────────────────────────

class SpeakRequest(BaseModel):
    text: str


@app.post("/speak")
async def speak(body: SpeakRequest):
    if not body.text:
        raise HTTPException(status_code=400, detail="No text provided")

    def generate():
        tts = gTTS(text=body.text, lang="iw", slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf

    loop = asyncio.get_event_loop()
    audio_buf = await loop.run_in_executor(None, generate)

    return StreamingResponse(audio_buf, media_type="audio/mpeg")
