from fastapi import FastAPI
from kokoro_onnx import Kokoro
from fastapi.responses import Response
import io
import soundfile as sf

app = FastAPI()

tts = Kokoro("kokoro-v1.0.onnx")

@app.post("/tts")
async def generate(data: dict):

    text = data["text"]

    audio, sr = tts.create(text)

    buf = io.BytesIO()
    sf.write(buf, audio, sr, format="WAV")

    return Response(buf.getvalue(), media_type="audio/wav")