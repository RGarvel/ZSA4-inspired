#!/usr/bin/env python3
"""Collect latest arXiv papers from cs.AI, cs.LG, cs.CL categories."""
import json, urllib.request, xml.etree.ElementTree as ET, sys

DATA_DIR = r"C:\Users\阮家威\AppData\Local\hermes\data\inspiration\data"
TODAY = "2026-07-23"
BASE_URL = "https://export.arxiv.org/api/query"

categories = ["cs.AI", "cs.LG", "cs.CL"]
all_papers = []

for cat in categories:
    query = f"search_query=cat:{cat}&sortBy=submittedDate&sortOrder=descending&max_results=15"
    url = BASE_URL + "?" + query
    req = urllib.request.Request(url, headers={"User-Agent": "BlogWatcher/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        xml = resp.read().decode("utf-8")
    
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml)
    
    for entry in root.findall("a:entry", ns):
        title = entry.find("a:title", ns).text.strip().replace("\n", " ")
        arxiv_id = entry.find("a:id", ns).text.strip().split("/abs/")[-1]
        published = entry.find("a:published", ns).text[:10]
        summary = entry.find("a:summary", ns).text.strip()[:500].replace("\n", " ")
        cats = [c.get("term") for c in entry.findall("a:category", ns)]
        authors_entries = entry.findall("a:author", ns)
        authors = ", ".join(a.find("a:name", ns).text for a in authors_entries[:5])
        
        all_papers.append({
            "arxiv_id": arxiv_id,
            "title": title,
            "published": published,
            "authors": authors,
            "summary": summary,
            "categories": cats
        })

tmp_path = f"{DATA_DIR}/temp_arxiv_{TODAY}.json"
with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(all_papers, f, indent=2, ensure_ascii=False)

print(f"Fetched {len(all_papers)} papers from arXiv")
for p in all_papers[:5]:
    print(f"  - [{p['arxiv_id']}] {p['title'][:80]}")
print(f"Saved to {tmp_path}")
