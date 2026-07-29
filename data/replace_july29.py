import json

# 读取 all_inspiration.json
with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 读取灵感文件获取完整信息
with open('inspiration_2026-07-29.json', 'r', encoding='utf-8') as f:
    inspiration = json.load(f)

# 删除所有旧7.29记录
before = len(data)
data = [r for r in data if r.get('date') != '2026-07-29']
removed = before - len(data)
print(f"移除旧7.29记录: {removed} 条")

# 添加新格式的7.29记录
for rec in inspiration['records']:
    data.append(rec)
print(f"添加新7.29记录: {len(inspiration['records'])} 条")

# 按日期和ID排序
data.sort(key=lambda x: (x.get('date', ''), x.get('id', '')))

# 保存
with open('all_inspiration.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 验证
with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    verify = json.load(f)

july29 = [r for r in verify if r.get('date') == '2026-07-29']
print(f"\n✓ 验证: 7.29 共 {len(july29)} 条")
for r in july29:
    has_kw = 'keywords' in r
    has_url = 'url' in r
    has_src = 'source' in r
    print(f"  [{r.get('category')}] {r.get('title')[:40]} | url:{has_url} src:{has_src} kw:{has_kw}")
