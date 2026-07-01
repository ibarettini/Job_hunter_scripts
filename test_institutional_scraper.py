#!/usr/bin/env python3
"""
Test scraper institutional v5 - corrected URLs
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
    "transferencia", "desarrollo de negocio", "innovacion",
    "gestor", "responsable comercial", "chief of staff",
    "director", "manager", "head of",
]

EXCLUDE_KEYWORDS = [
    "phd", "postdoc", "research scientist", "software engineer",
    "hardware engineer", "lab technician", "internship", "professor",
    "postdoctoral", "becario", "undergraduate", "student", "r1", "r0",
]

def test_bsc():
    print("\n=== BSC - Deep dive ===")
    try:
        url = "https://www.bsc.es/join-us/job-opportunities"
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        
        all_links = soup.find_all("a", href=True)
        job_links = [l for l in all_links if "/job-opportunities/" in l.get('href', '') 
                     and l.get_text(strip=True) 
                     and len(l.get_text(strip=True)) > 10]
        
        print(f"Job links found: {len(job_links)}")
        
        relevant = []
        for l in job_links:
            title = l.get_text(strip=True)
            title_lower = title.lower()
            if any(kw in title_lower for kw in ROLE_KEYWORDS) and not any(kw in title_lower for kw in EXCLUDE_KEYWORDS):
                relevant.append({"title": title, "url": l['href']})
        
        print(f"Relevant after filtering: {len(relevant)}")
        for j in relevant:
            print(f"  -> {j['title']}")
            print(f"     {j['url']}")
            
        print("\nAll positions (first 15):")
        for l in job_links[:15]:
            print(f"  -> {l.get_text(strip=True)[:80]}")
            
    except Exception as e:
        print(f"BSC error: {e}")


def test_qutech():
    print("\n=== QUTECH - Deep dive ===")
    try:
        url = "https://qutech.nl/careers/job-opportunities/"
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        
        all_links = soup.find_all("a", href=True)
        print(f"Total links: {len(all_links)}")
        
        job_links = [l for l in all_links if re.search(r'/vacancy|/job/|/position/', l.get('href', ''))]
        print(f"Job links: {len(job_links)}")
        for l in job_links[:10]:
            print(f"  -> {l.get_text(strip=True)[:80]} | {l['href']}")
        
        # Try headings
        for tag in ["h2", "h3", "h4"]:
            headings = soup.find_all(tag)
            if headings:
                print(f"\n{tag} headings ({len(headings)}):")
                for h in headings[:8]:
                    print(f"  -> {h.get_text(strip=True)[:80]}")
                    
    except Exception as e:
        print(f"QuTech error: {e}")


def test_tecnalia():
    print("\n=== TECNALIA - Corrected URL ===")
    try:
        url = "https://www.tecnalia.com/trabaja-en-tecnalia"
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        
        title = soup.find("title")
        print(f"Page title: {title.get_text(strip=True)[:80] if title else 'N/A'}")
        
        all_links = soup.find_all("a", href=True)
        job_links = [l for l in all_links if re.search(r'/empleo|/job|/oferta|/vacante|/posicion|\d{4,}', l.get('href', ''))]
        print(f"Job links: {len(job_links)}")
        for l in job_links[:10]:
            print(f"  -> {l.get_text(strip=True)[:80]} | {l['href']}")
            
    except Exception as e:
        print(f"Tecnalia error: {e}")


def test_vtt():
    print("\n=== VTT - Corrected URL ===")
    try:
        url = "https://www.vttresearch.com/en/careers/come-and-build-future-vtt"
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        
        title = soup.find("title")
        print(f"Page title: {title.get_text(strip=True)[:80] if title else 'N/A'}")
        
        all_links = soup.find_all("a", href=True)
        job_links = [l for l in all_links if re.search(r'/job|/position|/vacancy|/open-position', l.get('href', ''))]
        print(f"Job links: {len(job_links)}")
        for l in job_links[:10]:
            print(f"  -> {l.get_text(strip=True)[:80]} | {l['href']}")
            
    except Exception as e:
        print(f"VTT error: {e}")


def test_imec():
    print("\n=== IMEC - Try different URLs ===")
    urls = [
        "https://www.imec-int.com/en/work-at-imec",
        "https://www.imec-int.com/en/careers",
        "https://imec-int.com/en/careers/job-opportunities",
    ]
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            print(f"Status {url}: {r.status_code}")
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                title = soup.find("title")
                print(f"Page title: {title.get_text(strip=True)[:80] if title else 'N/A'}")
                all_links = soup.find_all("a", href=True)
                job_links = [l for l in all_links if re.search(r'/job|/vacancy|/career|/position|\d{4,}', l.get('href', ''))]
                print(f"Job links: {len(job_links)}")
                for l in job_links[:5]:
                    print(f"  -> {l.get_text(strip=True)[:80]} | {l['href']}")
                break
        except Exception as e:
            print(f"imec error ({url}): {e}")


def test_quantum_ada():
    print("\n=== QUANTUM ADA - Empleo público ===")
    try:
        url = "https://www.juntadeandalucia.es/organismos/ada/servicios/ofertas-empleo-publico.html"
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        
        title = soup.find("title")
        print(f"Page title: {title.get_text(strip=True)[:80] if title else 'N/A'}")
        
        all_links = soup.find_all("a", href=True)
        print(f"Total links: {len(all_links)}")
        
        for tag in ["h2", "h3", "h4"]:
            headings = soup.find_all(tag)
            if headings:
                print(f"{tag} headings ({len(headings)}):")
                for h in headings[:8]:
                    print(f"  -> {h.get_text(strip=True)[:80]}")
                    
    except Exception as e:
        print(f"Quantum ADA error: {e}")


if __name__ == "__main__":
    print("Testing institutional job portals v5...")
    test_bsc()
    test_qutech()
    test_tecnalia()
    test_vtt()
    test_imec()
    test_quantum_ada()
    print("\nDone!")
