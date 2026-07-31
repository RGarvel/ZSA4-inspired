#!/usr/bin/env python3
"""
自动生成每日灵感洞察

使用 Hermes CLI (hermes -z) 调用 LLM 分析当日新闻，生成：
- 行业趋势洞察 (industry_insight)
- 创业建议 (startup_advice)
- 项目创意 (side_project)

使用方法：
    python scripts/generate_daily_insights.py 2026-07-30
"""

import json
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path

# 配置
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ALL_DATA_FILE = DATA_DIR / "all_inspiration.json"


def load_today_news(date_str: str) -> list:
    """从 all_inspiration.json 中加载指定日期的新闻"""
    if not ALL_DATA_FILE.exists():
        print(f"错误：找不到 {ALL_DATA_FILE}")
        return []

    with open(ALL_DATA_FILE, "r", encoding="utf-8") as f:
        all_data = json.load(f)

    today_news = [item for item in all_data if item.get("date") == date_str]
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


def call_llm(system_prompt: str, user_prompt: str, max_retries: int = 3) -> dict:
    """通过 hermes -z 调用 LLM，返回 JSON（带重试和速率限制）"""
    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["hermes", "-z", full_prompt, "--no-restore-cwd"],
                capture_output=True,
                text=True,
                timeout=60,
                encoding="utf-8",
            )

            if result.returncode != 0:
                stderr = result.stderr.lower()
                # 检测 429 速率限制错误
                if "429" in stderr or "rate" in stderr or "exhaust" in stderr or "quota" in stderr:
                    wait_time = 2 ** attempt * 10  # 指数退避: 10s, 20s, 40s
                    print(f"⚠ 速率限制 (429)，等待 {wait_time}s 后重试 ({attempt+1}/{max_retries})...")
                    time.sleep(wait_time)
                    continue
                print(f"hermes CLI 调用失败 (exit {result.returncode})")
                print(f"stderr: {result.stderr[:200]}")
                return None

            content = result.stdout.strip()

            # 清理 markdown 代码块标记
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            return json.loads(content)

        except subprocess.TimeoutExpired:
            print(f"hermes CLI 超时 (60s)，重试 ({attempt+1}/{max_retries})...")
            time.sleep(2 ** attempt * 5)
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
            print(f"原始内容: {content[:200]}")
            return None
        except Exception as e:
            print(f"调用异常: {e}")
            return None

    print(f"✗ 达到最大重试次数 ({max_retries})，放弃")
    return None


def generate_industry_insight(news_text: str) -> dict:
    """生成行业趋势洞察"""
    system_prompt = "你是一个专业的 AI 行业分析师，擅长从新闻中提炼洞察。只输出 JSON，不要任何额外文字。"

    user_prompt = f"""根据以下今日 AI 领域的新闻动态，总结 1 个重要的行业趋势洞察。

今日新闻：
{news_text}

要求：
1. 识别跨新闻的共性主题
2. 分析技术发展方向
3. 预测可能的行业影响
4. 用 100 字以内总结趋势

只输出严格的 JSON 格式（不要 markdown 代码块）：
{{
  "type": "industry_insight",
  "title": "趋势标题（20字以内）",
  "body": "100字以内的趋势分析",
  "importance": 4,
  "score": 80,
  "summary": "一句话概括（15字以内）"
}}"""
    return call_llm(system_prompt, user_prompt)


def generate_startup_advice(news_text: str) -> dict:
    """生成创业建议"""
    system_prompt = "你是一个专业的创业顾问，擅长发现商业机会。只输出 JSON，不要任何额外文字。"

    user_prompt = f"""根据以下今日 AI 新闻动态，为创业者提供 1 条实用建议。

今日新闻：
{news_text}

要求：
1. 从技术趋势中发现商业机会
2. 识别未被满足的市场需求
3. 给出具体的创业方向建议
4. 说明为什么现在是好时机

只输出严格的 JSON 格式（不要 markdown 代码块）：
{{
  "type": "startup_advice",
  "title": "建议标题（20字以内）",
  "body": "150字以内的创业建议",
  "importance": 4,
  "score": 75,
  "summary": "一句话概括（15字以内）",
  "actionable_steps": ["步骤1", "步骤2", "步骤3"]
}}"""
    return call_llm(system_prompt, user_prompt)


def generate_side_project(news_text: str) -> dict:
    """生成项目创意"""
    system_prompt = "你是一个技术创意导师，擅长设计可执行的小项目。只输出 JSON，不要任何额外文字。"

    user_prompt = f"""根据以下今日 AI 新闻动态，提出 1 个可以做的小项目创意。

今日新闻：
{news_text}

要求：
1. 基于热门技术或工具
2. 项目规模适合独立开发者
3. 1-2周可完成
4. 有实际应用价值

只输出严格的 JSON 格式（不要 markdown 代码块）：
{{
  "type": "side_project",
  "title": "项目名称（20字以内）",
  "body": "100字以内的项目描述",
  "importance": 3,
  "score": 70,
  "summary": "一句话概括（15字以内）",
  "tech_stack": ["技术1", "技术2"],
  "estimated_time": "1周"
}}"""
    return call_llm(system_prompt, user_prompt)


def save_daily_insights(date_str: str, insights: list, records: list):
    """保存每日灵感到 JSON 文件"""
    output_file = DATA_DIR / f"inspiration_{date_str}.json"

    # 统计分类
    categories = {
        "ai_tech": 0,
        "startup": 0,
        "product_tool": 0,
        "academic_paper": 0,
        "academic": 0
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

    # 加载当日新闻
    news_items = load_today_news(date_str)
    if not news_items:
        print(f"错误：{date_str} 没有新闻数据")
        sys.exit(1)

    # 格式化新闻
    news_text = format_news_for_prompt(news_items)

    # 生成三类洞察
    insights = []

    print("\n🔍 生成行业趋势洞察...")
    insight1 = generate_industry_insight(news_text)
    if insight1:
        insights.append(insight1)
        print(f"  ✓ {insight1['title']}")
    else:
        print("  ✗ 生成失败")

    # 速率控制：等待 2 秒再调用下一个
    time.sleep(2)

    print("\n💡 生成创业建议...")
    insight2 = generate_startup_advice(news_text)
    if insight2:
        insights.append(insight2)
        print(f"  ✓ {insight2['title']}")
    else:
        print("  ✗ 生成失败")

    # 速率控制：等待 2 秒再调用下一个
    time.sleep(2)

    print("\n🚀 生成项目创意...")
    insight3 = generate_side_project(news_text)
    if insight3:
        insights.append(insight3)
        print(f"  ✓ {insight3['title']}")
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
