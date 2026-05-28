from pathlib import Path
import time
import streamlit as st
import pandas as pd
from src.auth import require_login, sidebar_user
from src.db import insert_plant, list_plants
from src.pdf_generator import generate_pflanzenbuch

ROOT = Path(__file__).resolve().parents[1]
UPLOADS = ROOT / 'uploads'; UPLOADS.mkdir(exist_ok=True)

st.set_page_config(page_title='Pflanzenbuch', page_icon='🌱', layout='wide')
user = require_login(); sidebar_user()
st.title('🌱 Pflanzenkunde & Pflanzenbuch')

tab_new, tab_book = st.tabs(['Neue Pflanze', 'Mein Pflanzenbuch'])
with tab_new:
    st.subheader('Steckbrief anlegen')
    with st.form('plant', clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            deutscher_name = st.text_input('Deutscher Name')
            botanischer_name = st.text_input('Botanischer Name')
            familie = st.text_input('Familie')
            standort = st.text_input('Standort')
            boden = st.text_input('Boden')
            bluetezeit = st.text_input('Blütezeit')
        with col2:
            verwendung = st.text_area('Verwendung im GaLaBau')
            pflege = st.text_area('Pflege / Schnitt / Besonderheiten')
            merkmale = st.text_area('Erkennungsmerkmale')
            bildquelle = st.text_input('Bildquelle', placeholder='Eigenes Foto oder URL/Quelle eintragen')
            status = st.selectbox('Status', ['Entwurf','Geprüft','Bild fehlt noch'])
            bild = st.file_uploader('Eigenes Bild', type=['jpg','jpeg','png','webp'])
        submitted = st.form_submit_button('Pflanze speichern', type='primary')
    if submitted:
        bildpfad = ''
        if bild:
            p = UPLOADS / f"plant_{user['id']}_{int(time.time())}{Path(bild.name).suffix.lower()}"
            p.write_bytes(bild.getbuffer())
            bildpfad = str(p)
        insert_plant(user['id'], locals() | {'bildpfad': bildpfad})
        st.success('Pflanze gespeichert.')

with tab_book:
    plants = list_plants(user['id'])
    if not plants:
        st.info('Noch keine Pflanzen gespeichert.')
    else:
        st.dataframe(pd.DataFrame(plants)[['deutscher_name','botanischer_name','familie','standort','bluetezeit','status','created_at']], use_container_width=True)
        if st.button('PDF-Pflanzenbuch erzeugen', type='primary'):
            path = generate_pflanzenbuch(plants, user['username'])
            st.success('PDF wurde erstellt.')
            st.download_button('PDF herunterladen', path.read_bytes(), file_name=path.name, mime='application/pdf')
        for p in plants:
            with st.expander(f"{p.get('deutscher_name') or 'Unbenannt'} – {p.get('botanischer_name') or ''}"):
                cols = st.columns([1,2])
                with cols[0]:
                    if p.get('bildpfad') and Path(p['bildpfad']).exists():
                        st.image(p['bildpfad'], use_container_width=True)
                    else:
                        st.warning('Bild fehlt noch.')
                with cols[1]:
                    st.write('**Familie:**', p.get('familie') or '-')
                    st.write('**Standort:**', p.get('standort') or '-')
                    st.write('**Boden:**', p.get('boden') or '-')
                    st.write('**Blütezeit:**', p.get('bluetezeit') or '-')
                    st.write('**Verwendung:**', p.get('verwendung') or '-')
                    st.write('**Pflege:**', p.get('pflege') or '-')
                    st.write('**Merkmale:**', p.get('merkmale') or '-')
                    st.write('**Bildquelle:**', p.get('bildquelle') or '-')
