from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
from kokoro_onnx import Kokoro
import io
import soundfile as sf
import traceback

app = FastAPI()

print("Loading Kokoro model...")

# Force CPU provider to avoid GPU detection delay
tts = Kokoro(
    "kokoro-v1.0.onnx",
    "voices-v1.0.bin",
    providers=["CPUExecutionProvider"]
)

print("Model ready")
print("AVAILABLE VOICES:", list(tts.voices.keys()))

# ---------------------------------------------------
# Warmup model to avoid first-request latency
# ---------------------------------------------------
print("Warming up model...")

try:
    tts.create("hello world", voice="af_bella")
    print("Warmup complete")
except Exception as e:
    print("Warmup failed:", e)

# ---------------------------------------------------
# Health check
# ---------------------------------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# ---------------------------------------------------
# TTS Endpoint
# ---------------------------------------------------
@app.post("/tts")
async def generate(request: Request):

    try:
        data = await request.json()

        text = data.get("text")
        voice = data.get("voice", "af_bella")

        if not text:
            return JSONResponse(
                {"error": "text is required"},
                status_code=400
            )

        # limit text length (avoid long inference)
        if len(text) > 300:
            text = text[:300]

        if voice not in tts.voices:
            return JSONResponse(
                {
                    "error": "voice not found",
                    "available": list(tts.voices.keys())
                },
                status_code=400
            )

        print(f"TTS request | voice={voice} | text_length={len(text)}")

        audio, sr = tts.create(text, voice=voice)

        buf = io.BytesIO()
        sf.write(buf, audio, sr, format="WAV")

        print("TTS generation success")

        return Response(
            buf.getvalue(),
            media_type="audio/wav"
        )

    except Exception as e:

        print("TTS ERROR:")
        traceback.print_exc()

        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )
