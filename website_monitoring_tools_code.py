# === Scraper + Benachrichtigung ===

import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.message import EmailMessage

KEYWORDS = ["digitale Identität", "eIDAS", "EUDI-Wallet"]
URLS = [
    "https://www.kas.de/de/veranstaltungen",
    "https://www.bsi.bund.de/DE/Service/Veranstaltungen/veranstaltungen_node.html",
    # Weitere URLs können hier ergänzt werden
]

def check_events():
    results = []
    for url in URLS:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            text = soup.get_text().lower()
            for keyword in KEYWORDS:
                if keyword.lower() in text:
                    results.append((url, keyword))
        except Exception as e:
            print(f"Fehler bei {url}: {e}")
    return results

def send_email_alert(results):
    if not results:
        return
    msg = EmailMessage()
    msg["Subject"] = "Neue Veranstaltungen gefunden"
    msg["From"] = "dein.email@example.com"
    msg["To"] = "ziel.email@example.com"
    body = "\n\n".join([f"{kw}: {url}" for url, kw in results])
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.example.com", 465) as smtp:
        smtp.login("dein.email@example.com", "deinpasswort")
        smtp.send_message(msg)

if __name__ == "__main__":
    results = check_events()
    if results:
        send_email_alert(results)


# === Streamlit Dashboard ===

import streamlit as st

# Beispielhafte Resultate (in der echten Anwendung per Import aus check_events())
results = [
    ("https://www.kas.de/de/veranstaltungen", "digitale Identität"),
    ("https://www.bsi.bund.de/DE/Service/Veranstaltungen/veranstaltungen_node.html", "eIDAS"),
]

st.title("Monitoring: Veranstaltungen zu digitalen Identitäten")
if results:
    for url, keyword in results:
        st.write(f"- **{keyword}** gefunden auf: [Website]({url})")
else:
    st.success("Keine neuen Veranstaltungen gefunden.")
