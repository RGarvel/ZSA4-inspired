#!/usr/bin/env python3
"""修复 all_inspiration.json 中的分类字段"""
import json
from pathlib import Path

DATA_FILE = Path(r"C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data\all_inspiration.json")

# 读取数据
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 修复分类字段
fixed_count = 0
for item in data:
    if item.get('category') == 'academic':
        item['category'] = 'academic_paper'
        fixed_count += 1

# 保存回文件
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✓ 修复了 {fixed_count} 条记录：'academic' → 'academic_paper'")

# 验证
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)
july30_papers = [item for item in data if item.get('date') == '2026-07-30' and item.get('category') == 'academic_paper']
print(f"✓ 2026-07-30 现在有 {len(july30_papers)} 篇学术论文")
