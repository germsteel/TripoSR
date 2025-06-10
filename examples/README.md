# 3D模型优化工具使用说明

本工具提供了一套完整的3D模型优化功能，可以根据不同的目标平台和质量要求优化模型的网格和纹理。

## 安装依赖

确保已安装所有必要的依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法
```bash
python optimize_mesh.py input_model.obj --platform unity --quality balanced
```

### 参数说明

- `input_path`: 输入模型文件路径(.obj或.glb)
- `--platform`: 目标平台，可选值：
  - unity (默认)
  - blender
  - web
  - mobile
- `--quality`: 质量等级，可选值：
  - high (高质量)
  - balanced (平衡，默认)
  - performance (性能优先)
- `--output_dir`: 输出目录，默认为 'output'

### 示例命令

1. Unity平台高质量优化：
```bash
python optimize_mesh.py input_model.obj --platform unity --quality high
```

2. 移动端性能优先优化：
```bash
python optimize_mesh.py input_model.obj --platform mobile --quality performance
```

3. Web平台平衡质量：
```bash
python optimize_mesh.py input_model.obj --platform web --quality balanced
```

## 优化参数参考

### Unity平台
- 高质量：15000面，4096纹理分辨率
- 平衡：8000面，2048纹理分辨率
- 性能：3000面，1024纹理分辨率

### Blender平台
- 高质量：20000面，4096纹理分辨率
- 平衡：10000面，2048纹理分辨率
- 性能：5000面，1024纹理分辨率

### Web平台
- 高质量：10000面，2048纹理分辨率
- 平衡：5000面，1024纹理分辨率
- 性能：2000面，512纹理分辨率

### 移动平台
- 高质量：5000面，1024纹理分辨率
- 平衡：3000面，512纹理分辨率
- 性能：1500面，256纹理分辨率

## 注意事项

1. 内存使用
   - 对于大型模型，建议使用性能模式先进行测试
   - 如果出现内存不足，可以尝试降低质量等级

2. UV优化
   - 优化过程会自动处理UV展开
   - 纹理填充会根据分辨率自动调整

3. 输出文件
   - 输出文件名格式：{原文件名}_{平台}_{质量}.obj
   - 同时会保存优化参数信息

## 开发扩展

如果需要自定义优化参数，可以修改 `MeshOptimizer` 类中的配置：

```python
from tsr.utils.mesh_optimizer import MeshOptimizer

optimizer = MeshOptimizer()
mesh, config = optimizer.optimize_for_platform(
    input_mesh,
    platform='custom',
    quality_level='custom'
)
```

可以通过继承 `MeshOptimizer` 类来添加自定义优化策略：

```python
class CustomOptimizer(MeshOptimizer):
    def __init__(self):
        super().__init__()
        # 添加自定义配置