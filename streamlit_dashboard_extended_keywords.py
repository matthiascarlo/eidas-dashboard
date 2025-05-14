
import requests
from bs4 import BeautifulSoup
import streamlit as st

KEYWORDS = [
    "digitale Verwaltung Identität",
    "digitaler Personalausweis EU",
    "EUDI für Behörden",
    "eIDAS für öffentliche Verwaltung",
    "Interoperabilität digitale Identität",
    "digitale Identität",
    "digital identity",
    "self-sovereign identity",
    "SSI und eIDAS",
    "digitale Brieftasche EU",
    "Vertrauensdiensteanbieter",
    "trust service provider",
    "eID",
    "elektronischer Identitätsnachweis EU",
    "Verordnung (EU) 2024/1183",
    "wallet government services",
    "Verwaltungsdigitalisierung Identität",
    "Behördenzugang EUDI Wallet",
    "eIDAS"
]

SOURCES = {
    "Konrad-Adenauer-Stiftung": "https://www.kas.de/de/veranstaltungen",
    "BSI – Bundesamt für Sicherheit in der Informationstechnik": "https://www.bsi.bund.de/DE/Service/Veranstaltungen/veranstaltungen_node.html",
    "NEGZ": "https://negz.org/aktuelle-veranstaltungen/",
    "BITKOM": "https://www.bitkom.org/events#konferenzen", 
    "Friedrich-Naumann-Stiftung": "https://shop.freiheit.org/", 
    "Friedrich-Ebert-Stiftung": "https://www.fes.de/veranstaltungen", 
    "Heinrich-Böll-Stiftung": "https://calendar.boell.de/de/calendar/advancedsearch?f%5B0%5D=webseiten_zuordnung_des_termins%3A3617", 
    "Behörden Spiegel": "https://www.behoerden-spiegel.de/veranstaltungen/", 
    
    # Weitere Quellen hier hinzufügen
}

def check_events():
    results = []
    for name, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            text = soup.get_text(separator=" ").lower()
            for keyword in KEYWORDS:
                if keyword.lower() in text:
                    index = text.find(keyword.lower())
                    snippet = text[max(index-100, 0):index+100]
                    snippet = snippet.replace("\n", " ").strip()
                    results.append((name, url, keyword, snippet))
        except Exception as e:
            results.append((name, url, "FEHLER", f"Fehler beim Zugriff: {e}"))
    return results

# Streamlit Dashboard
st.title("Monitoring: Veranstaltungen zu digitalen Identitäten")

results = check_events()

if results:
    for name, url, keyword, snippet in results:
        if keyword != "FEHLER":
            st.markdown(f"🔎 **{keyword}** gefunden auf **{name}** ([{url.split('//')[1].split('/')[0]}]({url})) in folgendem Text: „...{snippet}...“")
        else:
            st.warning(f"⚠️ Fehler bei {name} ({url}): {snippet}")
else:
    st.success("Keine neuen Veranstaltungen gefunden.")
