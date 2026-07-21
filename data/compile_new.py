#!/usr/bin/env python3
"""Compile new data, merge with existing, validate, and write all_inspiration.json."""
import json, os, re
from pathlib import Path

DATA_DIR = Path(os.environ.get("HOME", r"C:\Users\阮家威")) / "AppData" / "Local" / "hermes" / "data" / "inspiration" / "data"
DATA_FILE = DATA_DIR / "all_inspiration.json"

# ── New data collected today ──────────────────────────────────────────
new_data = [
    # --- AI TECH ---
    {
        "id": "ait-12",
        "date": "2026-07-20",
        "category": "ai_tech",
        "title": "Moonshot AI Kimi K3遭遇服务器过载：2.8万亿参数模型需求远超预期",
        "raw_summary": "Moonshot AI于7月16日发布Kimi K3后，因用户量激增导致服务器过载，订阅服务一度不可用。该公司于7月20日宣布正在加速部署新硬件，但尚未公布全面恢复的时间表。Kimi K3是全球最大的开源AI模型，拥有2.8万亿参数，采用稀疏MoE架构（896个专家中每次推理激活16个），原生视觉支持和100万token上下文窗口。定价为每百万输入token 3美元、输出15美元、缓存0.30美元。完整开源权重预计7月27日发布。",
        "source": "Reuters/Bloomberg",
        "url": "https://www.bloomberg.com/news/articles/2026-07-20/moonshot-s-kimi-k3-may-be-more-about-memory-than-compute",
        "keywords": ["Moonshot AI", "Kimi K3", "服务器过载", "MoE", "开源模型"],
        "original_language": "zh"
    },
    {
        "id": "ait-13",
        "date": "2026-07-20",
        "category": "ai_tech",
        "title": "Apple Intelligence获中国批准，阿里巴巴Qwen驱动",
        "raw_summary": "中国网信办于7月15日正式批准Apple Intelligence在中国落地，结束了长达22个月的等待。根据批准条件，Apple Intelligence在中国将使用阿里巴巴的Qwen模型处理语言和文本生成，百度负责视觉搜索。这是中国监管机构首次批准外国AI助手的本地化运营，标志着中美AI监管格局的重大变化。苹果此前因无法找到符合中国法规的本地AI合作伙伴而被迫在中国市场暂时禁用该功能。",
        "source": "TechCrunch/Bloomberg",
        "url": "https://techcrunch.com/2026/07/16/apple-intelligence-approved-for-launch-in-china-with-alibabas-qwen-ai/",
        "keywords": ["Apple Intelligence", "阿里巴巴", "Qwen", "中国审批", "百度"],
        "original_language": "zh"
    },
    {
        "id": "ait-14",
        "date": "2026-07-19",
        "category": "ai_tech",
        "title": "OpenAI首个硬件设备曝光：Jony Ive设计的无屏智能音箱",
        "raw_summary": "据彭博社记者Mark Gurman报道，OpenAI的首款消费级硬件设备将是一款由Jony Ive参与设计的无屏幕智能音箱。该设备没有显示屏，可在家中各个房间之间移动，核心特色是AI的'个性'和与用户的连接能力。OpenAI计划在2026年底首次展示该设备，2027年正式发售，定价约200美元。这标志着OpenAI从纯软件公司向硬件领域的首次重大拓展。",
        "source": "Bloomberg/TechCrunch",
        "url": "https://techcrunch.com/2026/07/14/openais-first-hardware-device-is-reportedly-a-screenless-speaker-that-can-move/",
        "keywords": ["OpenAI", "Jony Ive", "智能音箱", "硬件", "无屏设备"],
        "original_language": "zh"
    },
    {
        "id": "ait-15",
        "date": "2026-07-18",
        "category": "ai_tech",
        "title": "Cars24使用OpenAI语音和聊天Agent处理每月超100万次对话",
        "raw_summary": "印度二手车交易平台Cars24宣布已部署OpenAI驱动的语音和聊天Agent，每月处理超过100万次对话。这些Agent覆盖了购车、售车、融资、跟进和客户支持等关键环节，帮助公司挽回了12%的流失客户线索。这是AI Agent在传统行业中规模化应用的典型案例，展示了AI在复杂业务流程中的实际ROI。该案例于7月16日由OpenAI官方发布。",
        "source": "OpenAI/Creati.ai",
        "url": "https://openai.com/index/cars24/",
        "keywords": ["Cars24", "OpenAI", "语音Agent", "印度", "商业应用"],
        "original_language": "zh"
    },
    {
        "id": "ait-16",
        "date": "2026-07-17",
        "category": "ai_tech",
        "title": "Anthropic CEO警告：AI将在2026-2027年匹配'天才之国'",
        "raw_summary": "Anthropic CEO Dario Amodei在7月17日的演讲中发出警告，称AI系统的整体能力有望在2026至2027年间达到甚至超越'天才之国'（nation of geniuses）的水平——即整个国家的人口智力总和。这一预测标志着AI能力评估框架的重大转变，从单一模型能力转向整体社会影响力的衡量。Amodei同时强调需要建立相应的治理框架来应对这一变革。",
        "source": "VentureBeat",
        "url": "https://venturebeat.com/ai/anthropic-ceo-dario-amodei-warns-ai-will-match-country-of-geniuses-by-2026",
        "keywords": ["Anthropic", "Dario Amodei", "AI能力", "治理", "预测"],
        "original_language": "zh"
    },
    {
        "id": "ait-17",
        "date": "2026-07-16",
        "category": "ai_tech",
        "title": "LM Studio发布Bionic：面向开源模型的独立AI编程Agent",
        "raw_summary": "LM Studio于7月16日发布Bionic，这是一款专为开源模型打造的独立AI编程Agent应用。与Claude Code或Cursor不同，Bionic默认在本地运行——代码不会离开用户机器，但可以切换到云端模型处理更重的任务。Bionic提供'代码项目'（支持仓库级别的内联diff和智能搜索）和'工作项目'（处理文档、PDF、演示文稿和电子表格）两种模式。LM Studio承诺Zero Data Retention保证，为注重隐私的开发者提供了新的选择。",
        "source": "9to5Mac/LM Studio",
        "url": "https://9to5mac.com/2026/07/16/lm-studio-expands-beyond-chat-with-bionic-a-new-ai-agent-app-for-open-models/",
        "keywords": ["LM Studio", "Bionic", "开源模型", "AI编程", "隐私"],
        "original_language": "zh"
    },
    {
        "id": "ait-18",
        "date": "2026-07-17",
        "category": "ai_tech",
        "title": "Z.ai发布GLM-5.2：中国MIT许可AI模型挑战美国巨头",
        "raw_summary": "中国AI初创公司Z.ai发布的GLM-5.2模型在Artificial Analysis Intelligence Index v4.1中排名第四，超越了MiniMax-M3和DeepSeek V4 Pro等美国系统。该模型采用MIT许可证开源，无任何地区限制，拥有100万token上下文窗口（是其前代的5倍），在三个长程编程基准测试中均为开源模型之首。该模型定价低廉，被认为是给DeepSeek带来的'既视感'——以极低价格提供接近闭源模型的性能。",
        "source": "ChinaTechNews/Yahoo Finance",
        "url": "https://www.chinatechnews.com/2026/07/02/124817-chinese-ai-model-glm-5-2-poses-challenge-to-anthropic-and-openai",
        "keywords": ["Z.ai", "GLM-5.2", "MIT许可", "开源", "中国AI"],
        "original_language": "zh"
    },
    {
        "id": "ait-19",
        "date": "2026-07-17",
        "category": "ai_tech",
        "title": "CuspAI发布AI材料工厂：NVIDIA、Meta等45家企业共建材料发现网络",
        "raw_summary": "英国AI材料发现初创公司CuspAI于7月16日发起'AI材料工厂'(AI Materials Foundry)，联合NVIDIA、Meta等45家机构组成全球网络，利用AI加速半导体、清洁能源和先进制造领域的新材料发现。该项目将数据、实验室、算力和科学专业知识整合到一个智能体平台中，设立北美、欧洲和亚太三大区域枢纽。CuspAI声称80%的材料研究目标仍未实现突破，该平台旨在解决这一瓶颈。",
        "source": "BusinessWire/IntelligentCIO",
        "url": "https://www.businesswire.com/news/home/20260716196996/en/CuspAI-Launches-AI-Materials-Foundry-a-Global-Network-to-Accelerate-Breakthrough-Discoveries",
        "keywords": ["CuspAI", "AI材料", "NVIDIA", "Meta", "材料发现"],
        "original_language": "zh"
    },
    {
        "id": "ait-20",
        "date": "2026-07-17",
        "category": "ai_tech",
        "title": "OpenAI广告收入远低于预期，距25亿美元目标差距巨大",
        "raw_summary": "据Blogs Grocliq报道，2026年OpenAI的广告收入预计将远低于其25亿美元的年度目标。根据Emarketer数据，OpenAI、微软、Google和Amazon四家的AI广告总收入加起来也不到10亿美元。OpenAI此前曾宣称其AI广告收入alone将达到25亿美元，但实际进展缓慢。这一差距引发了投资者对OpenAI商业模式可持续性的担忧，尤其是在竞争日益激烈的AI市场中。",
        "source": "Blogs Grocliq/Emarketer",
        "url": "https://blogs.grocliq.com/2026/07/20/openai-appears-to-be-missing-its-sales-goals-by-a-vast-margin/",
        "keywords": ["OpenAI", "广告收入", "商业模式", "投资者", "竞争"],
        "original_language": "zh"
    },
    {
        "id": "ait-21",
        "date": "2026-07-16",
        "category": "ai_tech",
        "title": "Samsung UFS 5.0发布：业界最快存储方案支持端侧AI",
        "raw_summary": "三星电子于7月8日在其全球新闻室发布了业界最快的UFS 5.0存储解决方案，数据传输速度高达10.8GB/s，专为下一代端侧AI应用设计。该存储方案将显著提升智能手机和边缘设备的AI推理速度，使更复杂的本地AI模型能够在设备上运行而无需依赖云端。这是AI硬件基础设施领域的重要进展，与端侧AI模型（如Bonsai 27B）的发展形成互补。",
        "source": "Samsung Semiconductor",
        "url": "https://news.samsungsemiconductor.com/global/",
        "keywords": ["三星", "UFS 5.0", "端侧AI", "存储", "AI硬件"],
        "original_language": "zh"
    },
    # --- STARTUPS ---
    {
        "id": "st-6",
        "date": "2026-07-20",
        "category": "startup",
        "title": "CuspAI完成4.5亿美元B轮融资，估值26亿美元",
        "raw_summary": "剑桥AI材料发现初创公司CuspAI于7月20日宣布完成4.5亿美元Series B融资，估值达26亿美元。本轮由Kleiner Perkins和NEA领投，Jeff Bezos通过Bezos Expeditions跟投，英国政府主权AI基金也参与其中。CuspAI成立于两年前，专注于利用AI加速半导体和清洁能源领域的新材料发现。该公司同时启动了与NVIDIA、Meta等45家企业的AI材料工厂合作。",
        "source": "Bloomberg/Guardian/CNBC",
        "url": "https://www.bloomberg.com/news/articles/2026-07-20/bezos-backs-startup-focused-on-material-discovery-for-chipmaking",
        "keywords": ["CuspAI", "B轮", "Jeff Bezos", "材料发现", "NVIDIA"],
        "original_language": "zh"
    },
    {
        "id": "st-7",
        "date": "2026-07-20",
        "category": "startup",
        "title": "李开复01.ai筹备2027年香港IPO，目标成为AI 2.0单季盈利企业",
        "raw_summary": "李开复创办的中国AI公司01.ai于7月20日宣布正在推进2027年香港IPO计划。公司正在拆除红筹结构（中国企业常见的离岸上市架构），并目标在明年实现单季度盈利。李开复表示01.ai将成为中国首家AI 2.0公司实现盈利。此前01.ai已停止预训练路线，转而专注于推理和应用层AI。",
        "source": "Bloomberg/TestingCatalog",
        "url": "https://www.bloomberg.com/news/articles/2026-07-20/ai-pioneer-kai-fu-lee-s-startup-targets-hong-kong-ipo-next-year",
        "keywords": ["01.ai", "李开复", "香港IPO", "AI 2.0", "盈利"],
        "original_language": "zh"
    },
    # --- PRODUCT/TOOL ---
    {
        "id": "pt-7",
        "date": "2026-07-16",
        "category": "product_tool",
        "title": "LM Studio Bionic：本地优先的开源AI编程Agent工具",
        "raw_summary": "LM Studio于7月16日发布Bionic，一款专为开源模型打造的独立AI编程Agent应用。Bionic提供两种项目模式：代码项目（支持仓库级别的内联diff编辑和智能搜索）和工作项目（处理文档、PDF、演示文稿和电子表格）。默认本地运行确保代码不离开用户机器，同时可无缝切换到云端模型处理重型任务。LM Studio承诺Zero Data Retention，为注重隐私的开发者提供了Cursor和Claude Code之外的替代选择。",
        "source": "9to5Mac/LM Studio",
        "url": "https://9to5mac.com/2026/07/16/lm-studio-expands-beyond-chat-with-bionic-a-new-ai-agent-app-for-open-models/",
        "keywords": ["LM Studio", "Bionic", "AI编程Agent", "开源", "隐私"],
        "original_language": "zh"
    },
    {
        "id": "pt-8",
        "date": "2026-07-20",
        "category": "product_tool",
        "title": "AI Weekly News：每日AI新闻聚合工具更新",
        "raw_summary": "AI Weekly于7月21日发布最新一期AI新闻汇总，覆盖了过去一周最重要的AI行业动态，包括Kimi K3服务器过载、Apple Intelligence中国获批、OpenAI智能音箱硬件计划等。该工具追踪113个AI实体，每日精选顶级AI故事并提供现场更新，是AI从业者获取行业全景的高效工具。",
        "source": "AI Weekly",
        "url": "https://aiweekly.co/ai-news-today",
        "keywords": ["AI Weekly", "新闻聚合", "AI动态", "行业追踪"],
        "original_language": "zh"
    },
]

