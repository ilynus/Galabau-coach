from pathlib import Path
import time
import streamlit as st
from src.auth import require_login, sidebar_user
from src.db import get_profile, conn
from src.ai import analyze_image

ROOT = Path(__file__).resolve().parents[1]
UPLOADS = ROOT / 'uploads'; UPLOADS.mkdir(exist_ok=True)

st.set_page_config(page_title='Fotoanalyse', page_icon='📷', layout='wide')
user = require_login(); sidebar_user(); profile = get_profile(user['id'])
st.title('📷 Foto hochladen & kategorisieren')
category = st.selectbox('Kategorie', ['Pflanze','Baustelle/Pflaster','Treppe','Mauer/Naturstein','Werkzeug/Maschine','Sonstiges'])
file = st.file_uploader('Foto auswählen', type=['jpg','jpeg','png','webp'])
note = st.text_area('Notiz / Fragestellung', placeholder='z.B. Welche Pflanze ist das? Was ist beim Treppenbau falsch?')
if file and st.button('Speichern und analysieren', type='primary'):
    suffix = Path(file.name).suffix.lower()
    path = UPLOADS / f"{user['id']}_{int(time.time())}{suffix}"
    path.write_bytes(file.getbuffer())
    with conn() as c:
        c.execute('INSERT INTO uploads(user_id,filename,category,note,path) VALUES(?,?,?,?,?)', (user['id'], file.name, category, note, str(path)))
    st.image(str(path), width=350)
    task = f'Kategorisiere dieses Bild als {category}. {note}. Gib eine fachliche Einschätzung und Lernhinweise für GaLaBau-Azubis.'
    with st.spinner('Analyse läuft...'):
        st.markdown(analyze_image(str(path), task, profile))
