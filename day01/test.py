import tensorrt as trt
import pycuda.driver as cuda  # 如果没有请 pip install pycuda
import pycuda.autoinit

logger = trt.Logger(trt.Logger.INFO)

# 测试是否能创建推理运行时
runtime = trt.Runtime(logger)
if runtime:
    print("🚀 TensorRT 运行时初始化成功！")

# 检查 GPU 是否被识别
print(f"当前使用的显卡: {cuda.Device(0).name()}")