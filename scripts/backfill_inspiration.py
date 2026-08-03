#!/usr/bin/env python3
"""
回溯采集灵感日报数据（7.19-7.26）
通过 arXiv API 和 web_search 获取历史数据
"""
import json
import os
import sys
import time
import re
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from html import unescape

def categorize_and_score(item):
    """
    根据标题和内容对条目进行分类和重要性评分
    """
    title = (item.get('title') or '').lower()
    
    # 分类逻辑
    if any(kw in title for kw in ['paper', 'arxiv', '研究', '论文', 'benchmark']):
        item['category'] = 'academic'
    elif any(kw in title for kw in ['funding', '融资', 'investment', 'startup', 'launch', '发布', 'announced']):
        item['category'] = 'startup'
    elif any(kw in title for kw in ['product', 'tool', 'api', 'platform', '工具', '产品']):
        item['category'] = 'product_tool'
    else:
        item['category'] = 'ai_tech'
    
    # 重要性评分逻辑
    importance = 2
    
    # 重大事件关键词
    major_keywords = ['gpt-5', 'claude', 'gemini', 'openai', 'anthropic', 'google deepmind',
                      'breakthrough', 'sota', 'state-of-the-art', 'record', '首次', '重大', '突破']
    
    if any(kw in title for kw in major_keywords):
        importance = 4
        item['is_major_event'] = True
    elif any(kw in title for kw in ['new', 'new', 'latest', '最新', '刚刚']):
        importance = 3
    else:
        item['is_major_event'] = False
    
    item['importance'] = importance
    return item

