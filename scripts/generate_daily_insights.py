#!/usr/bin/env python3
"""
自动生成每日灵感洞察

使用 LLM 分析当日新闻，生成：
- 行业趋势洞察 (industry_insight)
- 创业建议 (startup_advice)  
- 项目创意 (side_project)

使用方法：
    python scripts/generate_daily_insights.py 2026-07-30
    # 或在 cron job 中调用
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
import requests

# 配置
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ALL_DATA_FILE = DATA_DIR / "all_inspiration.json"

# LLM API 配置（使用 OpenAI 兼容 API）
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")


def load_today_news(date_str: str) -> list:
    """从 all_inspiration.json 中加载指定日期的新闻"""
    if not ALL_DATA_FILE.exists():
        print(f"错误：找不到 {ALL_DATA_FILE}")
        return []
    
    with open(ALL_DATA_FILE, "r", encoding="utf-8") as f:
        all_data = json.load(f)
    
    # all_inspiration.json 可能是数组或对象
    if isinstance(all_data, dict):
        # 如果是对象，尝试获取 records 或 items
        news_list = all_data.get("records", all_data.get("items", []))
    else:
        # 如果是数组，直接使用
        news_list = all_data
    
    # 过滤指定日期的新闻
    today_news = [
        item for item in news_list 
        if item.get("date") == date_str
    ]
    
    print(f"✓ 找到 {len(today_news)} 条 {date_str} 的新闻")
    return today_news


def format_news_for_prompt(news_items: list) -> str:
    """将新闻格式化为 LLM prompt"""
    lines = []
    for i, item in enumerate(news_items, 1):
        title = item.get("title", "无标题")
        summary = item.get("summary", "无摘要")
        category = item.get("category", "unknown")
        importance = item.get("importance", 3)
        
        lines.append(f"{i}. [{category}] {title}")
        lines.append(f"   摘要: {summary}")
        lines.append(f"   重要性: {importance}/5")
        lines.append("")
    
    return "\n".join(lines)


def call_llm(system_prompt: str, user_prompt: str) -> dict:
    """调用 LLM API"""
    if not LLM_API_KEY:
        print("错误：未设置 LLM_API_KEY 环境变量")
        return None
    
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # 清理 markdown 代码块标记
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        return json.loads(content)
    
    except requests.exceptions.RequestException as e:
        print(f"LLM API 调用失败: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        print(f"原始内容: {content}")
        return None


def generate_insights_batch(news_text: str, insight_type: str, min_count: int = 1) -> list:
    """
    批量生成指定类型的 insights
    
    Args:
        news_text: 新闻文本
        insight_type: insight 类型 (industry_insight/startup_advice/side_project)
        min_count: 最少生成数量
    
    Returns:
        list of insights
    """
    type_config = {
        "industry_insight": {
            "role": "你是一个专业的 AI 行业分析师，擅长从新闻中提炼洞察。输出严格的 JSON 格式。",
            "prompt_template": """你是一个 AI 行业分析师。根据以下今日 AI 领域的新闻动态，总结 {count} 个重要的行业趋势洞察。

今日新闻：
{news_text}

要求：
1. 识别跨新闻的共性主题
2. 分析技术发展方向
3. 预测可能的行业影响
4. 每个洞察用 100 字以内总结趋势
5. 按重要性排序

输出严格的 JSON 格式（不要包含 markdown 代码块标记）：
{{
  "insights": [
    {{
      "type": "industry_insight",
      "title": "趋势标题（20字以内）",
      "body": "100字以内的趋势分析",
      "importance": 4,
      "score": 80,
      "summary": "一句话概括（15字以内）"
    }}
  ]
}}"""
        },
        "startup_advice": {
            "role": "你是一个专业的创业顾问，擅长发现商业机会。输出严格的 JSON 格式。",
            "prompt_template": """你是一个创业顾问。根据以下今日 AI 新闻动态，为创业者提供 {count} 条实用建议。

今日新闻：
{news_text}

要求：
1. 从技术趋势中发现商业机会
2. 识别未被满足的市场需求
3. 给出具体的创业方向建议
4. 说明为什么现在是好时机
5. 每条建议包含可执行的步骤
6. 按重要性排序

输出严格的 JSON 格式（不要包含 markdown 代码块标记）：
{{
  "insights": [
    {{
      "type": "startup_advice",
      "title": "建议标题（20字以内）",
      "body": "150字以内的创业建议",
      "importance": 4,
      "score": 75,
      "summary": "一句话概括（15字以内）",
      "actionable_steps": ["步骤1", "步骤2", "步骤3"]
    }}
  ]
}}"""
        },
        "side_project": {
            "role": "你是一个技术创意导师，擅长设计可执行的小项目。输出严格的 JSON 格式。",
            "prompt_template": """你是一个技术创意导师。根据以下今日 AI 新闻动态，提出 {count} 个可以做的小项目创意。

