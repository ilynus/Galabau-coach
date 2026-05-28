"""Dynamisches Lexikon für GaLaBau Coach.

Funktionen:
- Wikipedia/MediaWiki-Suche nach Ausbildungs-Themen
- lokale Erweiterung durch vom Azubi hochgeladene Texte
- einfache Plausibilitätsprüfung: Quellenhinweis, Dubletten, Mindestlänge, Fachbezug

Hinweis:
Die Wikipedia-Schnittstelle nutzt die öffentliche MediaWiki-API.
Inhalte werden als Lernnotizen angezeigt und müssen bei prüfungs-/rechts-/normrelevanten Fragen
mit Originalquellen abgeglichen werden.
"""
from __future__ import annotations

import json
import re
import sqlite3
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DB_PATH = Path("galabau_coach.db")

WIKI_API = "https://de.wikipedia.org/w/api.php"
WIKI_REST_SUMMARY = "https://de.wikipedia.org/api/rest_v1/page/summary/"

DEFAULT_TOPICS = [
    "Garten- und Landschaftsbau",
    "Gärtner",
    "Pflaster",
    "Natursteinmauerwerk",
    "Trockenmauer",
    "Bodenart",
    "Bodenverdichtung",
    "Boden pH",
    "Kompost",
    "Drainage",
    "Bewässerung",
    "Erosionsschutz",
    "Staude",
    "Hecke",
    "Baumschnitt",
    "Pflanzenschutz",
    "Lavandula angustifolia",
    "Buxus sempervirens",
    "Taxus baccata",
    "Hydrangea macrophylla",
    "Acer campestre",
    "Carpinus betulus",
    "Baustelle",
    "Arbeitsschutz",
    "Persönliche Schutzausrüstung",
    "Werkvertrag",
    "Berufsbildungsgesetz",
]

GALABAU_KEYWORDS = [
    "garten", "landschaft", "pflanze", "baum", "strauch", "staude", "boden", "pflaster",
    "mauer", "naturstein", "baustelle", "ausbildung", "gärtner", "galabau", "bewässerung",
    "drainage", "arbeitsschutz", "werkvertrag", "berufsbildung", "pflege", "rasen",
]


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_dynamic_lexicon_db() -> None:
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS lexicon_custom (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            area TEXT NOT NULL,
            summary TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT NOT NULL,
            source TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'geprüft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fachbezug_score(text: str) -> int:
    hay = text.lower()
    return sum(1 for k in GALABAU_KEYWORDS if k in hay)


def classify_area(text: str) -> str:
    hay = text.lower()
    if any(k in hay for k in ["lavandula", "buxus", "taxus", "hydrangea", "pflanze", "baum", "strauch", "staude", "hecke"]):
        return "Pflanzenkunde"
    if any(k in hay for k in ["pflaster", "mauer", "naturstein", "treppe", "belag", "baustoff"]):
        return "Bautechnik"
    if any(k in hay for k in ["boden", "humus", "ph", "verdichtung", "erosion", "kompost"]):
        return "Bodenkunde"
    if any(k in hay for k in ["arbeitsschutz", "psa", "sicherheit", "unfall", "gefahr"]):
        return "Arbeitsschutz"
    if any(k in hay for k in ["vertrag", "bgb", "bbig", "vob", "abnahme", "ausbildung"]):
        return "WIPO & Recht"
    return "Allgemein"


def make_tags(text: str, max_tags: int = 6) -> list[str]:
    tags = []
    for k in GALABAU_KEYWORDS:
        if k in text.lower():
            tags.append(k.title())
    return tags[:max_tags] or ["Nachschlagen"]


def wiki_search(query: str, limit: int = 8) -> list[dict]:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": str(limit),
        "format": "json",
        "utf8": "1",
        "origin": "*",
    }
    url = WIKI_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "GaLaBauCoach/1.0 (educational app)"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    results = []
    for item in data.get("query", {}).get("search", []):
        title = item.get("title", "")
        snippet = re.sub("<.*?>", "", item.get("snippet", ""))
        if title:
            results.append({"title": title, "snippet": snippet})
    return results


