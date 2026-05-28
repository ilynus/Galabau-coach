import streamlit as st
from src.theme import apply_theme
from src.auth import require_login, sidebar_user
from src.dynamic_lexicon import wiki_search, wiki_summary, curated_wiki_entries

st.set_page_config(page_title='Enzyklopädie', page_icon='🌐', layout='wide')
apply_theme()
require_login(); sidebar_user()

st.markdown(
    """
    <div class="gbc-hero">
      <h1>🌐 Enzyklopädie-Schnittstelle</h1>
      <p>Suche direkt in Wikipedia und nutze geprüfte Kurzfassungen als Lernmaterial.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info('Diese Seite lädt öffentliche Informationen aus Wikipedia. Bitte prüfungsrelevante Aussagen immer mit Unterrichtsmaterial, Gesetzen, Normen oder Fachliteratur abgleichen.')

tab_search, tab_auto = st.tabs(['Direktsuche', 'Automatische Themenliste'])

with tab_search:
    q = st.text_input('Suchbegriff', placeholder='z. B. Trockenmauer, Bodenart, Lavendel, Arbeitsschutz')
    if st.button('Suchen', type='primary') and q.strip():
        try:
            hits = wiki_search(q.strip(), limit=8)
            for hit in hits:
                with st.expander(hit['title'], expanded=False):
                    st.write(hit.get('snippet', ''))
                    try:
                        summary = wiki_summary(hit['title'])
                        st.markdown(f"**Kurz:** {summary['kurz']}")
                        st.write(summary['inhalt'])
                        st.markdown(f"**Quelle:** {summary['quelle']}")
                    except Exception:
                        st.warning('Zusammenfassung konnte nicht geladen werden.')
        except Exception as e:
            st.error(f'Wikipedia konnte nicht erreicht werden: {e}')

with tab_auto:
    st.caption('Vorkuratierte GaLaBau-Themen aus Wikipedia.')
    if st.button('Themen laden', type='primary'):
        with st.spinner('Lade Themen aus Wikipedia...'):
            try:
                entries = curated_wiki_entries(limit=24)
                st.session_state.auto_wiki_entries = entries
            except Exception as e:
                st.error(f'Konnte Themen nicht laden: {e}')

    for e in st.session_state.get('auto_wiki_entries', []):
        with st.container(border=True):
            st.caption(e['bereich'])
            st.subheader(e['titel'])
            st.write(e['inhalt'])
            st.markdown(f"**Quelle:** {e['quelle']}")