def fetch_arxiv_for_date(target_date, max_days_back=2):
    """
    获取指定日期附近的 arXiv 论文
    arXiv API 没有精确的日期过滤，我们需要获取最近的数据然后按 published 日期过滤
    """
    import urllib.request
    import urllib.parse
    
    # arXiv API 查询
    base_url = "https://export.arxiv.org/api/query?"
    
    # 使用更广泛的查询来获取更多结果
    queries = [
        'search_query=all:"LLM" OR all:"GPT" OR all:"Claude" OR all:"Gemini"',
        'search_query=all:"AI agent" OR all:"multimodal" OR all:"reasoning"',
        'search_query=cat:cs.AI OR cat:cs.CL OR cat:cs.LG'
    ]
    
    all_papers = []
    
    for query in queries:
        params = {
            'start': 0,
            'max_results': 50,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        url = base_url + query + '&' + urllib.parse.urlencode(params)
        
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read().decode('utf-8')
            
            # 解析 Atom feed
            import xml.etree.ElementTree as ET
            root = ET.fromstring(data)
            
            # Atom namespace
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', ns):
                published = entry.find('atom:published', ns).text
                # 解析日期：2026-07-29T12:34:56Z
                pub_date = datetime.strptime(published[:10], '%Y-%m-%d').date()
                
                # 检查是否在目标日期范围内（允许前后几天）
                days_diff = abs((pub_date - target_date).days)
                if days_diff <= max_days_back:
                    title = entry.find('atom:title', ns).text.strip()
                    summary = entry.find('atom:summary', ns).text.strip()
                    link = entry.find('atom:id', ns).text
                    
                    all_papers.append({
                        'title': title,
                        'summary': summary[:500],
                        'url': link,
                        'published': published[:10],
                        'source': 'arxiv'
                    })
            
            # 避免请求过快
            time.sleep(1)
            
        except Exception as e:
            print(f"  arXiv 查询失败: {e}")
            continue
    
    return all_papers


def main():
    """主函数"""
    # 定义项目根目录
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    
    # 目标日期：7.19 - 7.26
    start_date = datetime(2026, 7, 19).date()
    end_date = datetime(2026, 7, 26).date()
    
    print(f"开始回溯采集 {start_date} 到 {end_date} 的数据...\n")
    
    # 加载现有的 all_inspiration.json
    all_inspiration_path = data_dir / "all_inspiration.json"
    if all_inspiration_path.exists():
        with open(all_inspiration_path, 'r', encoding='utf-8') as f:
            all_inspiration = json.load(f)
        print(f"已加载 {len(all_inspiration)} 条现有记录")
    else:
        all_inspiration = []
        print("创建新的 all_inspiration.json")
    
    # 创建已见标题集合（用于去重）
    seen_titles = {item['title'].lower() for item in all_inspiration}
    
    current_date = start_date
    
    while current_date <= end_date:
        date_str = current_date.isoformat()
        print(f"\n处理日期: {date_str}")
        
        # 检查是否已经有这个日期的完整数据
        date_file = data_dir / f"inspiration_{date_str}.json"
        if date_file.exists():
            with open(date_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            if 'records' in existing_data and len(existing_data['records']) > 0:
                print(f"  已有 {len(existing_data['records'])} 条记录，跳过")
                current_date += timedelta(days=1)
                continue
        
        # 获取 arXiv 数据
        print(f"  查询 arXiv 论文...")
        arxiv_papers = fetch_arxiv_for_date(current_date)
        print(f"  找到 {len(arxiv_papers)} 篇相关论文")
        
        # 构建 records
        new_records = []
        
        # 处理 arXiv 论文
        for paper in arxiv_papers:
            if paper['title'].lower() in seen_titles:
                continue
            
            record = {
                'id': f"arxiv_{current_date}_{len(new_records)}",
                'date': date_str,
                'title': paper['title'],
                'summary': paper['summary'],
                'url': paper['url'],
                'category': 'academic',
                'importance': 3,
                'is_major_event': False,
                'source': paper['source'],
                'tags': ['arxiv', 'research'],
                'published': paper['published']
            }
            
            # 应用启发式规则
            record = categorize_and_score(record)
            new_records.append(record)
            seen_titles.add(paper['title'].lower())
        
        print(f"  新增 {len(new_records)} 条记录")
        
        if new_records:
            # 生成 insights
            insights = generate_insights_from_records(new_records)
            
            # 保存日期文件
            date_data = {
                'date': date_str,
                'records': new_records,
                'insights': insights,
                'total_items': len(new_records)
            }
            
            with open(date_file, 'w', encoding='utf-8') as f:
                json.dump(date_data, f, ensure_ascii=False, indent=2)
            
            print(f"  已保存到 {date_file.name}")
            
            # 添加到 all_inspiration
            all_inspiration.extend(new_records)
        
        current_date += timedelta(days=1)
    
    # 保存更新后的 all_inspiration.json
    with open(all_inspiration_path, 'w', encoding='utf-8') as f:
        json.dump(all_inspiration, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成！总共采集到 {len(all_inspiration)} 条记录")
    print(f"已更新 {all_inspiration_path.name}")


def generate_insights_from_records(records):
    """
    从记录生成 insights
    简单版本：基于分类统计
    """
    category_counts = {}
    for record in records:
        cat = record.get('category', 'other')
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    insights = []
    
    # 生成行业趋势洞察
    if category_counts.get('ai_tech', 0) > 0 or category_counts.get('academic', 0) > 0:
        insights.append({
            'title': 'AI 技术进展',
            'type': 'tech_insight',
            'summary': f"今日收录 {category_counts.get('ai_tech', 0)} 条技术动态和 {category_counts.get('academic', 0)} 篇学术论文",
            'importance': 3
        })
    
    # 生成创业建议
    if category_counts.get('startup', 0) > 0:
        insights.append({
            'title': '创业机会',
            'type': 'startup_advice',
            'summary': f"今日收录 {category_counts.get('startup', 0)} 条创业动态，关注最新融资和产品发布",
            'importance': 3
        })
    
    # 生成项目创意
    if category_counts.get('product_tool', 0) > 0:
        insights.append({
            'title': '产品灵感',
            'type': 'side_project',
            'summary': f"今日收录 {category_counts.get('product_tool', 0)} 个产品工具，可探索新的应用场景",
            'importance': 3
        })
    
    return insights


if __name__ == '__main__':
    main()
