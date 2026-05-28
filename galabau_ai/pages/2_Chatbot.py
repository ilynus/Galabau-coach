from pathlib import Path
import sys

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st
from src.auth import require_login, sidebar_user
from src.db import get_profile
from src.ai import chat

st.set_page_config(page_title='Chatbot', page_icon='🤖', layout='wide')
user = require_login(); sidebar_user()
profile = get_profile(user['id'])
st.title('🤖 GaLaBau-Chatbot')
fach = st.selectbox('Thema', ['Pflanzenkunde','WIPO','Baurecht/VOB/B/BGB','Treppenbau','Pflasterbau','Bodenkunde','Baustoffkunde','Prüfungsvorbereitung','Sonstiges'])
frage = st.text_area('Deine Frage', height=160, placeholder='z.B. Erkläre mir die Treppenformel mit Beispiel oder erstelle Lernfragen zu Bodenkunde.')
if st.button('Antwort erzeugen', type='primary') and frage.strip():
    with st.spinner('Antwort wird erstellt...'):
        prompt = f'Thema: {fach}\nFrage: {frage}\nBitte mit Lernbeispiel und, wenn sinnvoll, prüfungsnahen Merksätzen antworten.'
        st.markdown(chat(prompt, profile))

st.divider()
st.subheader('Schnellstarts')
cols = st.columns(3)
examples = [
    ('Treppenbau üben', 'Erkläre Steigung, Auftritt und Schrittmaßregel beim Treppenbau mit Rechenbeispiel.'),
    ('Pflanzen-Steckbrief', 'Erstelle einen Muster-Steckbrief für Lavandula angustifolia.'),
    ('WIPO', 'Erkläre mir die Rechte und Pflichten aus dem Ausbildungsvertrag prüfungsnah.')
]
for col, (title, text) in zip(cols, examples):
    with col:
        if st.button(title):
            st.session_state.example = text
            st.rerun()
if 'example' in st.session_state:
    st.info(st.session_state.pop('example'))