def wiki_summary(title: str) -> dict:
    url = WIKI_REST_SUMMARY + urllib.parse.quote(title.replace(" ", "_"))
    req = urllib.request.Request(url, headers={"User-Agent": "GaLaBauCoach/1.0 (educational app)"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    extract = normalize_text(data.get("extract", ""))
    page_url = data.get("content_urls", {}).get("desktop", {}).get("page", f"https://de.wikipedia.org/wiki/{urllib.parse.quote(title)}")

    return {
        "bereich": classify_area(title + " " + extract),
        "titel": data.get("title", title),
        "kurz": extract[:220] + ("…" if len(extract) > 220 else ""),
        "inhalt": extract,
        "tags": make_tags(title + " " + extract),
        "quelle": f"Wikipedia: {page_url}",
        "url": page_url,
        "typ": "Wikipedia",
    }


def curated_wiki_entries(limit: int = 24) -> list[dict]:
    """Lädt automatisch relevante Wikipedia-Zusammenfassungen für GaLaBau-Azubis."""
    entries = []
    seen = set()

    for topic in DEFAULT_TOPICS:
        try:
            # First try exact summary; if unavailable search.
            entry = wiki_summary(topic)
            title_key = entry["titel"].lower()
            if title_key not in seen and entry["inhalt"] and fachbezug_score(entry["titel"] + " " + entry["inhalt"]) >= 1:
                entries.append(entry)
                seen.add(title_key)
        except Exception:
            try:
                for hit in wiki_search(topic, limit=3):
                    entry = wiki_summary(hit["title"])
                    title_key = entry["titel"].lower()
                    if title_key not in seen and entry["inhalt"] and fachbezug_score(entry["titel"] + " " + entry["inhalt"]) >= 1:
                        entries.append(entry)
                        seen.add(title_key)
                        break
            except Exception:
                continue
        if len(entries) >= limit:
            break

    return entries


def save_custom_entry(title: str, content: str, source: str, status: str = "geprüft") -> None:
    init_dynamic_lexicon_db()
    content = normalize_text(content)
    title = normalize_text(title)[:120] or "Eigener Eintrag"
    summary = content[:260] + ("…" if len(content) > 260 else "")
    area = classify_area(title + " " + content)
    tags = make_tags(title + " " + content)

    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO lexicon_custom (title, area, summary, content, tags, source, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (title, area, summary, content, json.dumps(tags, ensure_ascii=False), source, status),
    )
    conn.commit()
    conn.close()


def load_custom_entries() -> list[dict]:
    init_dynamic_lexicon_db()
    conn = _conn()
    rows = conn.execute("SELECT * FROM lexicon_custom ORDER BY created_at DESC").fetchall()
    conn.close()

    entries = []
    for r in rows:
        try:
            tags = json.loads(r["tags"])
        except Exception:
            tags = ["Upload"]
        entries.append(
            {
                "bereich": r["area"],
                "titel": r["title"],
                "kurz": r["summary"],
                "inhalt": r["content"],
                "tags": tags,
                "quelle": r["source"],
                "status": r["status"],
                "typ": "Upload",
            }
        )
    return entries


def split_uploaded_text(text: str, filename: str) -> list[dict]:
    """Zerlegt Upload-Text in sinnvolle Lexikon-Kandidaten."""
    text = normalize_text(text)
    if not text:
        return []

    # Prefer headings/paragraph chunks, fallback to fixed windows.
    parts = re.split(r"(?:\n\s*){2,}|(?<=\.)\s+(?=[A-ZÄÖÜ][A-Za-zÄÖÜäöüß\- ]{8,}:)", text)
    chunks = []
    current = ""

    for part in parts:
        part = normalize_text(part)
        if not part:
            continue
        if len(current) + len(part) < 900:
            current = (current + " " + part).strip()
        else:
            chunks.append(current)
            current = part
    if current:
        chunks.append(current)

    candidates = []
    for i, chunk in enumerate(chunks[:25], start=1):
        if len(chunk) < 160:
            continue

        score = fachbezug_score(chunk)
        status = "geprüft" if score >= 2 else "prüfen"

        # Try title from first sentence or first 8 words.
        first_sentence = re.split(r"(?<=[.!?])\s+", chunk)[0]
        words = first_sentence.split()
        title = " ".join(words[:9]).strip(":-–,.;")
        if len(title) < 8:
            title = f"Upload-Notiz {i}"

        candidates.append(
            {
                "title": title,
                "content": chunk,
                "source": f"Upload: {filename}",
                "status": status,
                "score": score,
            }
        )

    return candidates


def read_uploaded_file(uploaded_file) -> str:
    """Liest txt/md/csv-Dateien direkt. PDF/DOCX werden ohne Zusatzpakete nicht analysiert."""
    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()

    if name.endswith((".txt", ".md", ".csv")):
        for enc in ("utf-8", "latin-1"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return raw.decode("utf-8", errors="ignore")

    return ""


def merge_entries(static_entries: Iterable[dict], wiki_entries: Iterable[dict], custom_entries: Iterable[dict]) -> list[dict]:
    merged = []
    seen = set()
    for source in (custom_entries, wiki_entries, static_entries):
        for e in source:
            key = e.get("titel", "").lower().strip()
            if not key or key in seen:
                continue
            merged.append(e)
            seen.add(key)
    return merged