# ── Read existing data ────────────────────────────────────────────────
base_ids = set()
if DATA_FILE.exists():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        base_data = json.load(f)
    base_ids = {item["id"] for item in base_data}
else:
    base_data = []

# ── Deduplicate and merge ────────────────────────────────────────────
merged = list(base_data)
new_count = 0
for item in new_data:
    if item["id"] not in base_ids:
        merged.insert(0, item)  # prepend
        new_count += 1
    else:
        print(f"  SKIP duplicate: {item['id']}")

# ── Sort by date descending ──────────────────────────────────────────
merged.sort(key=lambda x: x["date"], reverse=True)

# ── Validate ─────────────────────────────────────────────────────────
required_fields = ["id", "date", "category", "title", "raw_summary", "source", "url", "keywords", "original_language"]
valid_categories = {"ai_tech", "startup", "product_tool"}
seen_ids = set()
errors = []

for i, item in enumerate(merged):
    for field in required_fields:
        if field not in item:
            errors.append(f"Item {i}: missing field '{field}'")
    if item.get("category") not in valid_categories:
        errors.append(f"Item {i}: invalid category '{item.get('category')}'")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", item.get("date", "")):
        errors.append(f"Item {i}: invalid date format '{item.get('date')}'")
    if item["id"] in seen_ids:
        errors.append(f"Item {i}: duplicate id '{item['id']}'")
    seen_ids.add(item["id"])

if errors:
    print("VALIDATION ERRORS:")
    for e in errors:
        print(f"  {e}")
else:
    print("Validation PASSED.")

# ── Write ────────────────────────────────────────────────────────────
DATA_DIR.mkdir(parents=True, exist_ok=True)
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"\nWrote {len(merged)} total records ({new_count} new) to {DATA_FILE}")

# Print summary
cats = {}
dates = {}
for item in merged:
    cats[item["category"]] = cats.get(item["category"], 0) + 1
    dates[item["date"]] = dates.get(item["date"], 0) + 1

print("\nBy category:")
for k, v in sorted(cats.items()):
    print(f"  {k}: {v}")
print("\nBy date:")
for k, v in sorted(dates.items(), reverse=True):
    print(f"  {k}: {v}")
