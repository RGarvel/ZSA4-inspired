import json

with open(r'C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data\all_inspiration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(r'C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data\inspiration_2026-07-20.json', 'r', encoding='utf-8') as f:
    insights = json.load(f)

# Stats
total = len(data)
ai_tech = [x for x in data if x['category'] == 'ai_tech']
startup = [x for x in data if x['category'] == 'startup']
product = [x for x in data if x['category'] == 'product_tool']

major_events = [x for x in data if x.get('is_major_event')]
today_items = [x for x in data if x['date'] == '2026-07-20']

print(f"=== 灵感日报 2026-07-20 ===")
print(f"总数据量: {total}")
print(f"  AI技术: {len(ai_tech)} | 创业动态: {len(startup)} | 产品工具: {len(product)}")
print(f"重大事件: {len(major_events)}")
print(f"今日新增: {len(today_items)}")
print()

# Generate markdown report
md = []
md.append("# 🧭 灵感日报 — 2026年7月20日（周一）")
md.append("")

md.append("## ⭐ 重大事件")
md.append("")
for item in major_events:
    md.append(f"- ⭐ [{item['date']}] **{item['title']}** — {item['raw_summary'][:100]}...")
md.append("")

md.append("## 🔬 AI 技术")
md.append("")
for item in sorted(ai_tech, key=lambda x: x['date'], reverse=True):
    if item['date'] == '2026-07-20':
        md.append(f"**🆕 今日** — {item['title']}")
        md.append(f"  - {item['raw_summary'][:200]}")
        md.append(f"  - 来源: {item['source']} | [链接]({item['url']})")
    else:
        md.append(f"- [{item['date']}] **{item['title']}** — {item['raw_summary'][:150]}")
md.append("")

md.append("## 💼 创业动态")
md.append("")
for item in sorted(startup, key=lambda x: x['date'], reverse=True):
    if item['date'] == '2026-07-20':
        md.append(f"**🆕 今日** — {item['title']}")
        md.append(f"  - {item['raw_summary'][:200]}")
    else:
        md.append(f"- [{item['date']}] **{item['title']}** — {item['raw_summary'][:150]}")
md.append("")

md.append("## 🛠️ 产品工具")
md.append("")
for item in sorted(product, key=lambda x: x['date'], reverse=True):
    if item['date'] == '2026-07-20':
        md.append(f"**🆕 今日** — {item['title']}")
        md.append(f"  - {item['raw_summary'][:200]}")
    else:
        md.append(f"- [{item['date']}] **{item['title']}** — {item['raw_summary'][:150]}")
md.append("")

md.append("## 💡 今日灵感")
md.append("")
for ins in insights['insights']:
    if ins['type'] == 'startup_advice':
        md.append(f"### 🚀 创业建议：{ins['title']}")
        md.append(f"{ins['summary']}")
        md.append(f"关联: {', '.join(ins['related_news'])} | Tags: {', '.join(ins['tags'])}")
        md.append("")
    elif ins['type'] == 'side_project':
        md.append(f"### 🔧 小项目：{ins['title']}")
        md.append(f"{ins['summary']}")
        md.append(f"难度: {ins.get('difficulty','?')} | 时间: {ins.get('estimated_time','?')} | 技术栈: {', '.join(ins.get('tech_stack',[]))}")
        md.append(f"关联: {', '.join(ins['related_news'])}")
        md.append("")
    elif ins['type'] == 'industry_insight':
        md.append(f"### 🔍 行业洞察：{ins['title']}")
        md.append(f"{ins['summary']}")
        md.append(f"关联: {', '.join(ins['related_news'])} | Tags: {', '.join(ins['tags'])}")
        md.append("")

md.append("---")
md.append("")
md.append("## 📊 统计摘要")
md.append(f"- 总收录条目: {total}")
md.append(f"- AI 技术: {len(ai_tech)} | 创业动态: {len(startup)} | 产品工具: {len(product)}")
md.append(f"- 重大事件: {len(major_events)}")
md.append(f"- 灵感条目: {len(insights['insights'])}（创业建议×2、小项目×3、行业洞察×2）")
md.append(f"- 数据日期范围: {data[-1]['date']} ~ {data[0]['date']}")

report = '\n'.join(md)
print(report)

# Save report
with open(r'C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data\report_2026-07-20.md', 'w', encoding='utf-8') as f:
    f.write(report)
print("\n\n✅ Report saved to report_2026-07-20.md")
