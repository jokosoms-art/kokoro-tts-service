from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
from kokoro_onnx import Kokoro
import io
import soundfile as sf
import traceback
import os

# ==========================================
# MEMORY OPTIMIZATION (important for Render)
# ==========================================

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OMP_WAIT_POLICY"] = "PASSIVE"
os.environ["ORT_DISABLE_MEMORY_ARENA"] = "1"

app = FastAPI()

print("Loading Kokoro model...")

# ==========================================
# LOAD QUANTIZED MODEL (IMPORTANT)
# ==========================================

tts = Kokoro(
    "kokoro-int8.onnx",
    "voices-v1.0.bin"
)

print("Model ready")
print("AVAILABLE VOICES:", list(tts.voices.keys()))

# ==========================================
# WARMUP
# ==========================================

print("Warming up Kokoro...")

try:
    tts.create("hello world", voice="af_bella")
    print("Warmup complete")
except Exception as e:
    print("Warmup error:", e)

# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def health():
    return {"status": "ok"}

# ==========================================
# TTS ENDPOINT
# ==========================================

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

        if voice not in tts.voices:
            return JSONResponse(
                {
                    "error": "voice not found",
                    "available": list(tts.voices.keys())
                },
                status_code=400
            )

        if len(text) > 300:
            text = text[:300]

        print(f"TTS request | voice={voice} | length={len(text)}")

        audio, sr = tts.create(text, voice=voice)

        buf = io.BytesIO()
        sf.write(buf, audio, sr, format="WAV")

        print("TTS success")

        return Response(
            buf.getvalue(),
            media_type="audio/wav"
        )

    except Exception as e:

        print("TTS ERROR")
        traceback.print_exc()

        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )