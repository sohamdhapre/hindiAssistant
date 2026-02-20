from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic(
    "hi_IN-rohan-medium.onnx",
    "hi_IN-rohan-medium-int8.onnx",
    weight_type=QuantType.QInt8
)
