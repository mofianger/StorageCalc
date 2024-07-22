import os
import argparse
from tqdm import tqdm

def get_size(size_in_bytes):
    """将字节转换为MB，并返回格式化的字符串"""
    if size_in_bytes >= 1024**3:
        return f"{size_in_bytes / (1024 ** 3):.2f} GB"
    else:
        return f"{size_in_bytes / (1024 ** 2):.2f} MB"

def transverse(root_dir="D:/", saving = False, output_file="fixed_size_report.txt"):
    # 获取D盘根目录下所有文件夹的列表
    all_files = os.listdir(root_dir)
    files = [f for f in all_files if not os.path.isdir(os.path.join(root_dir, f))]
    folders = [f for f in all_files if os.path.isdir(os.path.join(root_dir, f))]

    # 存储每个文件夹的名称和大小
    file_sizes = [(f, os.path.getsize(os.path.join(root_dir, f))) for f in files]
    print(file_sizes)
    folder_sizes = []

    # 使用tqdm创建一个进度条
    for folder_name in tqdm(folders, desc="Scanning folders", unit="folder"):
        folder_path = os.path.abspath(os.path.join(root_dir, folder_name))
        total_size = 0

        # 遍历文件夹内的所有文件
        for dirpath, dirnames, filenames in os.walk(folder_path):
            print(dirpath, dirnames, filenames)
            for filename in filenames:
                try:
                    file_path = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(file_path)
                except OSError as e:
                    print(f"无法获取 {file_path} 的大小: {e}")

        folder_sizes.append((folder_name, total_size))

    # 按大小从大到小排序
    folder_sizes.sort(key=lambda x: x[1], reverse=True)

    # 打开文件准备写入结果
    if saving:

        with open(output_file, 'w', encoding='utf-8') as f:
            # 打印结果到文件
            for folder_name, total_size_bytes in folder_sizes:
                f.write(f"文件夹：{folder_name} 总大小：{get_size(total_size_bytes)}\n")
    else:
        for folder_name, total_size_bytes in folder_sizes:
            print(f"文件夹：{folder_name} 总大小：{get_size(total_size_bytes)}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="统计D盘每个文件夹的大小")
    parser.add_argument(
        "--dir", type=str, default="D:/", help="指定要统计的目录，默认为D盘根目录"
    )
    parser.add_argument(
        "--saving", action="store_true", default = False, help = "是否保存"
    )
    parser.add_argument(
        "--output", type=str, default="fixed_size_report.txt", help="指定输出文件的名称和路径"
    )
    args = parser.parse_args()
    transverse(args.dir, args.saving, args.output)