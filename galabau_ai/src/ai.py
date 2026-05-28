from __future__ import annotations

import base64
import hashlib
import json
import os
from io import BytesIO
from pathlib import Path
from typing import Any

import streamlit as st
from PIL import Image

# Sehr kurzer Systemprompt: spart bei jeder Anfrage Tokens.
SYSTEM = (
    "Du bist ein knapper Lerncoach für GaLaBau-Azubis. "
    "Antworte praxisnah, prüfungsorientiert und nur so ausführlich wie nötig. "
    "Bei Recht/DIN/VOB/BGB: Lernhinweis, kein Einzelfall-Rechtsrat; Originalnorm prüfen."
)

DEFAULT_TEXT_MODEL = "gpt-4o-mini"
DEFAULT_VISION_MODEL = "gpt-4o-mini"
MAX_INPUT_CHARS = 1800
MAX_PROFILE_CHARS = 420
DEFAULT_MAX_TOKENS = 550
VISION_MAX_TOKENS = 420


def _secret_or_env(name: str, default: str | None = None) -> str | None:
    try:
        return st.secrets.get(name, None) or os.getenv(name) or default
    except Exception:
        return os.getenv(name) or default


def api_key() -> str | None:
    return _secret_or_env("OPENAI_API_KEY")


def text_model() -> str:
    return _secret_or_env("OPENAI_TEXT_MODEL", DEFAULT_TEXT_MODEL) or DEFAULT_TEXT_MODEL


def vision_model() -> str:
    return _secret_or_env("OPENAI_VISION_MODEL", DEFAULT_VISION_MODEL) or DEFAULT_VISION_MODEL


def _limit(text: Any, max_chars: int) -> str:
    s = "" if text is None else str(text).strip()
    return s if len(s) <= max_chars else s[: max_chars - 1].rstrip() + "…"


def compact_profile(profile: dict | None) -> str:
    """Nur die lernrelevanten Profilfelder senden, keine leeren Keys/SQL-Metadaten."""
    if not profile:
        return ""
    labels = {
        "ausbildungsjahr": "Jahr",
        "bundesland": "BL",
        "schwerpunkte": "Fokus",
        "staerken": "Stark",
        "schwaechen": "Üben",
        "pruefungsziel": "Ziel",
    }
    parts: list[str] = []
    for key, label in labels.items():
        val = _limit(profile.get(key), 120)
        if val:
            parts.append(f"{label}:{val}")
    return _limit("; ".join(parts), MAX_PROFILE_CHARS)


def _cache_key(kind: str, model: str, prompt: str, profile_hint: str = "", extra: str = "") -> str:
    raw = json.dumps(
        {"kind": kind, "model": model, "prompt": prompt, "profile": profile_hint, "extra": extra},
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _get_cache() -> dict[str, str]:
    if "llm_cache" not in st.session_state:
        st.session_state.llm_cache = {}
    return st.session_state.llm_cache


def chat(prompt: str, profile: dict | None = None, *, max_tokens: int = DEFAULT_MAX_TOKENS, use_cache: bool = True) -> str:
    """Tokenarme Textanfrage.

    Spart Kosten durch:
    - kurzen Systemprompt
    - kompaktes Profil statt kompletter JSON-Struktur
    - abgeschnittene Nutzereingabe
    - max_tokens-Limit
    - Session-Cache für identische Anfragen
    """
    key = api_key()
    if not key:
        return (
            "KI ist noch nicht aktiviert. Lege in `.streamlit/secrets.toml` einen OPENAI_API_KEY an.\n\n"
            "Bis dahin kannst du die Seiten, Uploads, Karteikarten und das Pflanzenbuch lokal nutzen."
        )

    prompt = _limit(prompt, MAX_INPUT_CHARS)
    profile_hint = compact_profile(profile)
    model = text_model()
    cache_key = _cache_key("text", model, prompt, profile_hint, str(max_tokens))
    cache = _get_cache()
    if use_cache and cache_key in cache:
        return cache[cache_key] + "\n\n*Aus Cache geladen.*"

    from openai import OpenAI

    client = OpenAI(api_key=key)
    messages = [{"role": "system", "content": SYSTEM}]
    user_content = f"Profil: {profile_hint}\n\n{prompt}" if profile_hint else prompt
    messages.append({"role": "user", "content": user_content})

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.25,
        max_tokens=max_tokens,
    )
    answer = resp.choices[0].message.content or ""
    if use_cache:
        cache[cache_key] = answer
    return answer


def _image_to_small_jpeg_b64(image_path: str, *, max_side: int = 768, quality: int = 72) -> str:
    """Komprimiert Bilder vor der API-Anfrage. Das reduziert Bild-/Vision-Kosten deutlich."""
    img = Image.open(image_path)
    img = img.convert("RGB")
    img.thumbnail((max_side, max_side))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def analyze_image(image_path: str, task: str, profile: dict | None = None, *, max_tokens: int = VISION_MAX_TOKENS) -> str:
    key = api_key()
    if not key:
        return "Bild wurde gespeichert. KI-Bildanalyse ist erst aktiv, wenn OPENAI_API_KEY gesetzt ist."

    task = _limit(task, 900)
    profile_hint = compact_profile(profile)
    model = vision_model()
    image_hash = hashlib.sha256(Path(image_path).read_bytes()).hexdigest()[:20]
    cache_key = _cache_key("vision", model, task, profile_hint, image_hash)
    cache = _get_cache()
    if cache_key in cache:
        return cache[cache_key] + "\n\n*Aus Cache geladen.*"

    from openai import OpenAI

    client = OpenAI(api_key=key)
    b64 = _image_to_small_jpeg_b64(image_path)
    text = (
        f"{SYSTEM}\nProfil:{profile_hint}\nAufgabe:{task}\n"
        "Antworte in max. 8 Stichpunkten. Unsicherheiten klar benennen."
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}", "detail": "low"}},
                ],
            }
        ],
        temperature=0.15,
        max_tokens=max_tokens,
    )
    answer = resp.choices[0].message.content or ""
    cache[cache_key] = answer
    return answer
