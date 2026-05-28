import streamlit as st
from src.auth import require_login, sidebar_user
from src.db import init_db, get_profile

st.set_page_config(page_title='GaLaBau Coach', page_icon='🌿', layout='wide')
init_db()
user = require_login()
sidebar_user()
profile = get_profile(user['id'])

st.title('🌿 GaLaBau Coach')
st.subheader('Dein Lernsystem für die Ausbildung im Garten- und Landschaftsbau')

c1, c2, c3 = st.columns(3)
c1.metric('Ausbildungsjahr', profile.get('ausbildungsjahr') or 'offen')
c2.metric('Bundesland', profile.get('bundesland') or 'offen')
c3.metric('Prüfungsziel', profile.get('pruefungsziel') or 'offen')

st.markdown('''
### Was du hier machen kannst
- KI-Lerncoach für Pflanzenkunde, WIPO, Baurecht, Treppenbau, Pflasterbau und Baustellenfragen nutzen
- Fotos hochladen und kategorisieren lassen
- ein fortlaufendes Pflanzenbuch als PDF erzeugen
- Karteikarten für Prüfungsthemen erstellen und wiederholen
- dein Ausbildungsprofil pflegen, damit Antworten besser zu dir passen
''')

st.info('Starte links mit „Profil“ und fülle dein Ausbildungsprofil aus. Danach funktionieren Chatbot und Lernkarten deutlich gezielter.')
