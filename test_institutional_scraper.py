#!/usr/bin/env python3
"""
Test scraper for institutional job portals
ETH Zurich, Fraunhofer, Max Planck
"""

import requests
from bs4 import BeautifulSoup
import re

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

ROLE_KEYWORDS = [
    "business development", "tech transfer", "innovation manager",
    "licensing", "exploitation", "partnership", "commercialization",
    "knowledge transfer", "valorisation", "market development",
    "bd manager", "commercial", "ecosystem"
]

def test_eth_zurich():
    print("\n=== ETH ZURICH ===")
    queries = ["business development", "tech transfer", "innovation"]
    for q in queries:
        try:
            url = f"https://jobs.ethz.ch/job/search?q={requests.utils.quote(q)}"
            r = requests.get(url, headers=HEADERS, timeout=10)
            print(f"Status {q}: {r.status_code}")
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Try different selectors
            jobs = soup.find_all(["div", "li", "article", "tr"], class_=re.compile("job|result|item|row|listing"))
            print(f"Cards found with class: {len(jobs)}")
            
            # Also try links
            links = soup.find_all("a", href=re.compile("/job/"))
            print(f"Job links found: {len(links)}")
            for link in links[:5]:
                print(f"  - {link.get_text(strip=True)} | {link['href']}")
                
        except Exception as e:
            print(f"ETH error ({q}): {e}")


def test_fraunhofer():
    print("\n=== FRAUNHOFER ===")
    queries = ["business development", "tech transfer", "innovation"]
    for q in queries:
        try:
            url = f"https://jobs.fraunhofer.de/suche?q={requests.utils.quote(q)}"
            r = requests.get(url, headers=HEADERS, timeout=10)
            print(f"Status {q}: {r.status_code}")
            soup = BeautifulSoup(r.text, "html.parser")
            
            jobs = soup.find_all(["div", "li", "article"], class_=re.compile("job|result|item|listing|card"))
            print(f"Cards found with class: {len(jobs)}")
            
            links = soup.find_all("a", href=re.compile("/job|/stelle|/position"))
            print(f"Job links found: {len(links)}")
            for link in links[:5]:
                print(f"  - {link.get_text(strip=True)} | {link['href']}")
                
        except Exception as e:
            print(f"Fraunhofer error ({q}): {e}")


def test_max_planck():
    print("\n=== MAX PLANCK ===")
    queries = ["business development", "tech transfer", "innovation"]
    for q in queries:
        try:
            url = f"https://www.mpg.de/jobboard?search={requests.utils.quote(q)}"
            r = requests.get(url, headers=HEADERS, timeout=10)
            print(f"Status {q}: {r.status_code}")
            soup = BeautifulSoup(r.text, "html.parser")
            
            jobs = soup.find_all(["div", "li", "article"], class_=re.compile("job|result|item|listing|card"))
            print(f"Cards found with class: {len(jobs)}")
            
            links = soup.find_all("a", href=re.compile("/job|/position|/stelle|/career"))
            print(f"Job links found: {len(links)}")
            for link in links[:5]:
                print(f"  - {link.get_text(strip=True)} | {link['href']}")
                
        except Exception as e:
            print(f"Max Planck error ({q}): {e}")


if __name__ == "__main__":
    print("Testing institutional job portals...")
    test_eth_zurich()
    test_fraunhofer()
    test_max_planck()
    print("\nDone!")
