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
kurz = st.toggle('Kurze, kostensparende Antwort', value=True)
if st.button('Antwort erzeugen', type='primary') and frage.strip():
    with st.spinner('Antwort wird erstellt...'):
        style = 'Antworte knapp in Stichpunkten, mit 1 Beispiel und 1 Merksatz.' if kurz else 'Antworte ausführlicher, aber ohne unnötige Wiederholungen.'
        prompt = f'Thema:{fach}\nFrage:{frage}\n{style}'
        st.markdown(chat(prompt, profile, max_tokens=380 if kurz else 750))

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
