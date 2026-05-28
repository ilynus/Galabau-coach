import streamlit as st
from src.theme import apply_theme
import pandas as pd
from src.auth import require_login, sidebar_user
from src.db import insert_flashcard, list_flashcards
from src.ai import chat
from src.db import get_profile

st.set_page_config(page_title='Karteikarten', page_icon='🧠', layout='wide')
apply_theme()
user = require_login(); sidebar_user(); profile = get_profile(user['id'])
st.title('🧠 Karteikarten')

tab_add, tab_review, tab_ai = st.tabs(['Manuell erstellen', 'Wiederholen', 'KI-Vorschläge'])
with tab_add:
    with st.form('card'):
        fach = st.selectbox('Fach', ['Pflanzenkunde','WIPO','Baurecht','Treppenbau','Pflasterbau','Bodenkunde','Baustoffkunde','Sonstiges'])
        thema = st.text_input('Thema')
        frage = st.text_area('Frage')
        antwort = st.text_area('Antwort')
        if st.form_submit_button('Karte speichern', type='primary'):
            insert_flashcard(user['id'], thema, frage, antwort, fach)
            st.success('Karte gespeichert.')
with tab_review:
    cards = list_flashcards(user['id'])
    if not cards:
        st.info('Noch keine Karteikarten vorhanden.')
    else:
        st.dataframe(pd.DataFrame(cards)[['fach','thema','frage','antwort','created_at']], use_container_width=True)
        for c in cards[:20]:
            with st.expander(f"{c['fach']} – {c['frage']}"):
                st.markdown('**Antwort:**')
                st.write(c['antwort'])
with tab_ai:
    thema = st.text_input('Thema für KI-Karteikarten', placeholder='z.B. Treppenbau Schrittmaßregel')
    anzahl = st.slider('Anzahl', 3, 12, 5)
    if st.button('Vorschläge erzeugen') and thema:
        prompt = f'Erstelle {anzahl} Karteikarten zum Thema {thema} für einen GaLaBau-Azubi. Format: Frage: ... Antwort: ...'
        st.markdown(chat(prompt, profile))
