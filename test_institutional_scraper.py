#!/usr/bin/env python3
"""
Test scraper for institutional job portals v2
ETH Zurich, Fraunhofer, Max Planck
"""

import requests
from bs4 import BeautifulSoup
import re

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def test_eth_zurich():
    print("\n=== ETH ZURICH ===")
    queries = ["business development", "tech transfer", "innovation"]
    for q in queries:
        try:
            url = f"https://jobs.ethz.ch/job/search?q={requests.utils.quote(q)}"
            r = requests.get(url, headers=HEADERS, timeout=10)
            print(f"Status '{q}': {r.status_code}")
            soup = BeautifulSoup(r.text, "html.parser")

            # Try different selectors
            for selector in ["job", "result", "item", "listing", "card", "position"]:
                cards = soup.find_all(["div", "li", "article"], class_=re.compile(selector))
                if cards:
                    print(f"  Cards with '{selector}': {len(cards)}")
                    for card in cards[:3]:
                        title = card.find(["h2", "h3", "h4", "a"])
                        if title:
                            print(f"    -> {title.get_text(strip=True)}")

            links = soup.find_all("a", href=re.compile("/job/|/position/|/vacancy/"))
            print(f"  Job links: {len(links)}")
            for link in links[:5]:
                print(f"    -> {link.get_text(strip=True)} | {link['href']}")

        except Exception as e:
            print(f"ETH error ({q}): {e}")


def test_fraunhofer():
    print("\n=== FRAUNHOFER ===")
    queries = ["business development", "tech transfer", "innovation"]
    for q in queries:
        try:
            url = f"https://jobs.fraunhofer.de/?locale=en_US&q={requests.utils.quote(q)}"
            r = requests.get(url, headers=HEADERS, timeout=10)
            print(f"Status '{q}': {r.status_code}")
            soup = BeautifulSoup(r.text, "html.parser")

            for selector in ["job", "result", "item", "listing", "card", "position", "vacancy"]:
                cards = soup.find_all(["div", "li", "article"], class_=re.compile(selector))
                if cards:
                    print(f"  Cards with '{selector}': {len(cards)}")
                    for card in cards[:3]:
                        title = card.find(["h2", "h3", "h4", "a"])
                        if title:
                            print(f"    -> {title.get_text(strip=True)}")

            # Look for job-specific links (not navigation)
            links = soup.find_all("a", href=True)
            job_links = [l for l in links if re.search(r'/job/\d+|/stelle/\d+|/position/\d+', l.get('href', ''))]
            print(f"  Job links: {len(job_links)}")
            for link in job_links[:5]:
                print(f"    -> {link.get_text(strip=True)} | {link['href']}")

        except Exception as e:
            print(f"Fraunhofer error ({q}): {e}")


def test_max_planck():
    print("\n=== MAX PLANCK ===")
    queries = ["business development", "tech transfer", "innovation"]
    for q in queries:
        try:
            url = f"https://www.mpg.de/jobboard?search={requests.utils.quote(q)}"
            r = requests.get(url, headers=HEADERS, timeout=10)
            print(f"Status '{q}': {r.status_code}")
            soup = BeautifulSoup(r.text, "html.parser")

            for selector in ["job", "result", "item", "listing", "card", "position", "vacancy", "offer"]:
                cards = soup.find_all(["div", "li", "article"], class_=re.compile(selector))
                if cards:
                    print(f"  Cards with '{selector}': {len(cards)}")
                    for card in cards[:3]:
                        title = card.find(["h2", "h3", "h4", "a"])
                        if title:
                            print(f"    -> {title.get_text(strip=True)}")

            links = soup.find_all("a", href=True)
            job_links = [l for l in links if re.search(r'/job|/stelle|/position|/offer|/vacancy', l.get('href', ''))]
            print(f"  Job links: {len(job_links)}")
            for link in job_links[:5]:
                print(f"    -> {link.get_text(strip=True)} | {link['href']}")

        except Exception as e:
            print(f"Max Planck error ({q}): {e}")


if __name__ == "__main__":
    print("Testing institutional job portals v2...")
    test_eth_zurich()
    test_fraunhofer()
    test_max_planck()
    print("\nDone!")
