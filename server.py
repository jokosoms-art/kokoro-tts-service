from fastapi import FastAPI, Request
from kokoro_onnx import Kokoro
from fastapi.responses import Response
import io
import soundfile as sf

app = FastAPI()

tts = Kokoro(
    "kokoro-v1.0.onnx",
    "voices-v1.0.bin"
)

print("AVAILABLE VOICES:", tts.voices)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/tts")
async def generate(request: Request):

    data = await request.json()

    text = data.get("text", "")
    voice = data.get("voice", "af")

    if voice not in tts.voices:
        voice = tts.voices[0]

    audio, sr = tts.create(text, voice=voice)

    buf = io.BytesIO()
    sf.write(buf, audio, sr, format="WAV")

    return Response(buf.getvalue(), media_type="audio/wav")
