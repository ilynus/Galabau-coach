from __future__ import annotations
import json, os, base64
from pathlib import Path
import streamlit as st

SYSTEM = '''Du bist ein hilfreicher Lerncoach für Auszubildende im Garten- und Landschaftsbau.
Antworte praxisnah, prüfungsorientiert und altersgerecht. Nutze das Nutzerprofil, wenn vorhanden.
Bei Rechtsthemen wie BGB, VOB/B, DIN, Arbeitsschutz und Baurecht: keine Rechtsberatung im Einzelfall,
sondern Lernhinweise, Normbezug und Warnung, dass Normen/Regelwerke im Original geprüft werden müssen.'''


def api_key() -> str | None:
    return st.secrets.get('OPENAI_API_KEY', None) or os.getenv('OPENAI_API_KEY')


def chat(prompt: str, profile: dict | None = None) -> str:
    key = api_key()
    if not key:
        return ('KI ist noch nicht aktiviert. Lege in `.streamlit/secrets.toml` einen OPENAI_API_KEY an.\n\n'
                'Bis dahin kannst du die Seiten, Uploads, Karteikarten und das Pflanzenbuch lokal nutzen.')
    from openai import OpenAI
    client = OpenAI(api_key=key)
    prof = json.dumps(profile or {}, ensure_ascii=False)
    resp = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role':'system','content':SYSTEM + '\nNutzerprofil: ' + prof}, {'role':'user','content':prompt}],
        temperature=0.35,
    )
    return resp.choices[0].message.content or ''


def analyze_image(image_path: str, task: str, profile: dict | None = None) -> str:
    key = api_key()
    if not key:
        return 'Bild wurde gespeichert. KI-Bildanalyse ist erst aktiv, wenn OPENAI_API_KEY gesetzt ist.'
    from openai import OpenAI
    client = OpenAI(api_key=key)
    b64 = base64.b64encode(Path(image_path).read_bytes()).decode('utf-8')
    resp = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{
            'role':'user',
            'content':[
                {'type':'text','text': SYSTEM + '\nAufgabe: ' + task + '\nProfil: ' + json.dumps(profile or {}, ensure_ascii=False)},
                {'type':'image_url','image_url':{'url': f'data:image/jpeg;base64,{b64}'}}
            ]
        }],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ''
