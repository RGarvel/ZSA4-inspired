import json
from datetime import datetime

# Read existing inspiration data
with open('all_inspiration.json', 'r', encoding='utf-8') as f:
    existing = json.load(f)

# Read raw data for arxiv papers
with open('temp_raw_data.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

# Get existing titles for dedup
existing_titles = set(item.get('title','').lower().strip() for item in existing)

today = '2026-07-31'
new_items = []

# Search results from web searches (manually captured)
search_data = [
    # AI startup funding search
    {
        "title": "AI Mega-Funding Week July 2026: $5.55B Legal AI, $450M Robotics Debut",
        "url": "https://featureddaily.com/news/ai-mega-funding-week-july-2026-fast-brief",
        "description": "The week of 10 July 2026 delivered a burst of outsized AI rounds — from a $5.55B legal-AI valuation to a $450M robotics debut. The FeaturedDaily Desk·11 July 2026.",
        "category": "startup",
        "importance": 4
    },
    {
        "title": "Sarvam AI Hits Unicorn Status: $234M at $1.5B Valuation Led by HCLTech",
        "url": "https://beststartup.in/india-startup-funding-july-2026/",
        "description": "India startup funding in July 2026 is accelerating. Sarvam AI, the Bengaluru-based sovereign AI platform, has reached unicorn status after closing $234M at a $1.5B valuation in a round led by HCLTech.",
        "category": "startup",
        "importance": 4
    },
    {
        "title": "MILA Stories Raises $800K for Argentina Conversational AI Startup",
        "url": "https://gentyrecruitment.io/news/mila-stories-raises-800k-argentina-ai-startup",
        "description": "Conversational AI platform for WhatsApp-based collaborative storytelling raises seed round. July 25, 2026.",
        "category": "startup",
        "importance": 3
    },
    {
        "title": "Ilya Sutskever's SSI Partners with NVIDIA to Scale AI Research",
        "url": "https://techcrunch.com/2026/07/27/ilya-sutskevers-safe-superintelligence-partners-with-nvidia-to-scale-its-ai-research/",
        "description": "Safe Superintelligence Inc (SSI) partners with NVIDIA to advance compute platforms, leveraging SSI's unique insights into the future of AI. SSI also partnered with Google Cloud last year.",
        "category": "ai_tech",
        "importance": 5
    },
    {
        "title": "Chinese Startup Moonshot Publicly Releases Kimi K3 AI Model Details",
        "url": "https://www.nytimes.com/2026/07/27/business/moonshot-kimi-k3-china-ai.html",
        "description": "Chinese startup Moonshot publicly released the details of its latest AI model Kimi K3 on July 27, showing the world how it was built.",
        "category": "ai_tech",
        "importance": 4
    },
    # New AI product launch search
    {
        "title": "Google Launches Gemini Omni Flash: Natively Multimodal Model for Text, Image, Audio, Video",
        "url": "https://delante.co/gemini-omni-flash/",
        "description": "Google has officially launched Gemini Omni Flash — a groundbreaking, natively multimodal AI model capable of simultaneously processing text, images, audio, and video as cohesive input data.",
        "category": "product_tool",
        "importance": 4
    },
    {
        "title": "Microsoft Introduces MAI-Cyber-1-Flash for Cybersecurity Inside MDASH",
        "url": "https://microsoft.ai/news/introducing-mai-cyber-1-flash-inside-mdash/",
        "description": "Mustafa Suleyman announces MAI-Cyber-1-Flash inside MDASH on July 27, 2026. Progress in AI has been startling and so has the new generation of cyber threats it's unleashing.",
        "category": "product_tool",
        "importance": 4
    },
    {
        "title": "Kimi K3: Moonshot AI's Latest Flagship Model Spanning Chat, Coding, Research, and Agents",
        "url": "https://kimik2ai.com/",
        "description": "Kimi AI is Moonshot AI's platform - a complete ecosystem of models, tools, and agents. The model family runs from K2 (July 2025) through the new K3 flagship (July 2026).",
        "category": "product_tool",
        "importance": 4
    },
    {
        "title": "OpenAI Introduces Presence: New Product Announced July 22, 2026",
        "url": "https://openai.com/",
        "description": "OpenAI introduces Presence, a new product announced on July 22, 2026 by David Vélez and Robin Vince.",
        "category": "product_tool",
        "importance": 4
    },
    {
        "title": "China and Russia Launch 29-Nation AI Alliance to Rival Western Control",
        "url": "https://eraoflight.com/2026/07/30/china-and-russia-launch-29-nation-ai-alliance-to-rival-western-control-of-technology/",
        "description": "Beijing's pitch is a direct answer to Washington's 'Pax Silica' project, unveiled last year to build the global technology supply chain for AI.",
        "category": "ai_tech",
        "importance": 4
    },
    {
        "title": "NVIDIA Launches Initiative Connecting AI Startups with Cloud Providers for GPU Access",
        "url": "https://www.linkedin.com/pulse/ai-news-day-6-july-2026-simran-sran-bdruc",
        "description": "Nvidia launched a new initiative connecting AI startups with cloud providers so they can access thousands of GPUs without purchasing the hardware directly. In return, Nvidia shares in cloud and product revenue.",
        "category": "ai_tech",
        "importance": 4
    },
    {
        "title": "Startup Market Trends July 2026: Early-Stage Market Deceptively Quiet",
        "url": "https://earlyfinder.co/blog/startup-market-trends-july-2026-signals-before-funding-1784786523562",
        "description": "July 2026 scan across 31,000+ companies shows an early-stage market that looks deceptively quiet. Public rounds skew later-stage and concentrated.",
        "category": "startup",
        "importance": 3
    }
]

for item in search_data:
    title = item['title'].strip()
    if title.lower() in existing_titles:
        continue
    
    desc = item.get('description', '')
    summary = desc[:150].strip() if desc else ''
    if len(desc) > 150:
        summary += '...'
    
    new_items.append({
        'title': title,
        'summary': summary,
        'url': item.get('url', ''),
        'source': 'web',
        'importance': item.get('importance', 3),
        'category': item.get('category', 'ai_tech'),
        'is_major_event': item.get('importance', 3) >= 4,
        'date': today,
        'keywords': []
    })
    existing_titles.add(title.lower())

# Add arxiv papers with date today (not already present)
arxiv_papers = raw.get('arxiv_papers', [])
# Deduplicate by URL
existing_urls = set(item.get('url', '') for item in existing)

for item in arxiv_papers:
    url = item.get('url', '').strip()
    if url in existing_urls:
        continue
    title = item.get('title', '').strip()
    if title.lower() in existing_titles:
        continue
    
    desc = item.get('description', '')
    summary = desc[:150].strip() if desc else ''
    if len(desc) > 150:
        summary += '...'
    
    new_items.append({
        'title': title,
        'summary': summary,
        'url': url,
        'source': 'arxiv',
        'importance': item.get('_imp', 3),
        'category': item.get('_cat', 'academic'),
        'is_major_event': False,
        'date': today,
        'keywords': item.get('keywords', [])
    })
    existing_titles.add(title.lower())
    existing_urls.add(url)

# Add new items to existing
existing.extend(new_items)

# Save updated file
with open('all_inspiration.json', 'w', encoding='utf-8') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_items)} new items today")
print(f"Total items now: {len(existing)}")

# Count by category for today
today_items = [item for item in existing if item.get('date') == today]
print(f"\nToday's items: {len(today_items)}")
categories = {}
for item in today_items:
    cat = item.get('category', 'unknown')
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")

# Count major events
major = [item for item in today_items if item.get('is_major_event')]
print(f"\nMajor events today: {len(major)}")
for item in major[:10]:
    print(f"  [{item['importance']}] {item['title']}")
