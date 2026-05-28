import streamlit as st
from src.gamification import add_event
from src.theme import apply_theme
from src.auth import require_login, sidebar_user
from src.db import get_profile
from src.ai import chat
from src.lexicon_data import QUICK_QUESTIONS

st.set_page_config(page_title='Chatbot', page_icon='🤖', layout='wide')
apply_theme()
user = require_login(); sidebar_user()
profile = get_profile(user['id'])

st.markdown(
    """
    <div class="gbc-hero">
      <h1>🤖 GaLaBau-Chatbot</h1>
      <p>Stelle Fragen zu Pflanzenkunde, Baustelle, Prüfung und WIPO. Nutze die Schnellstarts für typische Lernfragen.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

fach = st.selectbox('Thema', ['Pflanzenkunde','WIPO','Baurecht/VOB/B/BGB','Treppenbau','Pflasterbau','Bodenkunde','Baustoffkunde','Prüfungsvorbereitung','Sonstiges'])
frage = st.text_area('Deine Frage', height=160, placeholder='z.B. Erkläre mir die Treppenformel mit Beispiel oder erstelle Lernfragen zu Bodenkunde.')

if st.button('Antwort erzeugen', type='primary', use_container_width=True) and frage.strip():
    with st.spinner('Antwort wird erstellt...'):
        prompt = f"""Thema: {fach}
Frage: {frage}

Bitte antworte verständlich für GaLaBau-Azubis.
Baue ein Lernbeispiel, typische Fehler und eine kurze Merkliste ein.
Wenn es um Recht, Normen oder Prüfung geht: deutlich sagen, dass aktuelle Originalquellen/Unterrichtsmaterial zu prüfen sind."""
        st.markdown(chat(prompt, profile))
        add_event(user['id'], 'chat_question')
        st.toast('🤖 +10 Punkte für deine Lernfrage')

st.divider()
st.subheader('Schnellstarts')
cols = st.columns(3)
examples = [
    ('Treppenbau üben', 'Erkläre Steigung, Auftritt und Schrittmaßregel beim Treppenbau mit Rechenbeispiel.'),
    ('Pflanzen-Steckbrief', 'Erstelle einen Muster-Steckbrief für Lavandula angustifolia.'),
    ('WIPO', 'Erkläre mir die Rechte und Pflichten aus dem Ausbildungsvertrag prüfungsnah.'),
] + [(f'Frage {i+1}', q) for i, q in enumerate(QUICK_QUESTIONS[:3])]

for i, (title, text) in enumerate(examples[:6]):
    with cols[i % 3]:
        if st.button(title, use_container_width=True):
            st.session_state.example = text
            st.rerun()
if 'example' in st.session_state:
    st.info(st.session_state.pop('example'))
