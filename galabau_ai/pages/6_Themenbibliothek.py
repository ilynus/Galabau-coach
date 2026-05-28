import streamlit as st
import pandas as pd
from src.theme import apply_theme
from src.auth import require_login, sidebar_user
from src.lexicon_data import LEXICON, LEXICON_SOURCES, QUICK_QUESTIONS

st.set_page_config(page_title='Themenbibliothek', page_icon='📚', layout='wide')
apply_theme()
require_login(); sidebar_user()

st.markdown(
    """
    <div class="gbc-hero">
      <h1>📚 Themenbibliothek & Lexikon</h1>
      <p>Nachschlagen, filtern und prüfungsnah wiederholen – mit Quellenhinweisen.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning('Lernnotizen ersetzen keine aktuellen Normen, Gesetze, Unterrichtsmaterialien oder Ausbilderhinweise.')

areas = ['Alle'] + sorted({e['bereich'] for e in LEXICON})
col1, col2 = st.columns([1, 2])
with col1:
    area = st.selectbox('Bereich', areas)
with col2:
    query = st.text_input('Suche', placeholder='z. B. Pflaster, Lavendel, Prüfung, Arbeitsschutz')

def matches(entry):
    if area != 'Alle' and entry['bereich'] != area:
        return False
    if query.strip():
        hay = ' '.join([
            entry.get('bereich',''),
            entry.get('titel',''),
            entry.get('kurz',''),
            entry.get('inhalt',''),
            ' '.join(entry.get('tags', [])),
            entry.get('quelle',''),
        ]).lower()
        return query.strip().lower() in hay
    return True

results = [e for e in LEXICON if matches(e)]

m1, m2, m3 = st.columns(3)
m1.metric('Einträge', len(results))
m2.metric('Bereiche', len(set(e['bereich'] for e in LEXICON)))
m3.metric('Quellen', len(LEXICON_SOURCES))

tab_cards, tab_table, tab_sources = st.tabs(['Lexikon-Karten', 'Tabelle', 'Quellen'])

with tab_cards:
    if not results:
        st.info('Keine Treffer. Probiere einen anderen Suchbegriff.')
    for entry in results:
        with st.container(border=True):
            st.caption(entry['bereich'])
            st.subheader(entry['titel'])
            st.markdown(f"**Kurz:** {entry['kurz']}")
            st.write(entry['inhalt'])
            st.markdown(' '.join([f'<span class="gbc-chip">{tag}</span>' for tag in entry.get('tags', [])]), unsafe_allow_html=True)
            st.markdown(f"<div class='gbc-source'><b>Quelle/Abgleich:</b> {entry['quelle']}</div>", unsafe_allow_html=True)

with tab_table:
    df = pd.DataFrame(results if results else LEXICON)
    st.dataframe(df[['bereich','titel','kurz','quelle']], use_container_width=True, hide_index=True)

with tab_sources:
    st.subheader('Verwendete öffentliche Quellen')
    for s in LEXICON_SOURCES:
        st.markdown(f"**[{s['label']}]({s['url']})**")
        st.caption(s['note'])
    st.divider()
    st.subheader('Schnellfragen für den Chatbot')
    for q in QUICK_QUESTIONS:
        st.code(q, language=None)