今日新闻：
{news_text}

要求：
1. 基于热门技术或工具
2. 项目规模适合独立开发者
3. 1-2周可完成
4. 有实际应用价值
5. 按实用性和创新性排序

输出严格的 JSON 格式（不要包含 markdown 代码块标记）：
{{
  "insights": [
    {{
      "type": "side_project",
      "title": "项目名称（20字以内）",
      "body": "100字以内的项目描述",
      "importance": 3,
      "score": 70,
      "summary": "一句话概括（15字以内）",
      "tech_stack": ["技术1", "技术2"],
      "estimated_time": "1周"
    }}
  ]
}}"""
        }
    }
    
    if insight_type not in type_config:
        print(f"错误：未知的 insight 类型: {insight_type}")
        return []
    
    config = type_config[insight_type]
    system_prompt = config["role"]
    
    # 尝试生成多个 insights（2-3条）
    for count in [3, 2, 1]:
        user_prompt = config["prompt_template"].format(count=count, news_text=news_text)
        
        result = call_llm(system_prompt, user_prompt)
        
        if result and "insights" in result:
            insights = result["insights"]
            # 验证每条 insight
            valid_insights = []
            for insight in insights:
                if insight.get("type") == insight_type and insight.get("title"):
                    valid_insights.append(insight)
            
            if len(valid_insights) >= min_count:
                return valid_insights
    
    return []


def save_daily_insights(date_str: str, insights: list, records: list):
    """保存每日灵感到 JSON 文件"""
    output_file = DATA_DIR / f"inspiration_{date_str}.json"
    
    # 统计分类
    categories = {
        "ai_tech": 0,
        "startup": 0,
        "product_tool": 0,
        "academic_paper": 0
    }
    
    for record in records:
        cat = record.get("category", "unknown")
        if cat in categories:
            categories[cat] += 1
    
    output_data = {
        "date": date_str,
        "records": records,
        "total_new": len(records),
        "categories": categories,
        "is_major_event": any(r.get("is_major_event") for r in records),
        "insights": insights,
        "generated_at": datetime.now().isoformat()
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 已保存到 {output_file}")


def main():
    """主函数"""
    # 获取日期参数
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    print(f"📅 生成 {date_str} 的每日灵感洞察\n")
    
    # 检查 API key
    if not LLM_API_KEY:
        print("错误：未设置 LLM_API_KEY 环境变量")
        print("运行: export LLM_API_KEY='your-api-key'")
        sys.exit(1)
    
    # 加载当日新闻
    news_items = load_today_news(date_str)
    if not news_items:
        print(f"错误：{date_str} 没有新闻数据")
        sys.exit(1)
    
    # 格式化新闻
    news_text = format_news_for_prompt(news_items)
    
    # 生成三类洞察（每类至少1条，最多3条）
    insights = []
    
    # 1. 行业趋势洞察
    print("\n🔍 生成行业趋势洞察...")
    industry_insights = generate_insights_batch(news_text, "industry_insight", min_count=1)
    if industry_insights:
        insights.extend(industry_insights)
        print(f"  ✓ 生成 {len(industry_insights)} 条行业趋势洞察")
        for insight in industry_insights:
            print(f"    - {insight['title']}")
    else:
        print("  ✗ 生成失败")
    
    # 2. 创业建议
    print("\n💡 生成创业建议...")
    startup_insights = generate_insights_batch(news_text, "startup_advice", min_count=1)
    if startup_insights:
        insights.extend(startup_insights)
        print(f"  ✓ 生成 {len(startup_insights)} 条创业建议")
        for insight in startup_insights:
            print(f"    - {insight['title']}")
    else:
        print("  ✗ 生成失败")
    
    # 3. 项目创意
    print("\n🚀 生成项目创意...")
    project_insights = generate_insights_batch(news_text, "side_project", min_count=1)
    if project_insights:
        insights.extend(project_insights)
        print(f"  ✓ 生成 {len(project_insights)} 条项目创意")
        for insight in project_insights:
            print(f"    - {insight['title']}")
    else:
        print("  ✗ 生成失败")
    
    # 保存结果
    if insights:
        print(f"\n💾 保存结果...")
        save_daily_insights(date_str, insights, news_items)
        print(f"\n✅ 完成！生成了 {len(insights)} 条灵感洞察")
    else:
        print("\n❌ 未能生成任何洞察")
        sys.exit(1)


if __name__ == "__main__":
    main()
