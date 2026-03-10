from onnxruntime.quantization import quantize_dynamic, QuantType

input_model = "kokoro-v1.0.onnx"
output_model = "kokoro-int8.onnx"

quantize_dynamic(
    input_model,
    output_model,
    weight_type=QuantType.QInt8
)

print("Quantized model saved as:", output_model)