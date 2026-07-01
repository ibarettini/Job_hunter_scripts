#!/usr/bin/env python3
"""
Test scraper v7 - CIC Nanogune and DIPC/CFM
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
    "chief of staff", "director", "manager", "head of",
    "project manager", "sales", "transferencia", "desarrollo de negocio",
    "gestor", "responsable", "innovacion",
]

EXCLUDE_KEYWORDS = [
    "phd", "postdoc", "research scientist", "software engineer",
    "hardware engineer", "lab technician", "internship", "professor",
    "postdoctoral", "becario", "undergraduate", "student",
    "investigador", "físico", "beca",
]

def test_portal_generic(name, urls):
    print(f"\n=== {name.upper()} ===")
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            print(f"\nURL: {url}")
            print(f"Status: {r.status_code}")
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                title = soup.find("title")
                print(f"Page title: {title.get_text(strip=True)[:80] if title else 'N/A'}")
                
                all_links = soup.find_all("a", href=True)
                print(f"Total links: {len(all_links)}")
                
                # Job links with numeric IDs or job patterns
                job_links = [l for l in all_links if re.search(
                    r'\d{4,}|/job/|/vacancy/|/oferta|/empleo|/position|/career|/opening',
                    l.get('href', ''), re.I)]
                print(f"Job-related links: {len(job_links)}")
                for l in job_links[:8]:
                    print(f"  -> {l.get_text(strip=True)[:80]} | {l['href']}")

                # Relevant links by keyword
                relevant = [l for l in all_links
                            if any(kw in l.get_text(strip=True).lower() for kw in ROLE_KEYWORDS)
                            and not any(kw in l.get_text(strip=True).lower() for kw in EXCLUDE_KEYWORDS)
                            and len(l.get_text(strip=True)) > 10]
                print(f"Relevant by keyword: {len(relevant)}")
                for l in relevant[:8]:
                    print(f"  -> {l.get_text(strip=True)[:80]} | {l['href']}")

                # Headings
                for tag in ["h2", "h3", "h4"]:
                    headings = soup.find_all(tag)
                    if headings and len(headings) < 20:
                        print(f"{tag} headings ({len(headings)}):")
                        for h in headings[:6]:
                            print(f"  -> {h.get_text(strip=True)[:80]}")
                break  # Stop at first successful URL
                            
        except Exception as e:
            print(f"{name} error ({url}): {e}")


if __name__ == "__main__":
    print("Testing CIC Nanogune and DIPC/CFM...")

    test_portal_generic("CIC NANOGUNE", [
        "https://nanogune.eu/en/working-with-us/job-offers",
        "https://nanogune.eu/en/careers",
        "https://nanogune.eu/en/working-with-us",
        "https://www.nanogune.eu/jobs",
    ])

    test_portal_generic("DIPC / CFM", [
        "https://dipc.ehu.es/en/jobs",
        "https://dipc.ehu.es/en/careers",
        "https://cfm.ehu.es/en/jobs",
        "https://www.cfm.ehu.es/en/working-with-us",
    ])

    print("\nDone!")
