#!/bin/bash

echo "Preparing Kokoro model..."

# download voices
if [ ! -f voices-v1.0.bin ]; then
  echo "Downloading voices..."
  wget -q -O voices-v1.0.bin \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
fi

# download model
if [ ! -f kokoro-v1.0.onnx ]; then
  echo "Downloading Kokoro model..."
  wget -q -O kokoro-v1.0.onnx \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
fi

echo "Model ready"

export OMP_NUM_THREADS=1
export ORT_DISABLE_MEMORY_ARENA=1

uvicorn server:app --host 0.0.0.0 --port $PORT