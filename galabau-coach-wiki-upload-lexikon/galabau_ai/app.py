import streamlit as st
from src.theme import apply_theme
from src.auth import require_login, sidebar_user
from src.db import init_db, get_profile
from src.lexicon_data import LEXICON, QUICK_QUESTIONS

st.set_page_config(page_title='GaLaBau Coach', page_icon='🌿', layout='wide')
apply_theme()
init_db()
user = require_login()
sidebar_user()
profile = get_profile(user['id'])

st.markdown(
    """
    <div class="gbc-hero">
      <h1>🌿 GaLaBau Coach</h1>
      <p>Dein Lernsystem für Ausbildung, Baustelle, Pflanzenkunde und Prüfungsvorbereitung.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)
c1.metric('Ausbildungsjahr', profile.get('ausbildungsjahr') or 'offen')
c2.metric('Bundesland', profile.get('bundesland') or 'offen')
c3.metric('Prüfungsziel', profile.get('pruefungsziel') or 'offen')

st.divider()

left, right = st.columns([1.35, 1])
with left:
    st.subheader('Dein nächster Schritt')
    st.markdown(
        """
        <div class="gbc-card">
        <h3>📚 Schnell starten</h3>
        <p>Nutze links die Seiten für Profil, Chatbot, Pflanzenbuch, Karteikarten und das neue Lexikon.
        Die App ist jetzt stärker wie ein Lern-Dashboard aufgebaut: klare Navigation, Karten, Suchfunktion und Quellenbereich.</p>
        <span class="gbc-chip">Pflanzenkunde</span>
        <span class="gbc-chip">Pflasterbau</span>
        <span class="gbc-chip">Treppenbau</span>
        <span class="gbc-chip">WIPO</span>
        <span class="gbc-chip">Arbeitsschutz</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.subheader('Nachschlagewerk')
    st.markdown(
        f"""
        <div class="gbc-card">
        <h3>🔎 {len(LEXICON)} Lexikon-Einträge</h3>
        <p>Öffentliche Grunddaten, Wikipedia-Schnittstelle und Upload-Ergänzung sind eingebaut.
        Öffne <b>Themenbibliothek</b>, um zu suchen, Artikel zu übernehmen und eigene Unterlagen zu prüfen.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader('Beispielfragen')
cols = st.columns(3)
for i, question in enumerate(QUICK_QUESTIONS[:3]):
    with cols[i]:
        st.info(question)

st.markdown(
    """
    <div class="gbc-callout">
    <b>Hinweis:</b> Die Lexikon-Inhalte sind Lernnotizen. Normen, VOB/B, BBiG/BGB-Fragen,
    Pflanzenschutz und Prüfungsanforderungen bitte immer mit aktueller Originalquelle,
    Unterrichtsmaterial oder Ausbilder/in abgleichen.
    </div>
    """,
    unsafe_allow_html=True,
)
