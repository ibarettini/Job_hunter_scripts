#!/usr/bin/env python3
"""
Broad Tech Job Monitor - semiconductors, cybersecurity, deep tech + broad quantum BD
"""

import requests
import smtplib
import os
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

# Roles (cualquiera de estos)
ROLE_KEYWORDS = [
    "business development",
    "commercial partnerships",
    "market development",
    "application manager",
    "innovation manager",
    "tech transfer",
    "ip licensing",
    "licensing management",
    "bd manager",
    "head of commercial",
    "product strategy",
    "gtm manager",
    "partnership manager",
    "ecosystem manager",
    "solutions architect",
    "applications engineer",
    "commercial director",
    "quantum applications",
    "quantum solutions",
    "quantum ecosystem",
    "quantum commercialization",
    "quantum partnerships",
]

# Sectores (al menos uno)
SECTOR_KEYWORDS = [
    "quantum",
    "semiconductor",
    "microelectronics",
    "cybersecurity",
    "digital identity",
    "authentication",
    "cryptography",
    "photonics",
    "optics",
    "iot",
    "deep tech",
    "smart building",
    "access control",
    "defense tech",
    "dual use",
    "nxp",
    "infineon",
    "stmicroelectronics",
    "ams-osram",
    "bosch semiconductor",
    "nordic semiconductor",
    "melexis",
    "elmos",
    "trumpf",
    "jenoptik",
    "aixtron",
]

# Nivel senior
SENIORITY_KEYWORDS = [
    "senior", "director", "head of", "lead", "principal",
    "manager", "vp", "chief", "architect"
]

# Países y modalidad
COUNTRY_KEYWORDS = [
    "germany", "deutschland", "munich", "berlin", "hamburg", "frankfurt",
    "switzerland", "zurich", "zürich", "geneva", "basel",
    "austria", "vienna", "wien",
    "netherlands", "amsterdam", "eindhoven", "delft",
    "france", "paris", "grenoble",
    "uk", "london", "oxford", "cambridge",
    "remote", "hybrid", "europe"
]

# Excluir roles puramente técnicos
EXCLUDE_KEYWORDS = [
    "phd position", "postdoc", "research scientist", "software engineer",
    "hardware engineer", "lab technician", "internship", "praktikum",
    "process engineer", "design engineer", "test engineer"
]

# ============================================================
# FUENTES
# ============================================================

def fetch_google_jobs():
    jobs = []
    queries = [
        "semiconductor business development manager Europe",
        "cybersecurity digital identity business development DACH",
        "photonics innovation manager Germany Switzerland",
        "quantum applications manager Europe",
        "deep tech partnership manager Europe remote",
        "semiconductor GTM product strategy Netherlands Germany",
    ]
    headers = {"User-Agent": "Mozilla/5.0"}
    for query in queries:
        try:
            encoded = requests.utils.quote(query)
            url = f"https://www.google.com/search?q={encoded}+jobs&tbm=jobs&hl=en"
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            for card in soup.find_all("div", class_=lambda c: c and "job" in c.lower()):
                title = card.find("h3")
                company = card.find("div", class_=lambda c: c and "company" in c.lower())
                location = card.find("div", class_=lambda c: c and "location" in c.lower())
                link = card.find("a", href=True)
                if title:
                    jobs.append({
                        "title": title.get_text(strip=True),
                        "company": company.get_text(strip=True) if company else "",
                        "location": location.get_text(strip=True) if location else "",
                        "url": "https://www.google.com" + link["href"] if link else "",
                        "source": "Google Jobs"
                    })
        except Exception as e:
            print(f"Google Jobs error: {e}")
    return jobs


def fetch_linkedin():
    jobs = []
    searches = [
        "semiconductor+business+development&location=Germany",
        "semiconductor+business+development&location=Netherlands",
        "quantum+applications+manager&location=Europe",
        "cybersecurity+business+development&location=Germany",
        "photonics+innovation+manager&location=Europe",
        "deep+tech+partnership+manager&location=Europe",
    ]
    headers = {"User-Agent": "Mozilla/5.0"}
    for s in searches:
        try:
            url = f"https://www.linkedin.com/jobs/search/?keywords={s}&f_WT=2%2C3"
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            for card in soup.find_all("div", class_=lambda c: c and "job-search-card" in c.lower()):
                title = card.find("h3")
                company = card.find("h4")
                location = card.find("span", class_=lambda c: c and "location" in c.lower())
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

    has_location = any(kw in text for kw in COUNTRY_KEYWORDS)
    if not has_location:
        return False

    return True


# ============================================================
# EMAIL
# ============================================================

def send_email(jobs):
    today = datetime.now().strftime("%d/%m/%Y")

    if not jobs:
        subject = f"🔍 Broad Tech Monitor – {today} – Sin novedades"
        body_html = f"""
        <h2>Broad Tech Job Monitor – {today}</h2>
        <p>No se han encontrado ofertas nuevas relevantes hoy.</p>
        <p><i>Sectores: Semiconductores, Ciberseguridad, Fotónica, Deep Tech, Quantum BD</i></p>
        """
    else:
        subject = f"⚡ Broad Tech Monitor – {today} – {len(jobs)} oferta(s) encontrada(s)"
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
        <h2 style="color:#e8871a;">⚡ Broad Tech Job Monitor – {today}</h2>
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
            Sectores: Semiconductores | Ciberseguridad | Fotónica | Deep Tech | Quantum BD |
            DE / CH / AT / NL / FR / UK / Remote | Senior+
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
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando búsqueda amplia...")

    all_jobs = []
    all_jobs += fetch_google_jobs()
    all_jobs += fetch_linkedin()

    print(f"Total ofertas encontradas antes de filtrar: {len(all_jobs)}")

    relevant = [j for j in all_jobs if is_relevant(j)]

    seen = set()
    unique = []
    for j in relevant:
        key = f"{j['title'].lower()}|{j['company'].lower()}"
        if key not in seen:
            seen.add(key)
            unique.append(j)

    print(f"Ofertas relevantes tras filtrar: {len(unique)}")

    send_email(unique)
    print("¡Listo!")
