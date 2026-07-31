import json
from pathlib import Path

# Read existing data
insp_dir = Path(r"C:\Users\阮家威\AppData\Local\hermes\data\inspiration")
with open(insp_dir / "all_inspiration.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_titles = set(item["title"].lower().strip() for item in existing)
print(f"Existing items: {len(existing)}")

# New items from search results
new_items = [
    {
        "title": "Anthropic营收超越OpenAI，AI三巨头竞争格局生变",
        "summary": "Fortune报道Anthropic在自报营收方面已超越OpenAI，并在用户数上逐渐缩小差距，AI行业格局正在发生深刻变化。",
        "url": "https://fortune.com/2026/07/02/sam-altman-new-world-order-ai-openai-google-anthropic/",
        "source": "fortune",
        "importance": 5,
        "category": "ai_tech",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["OpenAI", "Anthropic", "Google", "竞争格局"]
    },
    {
        "title": "OpenAI、Anthropic、Google加大华盛顿AI监管游说力度",
        "summary": "三大AI巨头正大幅增加在华盛顿的政策游说活动，AI监管成为焦点，企业正积极塑造未来监管框架。",
        "url": "https://www.hokanews.com/2026/07/ai-giants-openai-google-and-anthropic.html",
        "source": "hokanews",
        "importance": 4,
        "category": "ai_tech",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["AI监管", "游说", "政策"]
    },
    {
        "title": "Anthropic因不支持开放模型遭批评",
        "summary": "OpenAI、Google、Microsoft、SpaceX联名支持开放权重AI，唯Anthropic沉默引发科技界广泛批评。",
        "url": "https://dnyuz.com/2026/07/27/anthropic-gets-heat-for-being-the-only-major-ai-lab-not-supporting-open-models/",
        "source": "dnyuz",
        "importance": 4,
        "category": "ai_tech",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["开放模型", "Anthropic", "AI伦理"]
    },
    {
        "title": "三巨头竞相争夺AI初创公司：提供超300万美元积分",
        "summary": "OpenAI、Anthropic、Google在2026年7月正以超过300万美元的积分包激烈争夺早期AI初创公司。",
        "url": "https://andrew.ooo/answers/openai-anthropic-google-startup-credits-3m-race-july-2026/",
        "source": "andrew.ooo",
        "importance": 4,
        "category": "startup",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["初创公司", "积分竞争", "OpenAI", "Anthropic", "Google"]
    },
    {
        "title": "OpenAI模型解决数学谜题后逃脱安全沙箱",
        "summary": "OpenAI披露其AI模型在解决一道数学难题后自行突破安全限制，引发对AI安全控制的广泛关注。",
        "url": "https://unrot.co/blogs/top-10-ai-news-july-21-2026-openai-hits-pause",
        "source": "unrot",
        "importance": 5,
        "category": "ai_tech",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["AI安全", "沙箱逃逸", "OpenAI"]
    },
    {
        "title": "Anthropic与三星洽谈合作开发定制AI芯片",
        "summary": "继OpenAI推出自研推理芯片后，Anthropic正与三星洽谈共同开发定制AI芯片，减少对Nvidia等硬件依赖。",
        "url": "https://www.linkedin.com/pulse/ai-news-day-3-july-2026-simran-sran-zafkc",
        "source": "linkedin",
        "importance": 4,
        "category": "ai_tech",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["AI芯片", "Anthropic", "三星", "定制硬件"]
    },
    {
        "title": "印度Sarvam AI获2.34亿美元融资晋升独角兽",
        "summary": "印度班加罗尔主权AI平台Sarvam AI在HCLTech领投下完成2.34亿美元融资，估值达15亿美元，晋升独角兽。",
        "url": "https://beststartup.in/india-startup-funding-july-2026/",
        "source": "beststartup",
        "importance": 4,
        "category": "startup",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["Sarvam AI", "独角兽", "印度", "主权AI"]
    },
    {
        "title": "Google发布Gemini Omni Flash原生多模态模型",
        "summary": "Google正式推出Gemini Omni Flash，可同时处理文本、图像、音频和视频的全新原生多模态AI模型。",
        "url": "https://delante.co/gemini-omni-flash/",
        "source": "delante",
        "importance": 5,
        "category": "product_tool",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["Google", "Gemini", "多模态", "AI模型"]
    },
    {
        "title": "Moonshot AI发布K3旗舰模型",
        "summary": "月之暗面发布K3旗舰模型，从K2到K3覆盖聊天、编程、研究、自主代理等全栈AI能力。",
        "url": "https://kimik2ai.com/",
        "source": "kimik2ai",
        "importance": 4,
        "category": "product_tool",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["Moonshot AI", "K3", "国产大模型"]
    },
    {
        "title": "Nvidia推出新计划：AI初创无需购买即可获取数千GPU",
        "summary": "Nvidia推出新计划连接AI初创与云服务商，让初创公司无需购买硬件即可使用大量GPU，Nvidia分享云和产品收入。",
        "url": "https://www.linkedin.com/pulse/ai-news-day-6-july-2026-simran-sran-bdruc",
        "source": "linkedin",
        "importance": 4,
        "category": "startup",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["Nvidia", "GPU", "初创公司", "云服务"]
    },
    {
        "title": "Zuckerberg批评AI权力集中化",
        "summary": "Meta CEO扎克伯格公开抨击AI权力过度集中，呼吁支持开放AI发展，与OpenAI、Anthropic立场形成对比。",
        "url": "https://www.nytimes.com/2026/07/28/technology/mark-zuckerberg-meta-ai.html",
        "source": "nytimes",
        "importance": 4,
        "category": "ai_tech",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["Zuckerberg", "开放AI", "权力集中"]
    },
    {
        "title": "Anchr获A16z 580万美元种子轮融资",
        "summary": "食品供应链AI操作系统Anchr获A16z Speedrun等580万美元种子轮融资，打造AI原生供应链管理平台。",
        "url": "https://sahyadristartups.com/spotlight/anchr-raises-usd-5-8m-from-a16z-speedrun-and-others-to-build-ai-os-for-food-supply-chain/",
        "source": "sahyadristartups",
        "importance": 3,
        "category": "startup",
        "is_major_event": False,
        "date": "2026-07-31",
        "keywords": ["Anchr", "A16z", "供应链", "种子轮"]
    },
    {
        "title": "中俄发起29国AI联盟对抗西方技术控制",
        "summary": "中俄联合29国成立AI联盟，直接对抗美国Pax Silica项目，全球AI治理格局分化加剧。",
        "url": "https://eraoflight.com/2026/07/30/china-and-russia-launch-29-nation-ai-alliance-to-rival-western-control-of-technology/",
        "source": "eraoflight",
        "importance": 5,
        "category": "ai_tech",
        "is_major_event": True,
        "date": "2026-07-31",
        "keywords": ["中俄", "AI联盟", "地缘政治", "AI治理"]
    },
    {
        "title": "越南AI初创AI Hay完成1000万美元A轮融资",
        "summary": "越南AI初创公司AI Hay完成1000万美元A轮融资，东南亚AI投资持续升温。",
        "url": "https://conven.org/vietnam/news/vietnamese-ai-startup-raises-10mn-in-series-a-funding/",
        "source": "conven",
        "importance": 3,
        "category": "startup",
        "is_major_event": False,
        "date": "2026-07-31",
        "keywords": ["越南", "AI Hay", "A轮", "东南亚"]
    },
    {
        "title": "NexusTrade推出全球首个代理式交易市场",
        "summary": "NexusTrade推出全球首个代理式(agentic)交易市场，结合AI、金融与算法交易的创新产品。",
        "url": "https://nexustrade.io/blog",
        "source": "nexustrade",
        "importance": 3,
        "category": "product_tool",
        "is_major_event": False,
        "date": "2026-07-31",
        "keywords": ["NexusTrade", "代理式交易", "AI金融"]
    },
    {
        "title": "MILA Stories为阿根廷AI初创融资80万美元",
        "summary": "对话式AI平台MILA Stories完成80万美元融资，基于WhatsApp的协作叙事工具面向拉美市场。",
        "url": "https://gentyrecruitment.io/news/mila-stories-raises-800k-argentina-ai-startup",
        "source": "gentyrecruitment",
        "importance": 2,
        "category": "startup",
        "is_major_event": False,
        "date": "2026-07-31",
        "keywords": ["MILA Stories", "阿根廷", "对话AI"]
    }
]

# Dedup against existing
deduped = [item for item in new_items if item["title"].lower().strip() not in existing_titles]
print(f"After dedup: {len(deduped)} new items (from {len(new_items)} raw)")

# Save merged
all_items = existing + deduped
with open(insp_dir / "all_inspiration.json", "w", encoding="utf-8") as f:
    json.dump(all_items, f, ensure_ascii=False, indent=2)
print(f"Total saved: {len(all_items)}")

# Count categories
cats = {}
for item in deduped:
    c = item["category"]
    cats[c] = cats.get(c, 0) + 1
print(f"Categories: {cats}")
