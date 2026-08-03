#!/usr/bin/env python3
"""
清理不完整数据的日期文件
删除没有 records 字段的 inspiration_*.json 文件
更新 all_inspiration.json 只保留有数据的日期
"""
import json
from pathlib import Path

data_dir = Path(__file__).parent.parent / "data"

# 找到所有 inspiration 文件
inspiration_files = sorted(data_dir.glob("inspiration_*.json"))

files_to_keep = []
files_to_delete = []

print("检查所有日期文件...\n")

for file in inspiration_files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 检查是否有 records 字段且有数据
    if 'records' in data and len(data['records']) > 0:
        files_to_keep.append(file)
        print(f"✓ {file.name}: {len(data['records'])} 条记录")
    else:
        files_to_delete.append(file)
        print(f"✗ {file.name}: 数据不完整（只有 insights）")

print(f"\n保留 {len(files_to_keep)} 个完整文件")
print(f"删除 {len(files_to_delete)} 个不完整文件\n")

# 删除不完整文件
for file in files_to_delete:
    file.unlink()
    print(f"已删除: {file.name}")

# 重新构建 all_inspiration.json
print("\n重建 all_inspiration.json...")
all_records = []

for file in sorted(files_to_keep):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    all_records.extend(data['records'])
    print(f"  加载 {file.name}: {len(data['records'])} 条")

# 保存更新后的 all_inspiration.json
all_inspiration_path = data_dir / "all_inspiration.json"
with open(all_inspiration_path, 'w', encoding='utf-8') as f:
    json.dump(all_records, f, ensure_ascii=False, indent=2)

print(f"\n✓ 已更新 all_inspiration.json: {len(all_records)} 条记录")

# 统计日期分布
date_counts = {}
for record in all_records:
    date = record.get('date', 'unknown')
    date_counts[date] = date_counts.get(date, 0) + 1

print("\n可用日期：")
for date in sorted(date_counts.keys(), reverse=True):
    print(f"  {date}: {date_counts[date]} 条记录")
