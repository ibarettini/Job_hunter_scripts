#!/usr/bin/env python3
"""
Test scraper for ETH Zurich - production ready version
"""

import requests
from bs4 import BeautifulSoup
import re

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

ROLE_KEYWORDS = [
    "business development", "tech transfer", "innovation manager",
    "licensing", "exploitation", "partnership", "commercialization",
    "knowledge transfer", "valorisation", "market development",
    "bd manager", "commercial", "ecosystem", "ip manager",
]

EXCLUDE_KEYWORDS = [
    "phd", "postdoc", "research scientist", "software engineer",
    "hardware engineer", "lab technician", "internship", "professor",
    "assistant professor", "group leader", "postdoctoral"
]

def fetch_eth_zurich():
    jobs = []
    try:
        url = "https://jobs.ethz.ch/site/index"
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"ETH Zurich status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        
        all_links = soup.find_all("a", href=True)
        job_links = [l for l in all_links if "/job/view/" in l.get('href', '')]
        print(f"Total job links found: {len(job_links)}")
        
        for link in job_links:
            title = link.get_text(strip=True)
            # Clean up title (remove location/date info after the job title)
            title_clean = title.split("100%")[0].split("80%")[0].split("60%")[0].strip()
            href = link['href']
            full_url = f"https://jobs.ethz.ch{href}" if href.startswith('/') else href
            
            jobs.append({
                "title": title_clean,
                "company": "ETH Zurich",
                "location": "Zurich, Switzerland",
                "url": full_url,
                "source": "ETH Zurich"
            })
            
    except Exception as e:
        print(f"ETH Zurich error: {e}")
    return jobs


def is_relevant(job):
    text = job['title'].lower()
    
    for kw in EXCLUDE_KEYWORDS:
        if kw in text:
            return False
    
    has_role = any(kw in text for kw in ROLE_KEYWORDS)
    return has_role


if __name__ == "__main__":
    print("Testing ETH Zurich scraper...")
    jobs = fetch_eth_zurich()
    print(f"\nAll jobs found: {len(jobs)}")
    
    relevant = [j for j in jobs if is_relevant(j)]
    print(f"Relevant jobs after filtering: {len(relevant)}")
    
    if relevant:
        print("\nRelevant positions:")
        for j in relevant:
            print(f"  -> {j['title']}")
            print(f"     {j['url']}")
    else:
        print("\nNo relevant positions today.")
        print("\nSample of all positions (first 10):")
        for j in jobs[:10]:
            print(f"  -> {j['title']}")
    
    print("\nDone!")
