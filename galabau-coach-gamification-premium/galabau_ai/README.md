# GaLaBau Coach MVP – öffentliche Lexikon-Version

Diese Version wurde überarbeitet:

- Stil stärker wie die Referenz-App: dunkle Sidebar, helle Karten, Dashboard-Aufbau
- `src.theme` mit einheitlichem Design
- Admin-Login über Streamlit Secrets
- neue Themenbibliothek mit kleinem Lexikon und Quellenbereich
- pycache-Dateien entfernt

## Upload in GitHub

Den kompletten Ordner `galabau_ai` hochladen bzw. den bestehenden Ordner ersetzen.

Streamlit Main file path:

```text
galabau_ai/app.py
```

## Streamlit Secrets

In Streamlit Cloud unter App → Settings → Secrets:

```toml
ADMIN_USER = "admin"
ADMIN_PASSWORD = "DEIN_NEUES_PASSWORT"
USER_ID = "admin"
```

Bitte kein Passwort verwenden, das schon öffentlich sichtbar war.

## Quellen im Lexikon

Die App enthält Lernnotizen auf Basis öffentlich zugänglicher Informationen, u. a.:

- BIBB Berufsprofil Gärtner/in Garten- und Landschaftsbau
- Gärtnerausbildungsverordnung
- KMK Rahmenlehrplan Gärtner/Gärtnerin
- Landwirtschaftskammer NRW Lehrgangsinhalte
- Landschaftsgärtner.com Ausbildungsinhalte
- BERUFENET Berufsbild

Hinweis: Normen, VOB/B, BGB/BBiG, Pflanzenschutz und Prüfungsanforderungen immer mit aktueller Originalquelle und Unterrichtsmaterial abgleichen.


## Update: Kontrast-Fix

Eingabefelder, Labels, Platzhalter und Selectboxen wurden auf hellen Hintergrund mit dunkler Schrift gesetzt, damit Text sichtbar bleibt.


## Wichtig: Kontrast-Fix

Diese Version enthält den geprüften Kontrast-Fix für Selectboxen, Buttons, Eingabefelder und Dropdowns.

Wenn du den Ordner in GitHub umbenennst, vermeide Leerzeichen. Empfohlen:

```text
galabau_ai
```

Main file path in Streamlit:

```text
galabau_ai/app.py
```

Die `.streamlit/config.toml` liegt zusätzlich auf Repository-Ebene, damit Streamlit Cloud sicher das helle Theme nutzt.


## Update: Enzyklopädie-Schnittstelle und Upload-Ergänzung

Neu enthalten:

- `src/dynamic_lexicon.py`
- Wikipedia/MediaWiki-Suche
- automatische GaLaBau-Themenliste
- manuelles Übernehmen von Wikipedia-Zusammenfassungen ins Lexikon
- Upload-Prüfung für `.txt`, `.md`, `.csv`
- Speicherung eigener geprüfter Lexikon-Einträge in SQLite
- Quellenanzeige pro Eintrag

PDF/DOCX werden absichtlich nicht direkt gelesen, damit keine schweren Zusatzpakete nötig sind. Inhalte daraus bitte als Text exportieren oder in `.txt`/`.md` hochladen.
