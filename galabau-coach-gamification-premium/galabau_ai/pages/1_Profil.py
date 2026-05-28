import streamlit as st
from src.gamification import add_event
from src.theme import apply_theme
from src.auth import require_login, sidebar_user
from src.db import get_profile, save_profile

st.set_page_config(page_title='Profil', page_icon='👤', layout='wide')
apply_theme()
user = require_login(); sidebar_user()
profile = get_profile(user['id'])
st.title('👤 Ausbildungsprofil')
st.caption('Diese Angaben nutzt der Chatbot, um Antworten auf Ausbildungsjahr, Bundesland und Lernstand anzupassen.')

with st.form('profil'):
    name = st.text_input('Name', profile.get('name') or '')
    jahr = st.selectbox('Ausbildungsjahr', [1,2,3], index=max(0, int(profile.get('ausbildungsjahr') or 1)-1))
    bundesland = st.text_input('Bundesland', profile.get('bundesland') or '')
    schwerpunkte = st.text_area('Betriebsschwerpunkte / Interessen', profile.get('schwerpunkte') or '', placeholder='z.B. Pflasterbau, Pflanzenpflege, Naturstein, Teichbau')
    staerken = st.text_area('Stärken', profile.get('staerken') or '')
    schwaechen = st.text_area('Schwächen / Themen, die geübt werden sollen', profile.get('schwaechen') or '')
    pruefungsziel = st.text_input('Prüfungsziel', profile.get('pruefungsziel') or '', placeholder='z.B. Zwischenprüfung 2026')
    if st.form_submit_button('Profil speichern', type='primary'):
        save_profile(user['id'], name=name, ausbildungsjahr=jahr, bundesland=bundesland, schwerpunkte=schwerpunkte, staerken=staerken, schwaechen=schwaechen, pruefungsziel=pruefungsziel)
        add_event(user['id'], 'profile_update')
    st.success('Profil gespeichert. +20 Punkte')
