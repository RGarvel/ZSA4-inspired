#!/usr/bin/env python3
"""
格式化灵感日报 QQ 推送消息

读取 inspiration_{TODAY}.json 和 models.json，按 AI Dashboard report 风格输出。

使用方法：
    python scripts/format_daily_report.py 2026-07-31
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# 配置
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DASHBOARD_DIR = PROJECT_ROOT / "project" / "ai-model-price-dashboard"


def load_inspiration(date_str: str) -> dict:
    """加载当日灵感数据"""
    file = DATA_DIR / f"inspiration_{date_str}.json"
    if not file.exists():
        print(f"⚠ 找不到 {file}")
        return {}
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_models() -> dict:
    """加载仪表盘模型数据"""
    file = DASHBOARD_DIR / "data" / "models.json"
    if not file.exists():
        print(f"⚠ 找不到 {file}")
        return {}
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def get_recommendation(models_data: dict) -> dict:
    """计算综合推荐模型（质量前5中性价比最高）"""
    models = models_data.get("models", [])
    if not models:
        return {}

    # 按 composite_score 降序，取前5
    top5 = sorted(models, key=lambda m: m.get("composite_score") or 0, reverse=True)[:5]

    # 从前5中选出 value_score 最高的
    best = max(top5, key=lambda m: m.get("value_score") or 0)
    return best


def format_report(date_str: str) -> str:
    """生成 AI Dashboard report 风格的 QQ 消息"""
    insp = load_inspiration(date_str)
    models_data = load_models()

    # 采集统计
    categories = insp.get("categories", {})
    total_new = insp.get("total_new", 0)
    records = insp.get("records", [])
    insights = insp.get("insights", [])

    # 重大事件（importance >= 4）
    major_events = [r for r in records if r.get("importance", 0) >= 4][:5]

    # 分类统计
    ai_tech = categories.get("ai_tech", 0)
    startup = categories.get("startup", 0)
    product_tool = categories.get("product_tool", 0)
    academic_paper = categories.get("academic_paper", 0)

    # 分组 insights
    industry = [i for i in insights if i.get("type") == "industry_insight"]
    startup_adv = [i for i in insights if i.get("type") == "startup_advice"]
    side_proj = [i for i in insights if i.get("type") == "side_project"]

    # 推荐模型
    rec = get_recommendation(models_data)
    updated_at = models_data.get("updated_at", "N/A")

    # 构建 report
    lines = []
    sep = "=" * 70

    lines.append(sep)
    lines.append(f"📅 灵感日报 · {date_str}")
    lines.append(sep)
    lines.append("")
    lines.append("【采集统计】")
    lines.append(f"• 新增 {total_new} 条 | AI技术 {ai_tech} · 创业 {startup} · 产品 {product_tool} · 学术 {academic_paper}")
    lines.append("")
    lines.append(sep)
    lines.append("")

    # 重大事件
    lines.append("【🔥 重大事件】")
    if major_events:
        for i, e in enumerate(major_events, 1):
            lines.append(f"{i}. {e.get('title', '')} — {e.get('summary', '')[:80]}")
    else:
        lines.append("无")
    lines.append("")

    # 行业趋势
    lines.append("【💡 行业趋势】")
    if industry:
        for item in industry:
            lines.append(f"• {item.get('title', '')} — {item.get('summary', '')}")
    else:
        lines.append("无")
    lines.append("")

    # 创业建议
    lines.append("【🚀 创业建议】")
    if startup_adv:
        for item in startup_adv:
            lines.append(f"• {item.get('title', '')} — {item.get('summary', '')}")
    else:
        lines.append("无")
    lines.append("")

    # 项目创意
    lines.append("【🛠️ 项目创意】")
    if side_proj:
        for item in side_proj:
            lines.append(f"• {item.get('title', '')} — {item.get('summary', '')}")
    else:
        lines.append("无")
    lines.append("")
    lines.append(sep)
    lines.append("")

    # AI 模型推荐
    lines.append(f"【🤖 AI 模型推荐】（仪表盘更新于 {updated_at}）")
    if rec:
        name = rec.get("name", "N/A")
        cs = rec.get("composite_score", 0)
        vs = rec.get("value_score", 0)
        op = rec.get("output_price_per_1m", 0)
        lines.append(f"• 综合推荐：{name} | 质量{cs} | 性价比{vs} | ${op}/M tokens")
    else:
        lines.append("• 无推荐数据")
    lines.append("")

    # GitHub
    lines.append("【📦 GitHub】")
    lines.append("✓ 已推送 https://github.com/RGarvel/ZSA4-inspired")
    lines.append("")
    lines.append("📰 灵感日报：https://rgarvel.github.io/ZSA4-inspired/")
    lines.append("")
    lines.append(sep)

    return "\n".join(lines)


def main():
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    report = format_report(date_str)
    print(report)


if __name__ == "__main__":
    main()
