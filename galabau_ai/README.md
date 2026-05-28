# GaLaBau Coach

Streamlit-MVP für eine Lernplattform in der Ausbildung zum Garten- und Landschaftsbauer.

## Funktionen

- Login und Registrierung ohne externe Datenbank
- Ausbildungsprofil für personalisierte Antworten
- KI-Chatbot für Pflanzenkunde, WIPO, Baurecht, Treppenbau, Pflasterbau usw.
- Foto-Upload mit optionaler KI-Bildanalyse
- Pflanzen-Steckbriefe und fortlaufendes PDF-Pflanzenbuch
- Karteikarten-Modul
- Themenbibliothek

## Lokal starten

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## KI aktivieren

Datei `.streamlit/secrets.toml` anlegen:

```toml
OPENAI_API_KEY = "sk-..."
```

Ohne API-Key läuft die App trotzdem. Chatbot und Bildanalyse zeigen dann nur Hinweise an.

## GitHub + Streamlit Cloud

1. Neues GitHub-Repository erstellen.
2. Projektdateien hochladen oder pushen.
3. Auf Streamlit Community Cloud Repository verbinden.
4. Main file: `app.py`.
5. Optional Secret `OPENAI_API_KEY` in Streamlit Cloud setzen.

## Hinweise

- Die lokale SQLite-Datenbank liegt in `data/galabau.db` und ist in `.gitignore` ausgeschlossen.
- Uploads liegen in `uploads/` und generierte PDFs in `generated/`.
- Für produktive Nutzung sollte später eine richtige Datenbank, Rollenverwaltung und Datenschutzseite ergänzt werden.

## Token- und Kostenoptimierung der LLM-Schnittstelle

Die LLM-Schicht in `src/ai.py` ist kostenarm konfiguriert:

- kurzer Systemprompt statt langer Rollenbeschreibung
- kompaktes Ausbildungsprofil statt vollständiger JSON-/Datenbankdaten
- Begrenzung langer Nutzereingaben
- `max_tokens` je Use Case
- Session-Cache für identische Anfragen
- Bildkomprimierung vor Vision-Anfragen
- Vision-Modus mit `detail="low"`
- optionale Modellwahl über `.streamlit/secrets.toml`

Beispiel:

```toml
OPENAI_API_KEY="..."
OPENAI_TEXT_MODEL="gpt-4o-mini"
OPENAI_VISION_MODEL="gpt-4o-mini"
```
