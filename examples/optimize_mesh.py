import os
import argparse
import trimesh
from tsr.utils.mesh_optimizer import MeshOptimizer

def main():
    parser = argparse.ArgumentParser(description='优化3D模型网格和纹理')
    parser.add_argument('input_path', type=str, help='输入模型文件路径(.obj或.glb)')
    parser.add_argument('--platform', type=str, default='unity', 
                      choices=['unity', 'blender', 'web', 'mobile'],
                      help='目标平台')
    parser.add_argument('--quality', type=str, default='balanced',
                      choices=['high', 'balanced', 'performance'],
                      help='质量等级')
    parser.add_argument('--output_dir', type=str, default='output',
                      help='输出目录')
    args = parser.parse_args()

    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)

    try:
        # 加载模型
        print(f"Loading mesh from {args.input_path}")
        mesh = trimesh.load(args.input_path)

        # 创建优化器
        optimizer = MeshOptimizer()

        # 优化网格
        print(f"Optimizing mesh for {args.platform} platform with {args.quality} quality")
        optimized_mesh, config = optimizer.optimize_for_platform(
            mesh,
            platform=args.platform,
            quality_level=args.quality
        )

        # 生成输出文件名
        base_name = os.path.splitext(os.path.basename(args.input_path))[0]
        output_path = os.path.join(
            args.output_dir,
            f"{base_name}_{args.platform}_{args.quality}.obj"
        )

        # 保存优化后的模型
        print(f"Saving optimized mesh to {output_path}")
        optimized_mesh.export(output_path)

        # 打印优化结果
        print("\nOptimization Results:")
        print(f"Original faces: {len(mesh.faces)}")
        print(f"Optimized faces: {len(optimized_mesh.faces)}")
        print(f"Target faces: {config['target_faces']}")
        print(f"Texture resolution: {config['texture_resolution']}")

        # 打印内存使用情况
        memory_stats = optimizer.monitor_memory()
        if "error" not in memory_stats:
            print(f"\nMemory Usage:")
            print(f"Current: {memory_stats['current_memory_mb']:.2f} MB")
            print(f"Peak: {memory_stats['peak_memory_mb']:.2f} MB")

        print("\nOptimization completed successfully!")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())