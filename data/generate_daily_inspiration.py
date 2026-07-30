#!/usr/bin/env python3
"""从 all_inspiration.json 生成每日灵感日报文件"""
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(r"C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data")
ALL_DATA = DATA_DIR / "all_inspiration.json"
TODAY = "2026-07-30"

# 读取所有数据
with open(ALL_DATA, 'r', encoding='utf-8') as f:
    all_data = json.load(f)

# 过滤今日数据
today_data = [item for item in all_data if item.get('date') == TODAY]

# 统计分类
categories = {
    'ai_tech': 0,
    'startup': 0,
    'product_tool': 0,
    'academic_paper': 0
}

for item in today_data:
    cat = item.get('category', 'ai_tech')
    if cat in categories:
        categories[cat] += 1

# 构建灵感日报结构
inspiration_data = {
    "date": TODAY,
    "total_new": len(today_data),
    "categories": categories,
    "is_major_event": any(item.get('is_major_event') for item in today_data),
    "insights": [
        {
            "type": "industry_insight",
            "title": "多智能体系统成为研究热点",
            "body": "今日多篇论文聚焦于多智能体协作、通信优化和集体决策，显示多智能体系统正从理论走向实用阶段。",
            "importance": 4,
            "score": 80,
            "summary": "多智能体系统从理论走向实用阶段"
        },
        {
            "type": "industry_insight",
            "title": "医疗AI持续突破",
            "body": "医学影像分析、药物发现和临床决策支持系统相关论文数量增加，AI在医疗领域的应用深度持续拓展。",
            "importance": 4,
            "score": 75,
            "summary": "AI在医疗领域应用深度持续拓展"
        },
        {
            "type": "industry_insight",
            "title": "模型效率优化受关注",
            "body": "多篇论文探讨模型压缩、推理加速和计算资源优化，反映业界对降低成本和能耗的强烈需求。",
            "importance": 3,
            "score": 65,
            "summary": "业界对降低AI成本和能耗需求强烈"
        }
    ],
    "records": today_data  # 关键：填充 records 数组
}

# 保存到文件
output_file = DATA_DIR / f"inspiration_{TODAY}.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(inspiration_data, f, ensure_ascii=False, indent=2)

print(f"✓ 生成灵感日报: {output_file}")
print(f"  总数: {len(today_data)}")
print(f"  分类统计: {categories}")
print(f"  记录数: {len(today_data)}")
