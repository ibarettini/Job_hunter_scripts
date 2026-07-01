#!/usr/bin/env python3
"""
Quantum Job Monitor v3
LinkedIn + ETH Zurich + BSC + QuTech + quantum portals
"""

import requests
import smtplib
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from bs4 import BeautifulSoup

# ============================================================
# CONFIGURACIÓN
# ============================================================

EMAIL_FROM = "inakibarettini@gmail.com"
EMAIL_TO   = "inakibarettini@gmail.com"
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_PASSWORD", "")

ROLE_KEYWORDS = [
    "business development", "commercial partnerships", "market development",
    "application manager", "innovation manager", "tech transfer",
    "ip licensing", "licensing management", "bd manager", "head of commercial",
    "quantum applications", "quantum solutions", "quantum ecosystem",
    "quantum commercialization", "quantum partnerships", "exploitation manager",
    "valorisation", "knowledge transfer", "chief of staff", "project manager",
    "director", "manager", "head of", "coordinator",
]

SECTOR_KEYWORDS = [
    "quantum", "qkd", "post-quantum", "deep tech", "photonics", "cryptography",
    "quantum computing", "quantum sensing", "quantum communication",
]

COUNTRY_KEYWORDS = [
    "germany", "deutschland", "munich", "berlin", "hamburg", "frankfurt",
    "switzerland", "zurich", "zürich", "geneva", "basel",
    "austria", "vienna", "wien",
    "netherlands", "amsterdam", "eindhoven", "delft",
    "remote", "hybrid", "europe", "european",
    "finland", "espoo", "france", "paris",
    "spain", "barcelona", "madrid",
]

