#!/bin/bash

echo "Downloading Kokoro model..."

if [ ! -f kokoro-v1.0.onnx ]; then
  wget -O kokoro-v1.0.onnx \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
fi

if [ ! -f voices-v1.0.bin ]; then
  wget -O voices-v1.0.bin \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
fi

echo "Model ready"

uvicorn server:app --host 0.0.0.0 --port $PORT
