import streamlit as st
from src.auth import require_login, sidebar_user

st.set_page_config(page_title='Themenbibliothek', page_icon='📚', layout='wide')
require_login(); sidebar_user()
st.title('📚 Themenbibliothek')
st.markdown('''
## Pflanzenkunde
Wuchsform, Blätter, Blüte, Frucht, Standort, Boden, Pflege, Verwendung, Giftigkeit, ökologische Bedeutung.

## Treppenbau
Steigung, Auftritt, Schrittmaßregel, Podeste, Entwässerung, Frostschutz, Beläge, DIN 18065 als Orientierung prüfen.

## Pflasterbau
Planum, Frostschutzschicht, Tragschicht, Bettung, Fugen, Gefälle, Randeinfassung, Verdichtung.

## Baurecht / Recht im GaLaBau
BGB-Werkvertrag, VOB/B, Mängelrechte, Abnahme, Verkehrssicherung, Arbeitsschutz, Baustellendokumentation.

## WIPO
Ausbildungsvertrag, Tarifvertrag, Sozialversicherung, Betrieb, Markt, Staat, Rechte und Pflichten.

## Maschinen & Arbeitsschutz
PSA, Gefährdungsbeurteilung, Unterweisung, Bedienungsanleitungen, Wartung, sichere Baustelle.
''')
st.warning('Normen, VOB/B und Rechtsfragen bitte immer mit aktueller Originalquelle bzw. Unterrichtsmaterial abgleichen.')