EXCLUDE_KEYWORDS = [
    "phd", "postdoc", "research scientist", "software engineer",
    "hardware engineer", "lab technician", "internship", "praktikum",
    "process engineer", "design engineer", "test engineer",
    "undergraduate", "student", "r1)", "r0)", "r2)",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# ============================================================
# FUENTES
# ============================================================

def fetch_linkedin():
    jobs = []
    searches = [
        "quantum+business+development&location=Germany",
        "quantum+business+development&location=Switzerland",
        "quantum+innovation+manager&location=Europe",
        "tech+transfer+quantum&location=Europe",
        "quantum+ecosystem+manager&location=Europe",
        "quantum+partnerships&location=Europe",
    ]
    for s in searches:
        try:
            url = f"https://www.linkedin.com/jobs/search/?keywords={s}&f_WT=2%2C3"
            r = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            for card in soup.find_all("div", class_=re.compile("job-search-card")):
                title = card.find("h3")
                company = card.find("h4")
                location = card.find("span", class_=re.compile("location"))
                link = card.find("a", href=True)
                if title:
                    jobs.append({
                        "title": title.get_text(strip=True),
                        "company": company.get_text(strip=True) if company else "",
                        "location": location.get_text(strip=True) if location else "",
                        "url": link["href"] if link else "",
                        "source": "LinkedIn"
                    })
        except Exception as e:
            print(f"LinkedIn error: {e}")
    return jobs


def fetch_quantumjobs_us():
    jobs = []
    try:
        url = "https://www.quantumjobs.us/jobs"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for card in soup.find_all(["div", "li", "article"], class_=re.compile("job|posting|listing")):
            title = card.find(["h2", "h3", "h4", "a"])
            link = card.find("a", href=True)
            if title:
                jobs.append({
                    "title": title.get_text(strip=True),
                    "company": "",
                    "location": "",
                    "url": "https://www.quantumjobs.us" + link["href"] if link and link["href"].startswith("/") else (link["href"] if link else ""),
                    "source": "quantumjobs.us"
                })
    except Exception as e:
        print(f"quantumjobs.us error: {e}")
    return jobs


def fetch_quantumcomputingjobs_uk():
    jobs = []
    try:
        url = "https://quantumcomputingjobs.co.uk/jobs/"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for card in soup.find_all(["div", "li", "article"], class_=re.compile("job|posting|listing")):
            title = card.find(["h2", "h3", "h4", "a"])
            link = card.find("a", href=True)
            location = card.find(class_=re.compile("location|place"))
            company = card.find(class_=re.compile("company|employer"))
            if title:
                jobs.append({
                    "title": title.get_text(strip=True),
                    "company": company.get_text(strip=True) if company else "",
                    "location": location.get_text(strip=True) if location else "",
                    "url": link["href"] if link else "",
                    "source": "quantumcomputingjobs.co.uk"
                })
    except Exception as e:
        print(f"quantumcomputingjobs.co.uk error: {e}")
    return jobs


def fetch_quantum_consortium():
    jobs = []
    try:
        url = "https://quantumconsortium.org/quantum-jobs/"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for card in soup.find_all(["div", "li", "article"], class_=re.compile("job|posting|listing")):
            title = card.find(["h2", "h3", "h4", "a"])
            link = card.find("a", href=True)
            if title:
                jobs.append({
                    "title": title.get_text(strip=True),
                    "company": "",
                    "location": "",
                    "url": link["href"] if link else "",
                    "source": "quantumconsortium.org"
                })
    except Exception as e:
        print(f"quantumconsortium.org error: {e}")
    return jobs


def fetch_eth_zurich():
    jobs = []
    try:
        url = "https://jobs.ethz.ch/site/index"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        all_links = soup.find_all("a", href=True)
        job_links = [l for l in all_links if "/job/view/" in l.get('href', '')]
        for link in job_links:
            title = link.get_text(strip=True)
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


def fetch_bsc():
    jobs = []
    try:
        url = "https://www.bsc.es/join-us/job-opportunities"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        all_links = soup.find_all("a", href=True)
        job_links = [l for l in all_links if "/job-opportunities/" in l.get('href', '')
                     and l.get_text(strip=True)
                     and len(l.get_text(strip=True)) > 10]
        for link in job_links:
            jobs.append({
                "title": link.get_text(strip=True),
                "company": "BSC Barcelona Supercomputing Center",
                "location": "Barcelona, Spain",
                "url": link['href'],
                "source": "BSC"
            })
    except Exception as e:
        print(f"BSC error: {e}")
    return jobs


def fetch_qutech():
    jobs = []
    try:
        url = "https://qutech.nl/careers/job-opportunities/"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        all_links = soup.find_all("a", href=True)
        job_links = [l for l in all_links if "/vacancy/" in l.get('href', '')
                     and l.get_text(strip=True)
                     and len(l.get_text(strip=True)) > 5]
        seen = set()
        for link in job_links:
            if link['href'] not in seen:
                seen.add(link['href'])
                jobs.append({
                    "title": link.get_text(strip=True),
                    "company": "QuTech / TU Delft",
                    "location": "Delft, Netherlands",
                    "url": link['href'],
                    "source": "QuTech"
                })
    except Exception as e:
        print(f"QuTech error: {e}")
    return jobs


# ============================================================
# FILTRADO
# ============================================================

def is_relevant(job):
    text = f"{job['title']} {job['company']} {job['location']}".lower()
    for kw in EXCLUDE_KEYWORDS:
        if kw in text:
            return False
    has_sector = any(kw in text for kw in SECTOR_KEYWORDS)
    if not has_sector:
        return False
    has_role = any(kw in text for kw in ROLE_KEYWORDS)
    if not has_role:
        return False
    return True


def is_relevant_institutional(job):
    text = f"{job['title']} {job['company']}".lower()
    for kw in EXCLUDE_KEYWORDS:
        if kw in text:
            return False
    has_role = any(kw in text for kw in ROLE_KEYWORDS)
    return has_role


# ============================================================
# EMAIL
# ============================================================

def send_email(jobs):
    today = datetime.now().strftime("%d/%m/%Y")
    if not jobs:
        subject = f"🔍 Quantum Jobs Monitor – {today} – Sin novedades"
        body_html = f"""
        <h2>Quantum Job Monitor – {today}</h2>
        <p>No se han encontrado ofertas nuevas relevantes hoy.</p>
        <p><i>Fuentes: LinkedIn | quantumjobs.us | quantumcomputingjobs.co.uk | quantumconsortium.org | ETH Zurich | BSC | QuTech</i></p>
        """
    else:
        subject = f"🚀 Quantum Jobs Monitor – {today} – {len(jobs)} oferta(s) encontrada(s)"
        rows = ""
        for j in jobs:
            rows += f"""
            <tr>
                <td style="padding:8px;border-bottom:1px solid #eee;">
                    <a href="{j['url']}" style="color:#1a73e8;font-weight:bold;">{j['title']}</a>
                </td>
                <td style="padding:8px;border-bottom:1px solid #eee;">{j['company']}</td>
                <td style="padding:8px;border-bottom:1px solid #eee;">{j['location']}</td>
                <td style="padding:8px;border-bottom:1px solid #eee;color:#888;">{j['source']}</td>
            </tr>
            """
        body_html = f"""
        <html><body style="font-family:Arial,sans-serif;max-width:800px;margin:auto;">
        <h2 style="color:#1a73e8;">🚀 Quantum Job Monitor – {today}</h2>
        <p>Se han encontrado <b>{len(jobs)}</b> oferta(s) relevante(s):</p>
        <table style="width:100%;border-collapse:collapse;">
            <thead>
                <tr style="background:#f1f3f4;">
                    <th style="padding:8px;text-align:left;">Posición</th>
                    <th style="padding:8px;text-align:left;">Empresa</th>
                    <th style="padding:8px;text-align:left;">Ubicación</th>
                    <th style="padding:8px;text-align:left;">Fuente</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        <br>
        <p style="color:#888;font-size:12px;">
            Fuentes: LinkedIn | quantumjobs.us | quantumcomputingjobs.co.uk | quantumconsortium.org | ETH Zurich | BSC | QuTech
        </p>
        </body></html>
        """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.attach(MIMEText(body_html, "html"))
    password = GMAIL_APP_PASSWORD.replace(" ", "")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, password)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    print(f"Email enviado: {subject}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando búsqueda quantum v3...")

    general_jobs = []
    general_jobs += fetch_linkedin()
    general_jobs += fetch_quantumjobs_us()
    general_jobs += fetch_quantumcomputingjobs_uk()
    general_jobs += fetch_quantum_consortium()

    institutional_jobs = []
    institutional_jobs += fetch_eth_zurich()
    institutional_jobs += fetch_bsc()
    institutional_jobs += fetch_qutech()

    relevant_general = [j for j in general_jobs if is_relevant(j)]
    relevant_institutional = [j for j in institutional_jobs if is_relevant_institutional(j)]

    all_relevant = relevant_general + relevant_institutional

    seen = set()
    unique = []
    for j in all_relevant:
        key = f"{j['title'].lower()}|{j['company'].lower()}"
        if key not in seen:
            seen.add(key)
            unique.append(j)

    print(f"Total antes de filtrar: {len(general_jobs) + len(institutional_jobs)}")
    print(f"Ofertas relevantes: {len(unique)}")

    send_email(unique)
    print("¡Listo!")
