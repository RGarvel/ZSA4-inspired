#!/usr/bin/env python3
"""检查并修复 all_inspiration.json 中 7.30 的数据"""
import json
from pathlib import Path

DATA_FILE = Path(r'C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data\all_inspiration.json')

# 读取数据
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 查找7.30的数据
july30_items = [item for item in data if item.get('date') == '2026-07-30']

print(f"找到 {len(july30_items)} 条 7.30 的记录\n")

# 检查每条记录的分类字段
for i, item in enumerate(july30_items[:5]):
    category = item.get('category', 'MISSING')
    title = item.get('title', 'N/A')[:50]
    has_source = 'source' in item
    print(f"记录 {i+1}:")
    print(f"  标题: {title}")
    print(f"  分类: {category}")
    print(f"  有source字段: {has_source}")
    print()

# 统计分类
categories = {}
for item in july30_items:
    cat = item.get('category', 'unknown')
    categories[cat] = categories.get(cat, 0) + 1

print("分类统计:")
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")

# 检查是否有 category 字段缺失的记录
missing_category = [item for item in july30_items if 'category' not in item]
print(f"\n缺少 category 字段的记录: {len(missing_category)}")

# 检查 source 字段
missing_source = [item for item in july30_items if 'source' not in item]
print(f"缺少 source 字段的记录: {len(missing_source)}")
