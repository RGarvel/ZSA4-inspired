#!/usr/bin/env python3
import json
from datetime import datetime

# 读取 all_inspiration.json
with open(r'C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data\all_inspiration.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

# 筛选 2026-07-30 的条目
july30_items = [item for item in all_data if item.get('date') == '2026-07-30']

# 统计分类
categories = {
    "ai_tech": 0,
    "startup": 0,
    "product_tool": 0,
    "academic_paper": 0
}

for item in july30_items:
    cat = item.get('category', 'ai_tech')
    if cat in categories:
        categories[cat] += 1

# 构建新的数据结构
new_data = {
    "date": "2026-07-30",
    "records": july30_items,
    "total_new": len(july30_items),
    "categories": categories,
    "is_major_event": False,
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
    "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000000")
}

# 写入文件
output_path = r'C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data\inspiration_2026-07-30.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f"✓ 更新完成")
print(f"  日期: 2026-07-30")
print(f"  记录数: {len(july30_items)}")
print(f"  分类统计:")
for cat, count in categories.items():
    print(f"    {cat}: {count}")
