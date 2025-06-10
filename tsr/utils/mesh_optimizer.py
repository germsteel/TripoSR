import numpy as np
import torch
import trimesh
import xatlas
from typing import Dict, Optional, Tuple

class MeshOptimizer:
    """网格模型优化工具类"""
    
    def __init__(self):
        self.timer = None
        self.memory_stats = {}
    
    @staticmethod
    def simplify_mesh(mesh: trimesh.Trimesh, 
                     target_faces: int = 5000,
                     preserve_uv: bool = True) -> trimesh.Trimesh:
        """简化网格模型

        Args:
            mesh: 输入的网格模型
            target_faces: 目标面数
            preserve_uv: 是否保留UV坐标
        
        Returns:
            简化后的网格模型
        """
        # 保存原始UV数据
        original_visual = mesh.visual.copy() if preserve_uv else None
        
        # 网格简化
        simplified = mesh.simplify_quadratic_decimation(target_faces)
        
        # 清理网格
        simplified.remove_duplicate_vertices()
        simplified.remove_unreferenced_vertices()
        simplified.remove_degenerate_faces()
        
        # 如果需要，重新映射UV
        if preserve_uv and original_visual is not None:
            simplified.visual = original_visual
            
        return simplified

    @staticmethod
    def optimize_uv_layout(mesh: trimesh.Trimesh,
                          texture_resolution: int = 2048,
                          padding: int = 2,
                          max_iterations: int = 4) -> Dict:
        """优化UV布局

        Args:
            mesh: 输入的网格模型
            texture_resolution: 纹理分辨率
            padding: 填充像素
            max_iterations: 最大迭代次数

        Returns:
            包含优化后UV信息的字典
        """
        atlas = xatlas.Atlas()
        atlas.add_mesh(mesh.vertices, mesh.faces)
        
        options = xatlas.PackOptions()
        options.resolution = texture_resolution
        options.padding = padding
        options.bilinear = True
        options.max_iterations = max_iterations
        
        atlas.generate(pack_options=options)
        vmapping, indices, uvs = atlas[0]
        
        return {
            "vmapping": vmapping,
            "indices": indices,
            "uvs": uvs
        }

    def optimize_for_platform(self, 
                            mesh: trimesh.Trimesh,
                            platform: str = "unity",
                            quality_level: str = "balanced") -> Tuple[trimesh.Trimesh, Dict]:
        """针对特定平台优化网格

        Args:
            mesh: 输入的网格模型
            platform: 目标平台 ("unity", "blender", "web", "mobile")
            quality_level: 质量等级 ("high", "balanced", "performance")

        Returns:
            优化后的网格模型和配置参数
        """
        # 平台特定的参数配置
        configs = {
            "unity": {
                "high": {"faces": 15000, "texture": 4096},
                "balanced": {"faces": 8000, "texture": 2048},
                "performance": {"faces": 3000, "texture": 1024}
            },
            "blender": {
                "high": {"faces": 20000, "texture": 4096},
                "balanced": {"faces": 10000, "texture": 2048},
                "performance": {"faces": 5000, "texture": 1024}
            },
            "web": {
                "high": {"faces": 10000, "texture": 2048},
                "balanced": {"faces": 5000, "texture": 1024},
                "performance": {"faces": 2000, "texture": 512}
            },
            "mobile": {
                "high": {"faces": 5000, "texture": 1024},
                "balanced": {"faces": 3000, "texture": 512},
                "performance": {"faces": 1500, "texture": 256}
            }
        }
        
        # 获取配置参数
        config = configs.get(platform, configs["unity"]).get(quality_level, configs["unity"]["balanced"])
        
        # 简化网格
        optimized_mesh = self.simplify_mesh(
            mesh, 
            target_faces=config["faces"],
            preserve_uv=True
        )
        
        # 优化UV
        uv_data = self.optimize_uv_layout(
            optimized_mesh,
            texture_resolution=config["texture"]
        )
        
        return optimized_mesh, {
            "platform": platform,
            "quality_level": quality_level,
            "target_faces": config["faces"],
            "texture_resolution": config["texture"],
            "uv_data": uv_data
        }

    def monitor_memory(self) -> Dict:
        """监控GPU内存使用"""
        if torch.cuda.is_available():
            current_memory = torch.cuda.memory_allocated() / 1024**2  # MB
            peak_memory = torch.cuda.max_memory_allocated() / 1024**2  # MB
            return {
                "current_memory_mb": current_memory,
                "peak_memory_mb": peak_memory
            }
        return {"error": "CUDA not available"}