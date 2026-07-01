#!/usr/bin/env python3
"""
Test scraper for institutional job portals v4
Tecnalia, BSC, QuTech/TU Delft, VTT, Quantum ADA Andalucia, imec
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
    "project manager", "transferencia", "desarrollo de negocio",
    "innovacion", "gestor", "responsable comercial",
]

EXCLUDE_KEYWORDS = [
    "phd", "postdoc", "research scientist", "software engineer",
    "hardware engineer", "lab technician", "internship", "professor",
    "assistant professor", "group leader", "postdoctoral", "becario",
    "investigador", "físico", "engineer"
]

def test_portal(name, url, job_link_pattern=None, title_tags=None):
    print(f"\n=== {name.upper()} ===")
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.find("title")
        print(f"Page title: {title.get_text(strip=True)[:80] if title else 'N/A'}")

        all_links = soup.find_all("a", href=True)
        print(f"Total links: {len(all_links)}")

        if job_link_pattern:
            job_links = [l for l in all_links if re.search(job_link_pattern, l.get('href', ''), re.I)]
            print(f"Job links ({job_link_pattern}): {len(job_links)}")
            for l in job_links[:8]:
                print(f"  -> {l.get_text(strip=True)[:80]} | {l['href']}")
        
        # Also try numeric ID pattern
        numeric_links = [l for l in all_links if re.search(r'\d{4,}', l.get('href', ''))]
        if numeric_links:
            print(f"Links with numeric IDs: {len(numeric_links)}")
            for l in numeric_links[:5]:
                print(f"  -> {l.get_text(strip=True)[:80]} | {l['href']}")

        # Try headings
        for tag in ["h2", "h3", "h4"]:
            headings = soup.find_all(tag)
            if headings and len(headings) < 30:
                print(f"{tag} headings ({len(headings)}):")
                for h in headings[:5]:
                    print(f"  -> {h.get_text(strip=True)[:80]}")

    except Exception as e:
        print(f"{name} error: {e}")


if __name__ == "__main__":
    print("Testing institutional job portals v4...")

    test_portal(
        "TECNALIA",
        "https://www.tecnalia.com/trabaja-con-nosotros",
        job_link_pattern=r'/empleo|/job|/oferta|/vacante|/trabaja'
    )

    test_portal(
        "BSC Barcelona Supercomputing Center",
        "https://www.bsc.es/join-us/job-opportunities",
        job_link_pattern=r'/job|/position|/vacancy|/offer'
    )

    test_portal(
        "QuTech / TU Delft",
        "https://qutech.nl/jobs/",
        job_link_pattern=r'/job|/vacancy|/position|/career'
    )

    test_portal(
        "VTT Finland",
        "https://www.vttresearch.com/en/careers/open-positions",
        job_link_pattern=r'/job|/position|/vacancy|/career|/open'
    )

    test_portal(
        "Quantum ADA Andalucia",
        "https://www.juntadeandalucia.es/organismos/ada/areas/inteligencia-artificial/quantumada.html",
        job_link_pattern=r'/empleo|/job|/oferta|/vacante|/convocatoria'
    )

    test_portal(
        "imec Belgium",
        "https://www.imec-int.com/en/careers/job-opportunities",
        job_link_pattern=r'/job|/vacancy|/position|/career|/opportunity'
    )

    print("\nDone!")
