import streamlit as st
import pandas as pd
from src.theme import apply_theme
from src.auth import require_login, sidebar_user
from src.lexicon_data import LEXICON, LEXICON_SOURCES, QUICK_QUESTIONS
from src.dynamic_lexicon import (
    curated_wiki_entries,
    wiki_search,
    wiki_summary,
    load_custom_entries,
    save_custom_entry,
    split_uploaded_text,
    read_uploaded_file,
    merge_entries,
)

st.set_page_config(page_title='Themenbibliothek', page_icon='📚', layout='wide')
apply_theme()
require_login(); sidebar_user()

st.markdown(
    """
    <div class="gbc-hero">
      <h1>📚 Themenbibliothek & Lexikon</h1>
      <p>Wikipedia-Schnittstelle, Upload-Ergänzung und quellenbasierte Lernnotizen für GaLaBau-Azubis.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning('Lexikon-Inhalte sind Lernnotizen. Normen, Gesetze, Pflanzenschutz und Prüfungsanforderungen bitte mit aktuellen Originalquellen und Unterrichtsmaterial abgleichen.')

@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def load_wiki_auto():
    return curated_wiki_entries(limit=24)

if 'wiki_extra_entries' not in st.session_state:
    st.session_state.wiki_extra_entries = []

wiki_entries = load_wiki_auto()
custom_entries = load_custom_entries()
all_entries = merge_entries(LEXICON, wiki_entries + st.session_state.wiki_extra_entries, custom_entries)

tab_lex, tab_wiki, tab_upload, tab_sources = st.tabs(['Lexikon', 'Wikipedia ergänzen', 'Uploads prüfen', 'Quellen'])

with tab_lex:
    areas = ['Alle'] + sorted({e.get('bereich', 'Allgemein') for e in all_entries})
    col1, col2 = st.columns([1, 2])
    with col1:
        area = st.selectbox('Bereich', areas)
    with col2:
        query = st.text_input('Suche', placeholder='z. B. Pflaster, Lavendel, Prüfung, Arbeitsschutz, Boden')

    def matches(entry):
        if area != 'Alle' and entry.get('bereich') != area:
            return False
        if query.strip():
            hay = ' '.join([
                entry.get('bereich',''),
                entry.get('titel',''),
                entry.get('kurz',''),
                entry.get('inhalt',''),
                ' '.join(entry.get('tags', [])),
                entry.get('quelle',''),
            ]).lower()
            return query.strip().lower() in hay
        return True

    results = [e for e in all_entries if matches(e)]

    m1, m2, m3 = st.columns(3)
    m1.metric('Einträge', len(results))
    m2.metric('Wikipedia', len(wiki_entries) + len(st.session_state.wiki_extra_entries))
    m3.metric('Uploads', len(custom_entries))

    card_tab, table_tab = st.tabs(['Karten', 'Tabelle'])

    with card_tab:
        if not results:
            st.info('Keine Treffer. Nutze den Tab „Wikipedia ergänzen“, um passende Themen nachzuladen.')
        for entry in results:
            with st.container(border=True):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.caption(f"{entry.get('bereich','Allgemein')} · {entry.get('typ','Lexikon')}")
                    st.subheader(entry.get('titel', 'Ohne Titel'))
                with cols[1]:
                    if entry.get('status') == 'prüfen':
                        st.warning('prüfen')
                    elif entry.get('typ') == 'Upload':
                        st.success('Upload')
                    elif entry.get('typ') == 'Wikipedia':
                        st.info('Wikipedia')
                st.markdown(f"**Kurz:** {entry.get('kurz','')}")
                st.write(entry.get('inhalt',''))
                st.markdown(' '.join([f'<span class="gbc-chip">{tag}</span>' for tag in entry.get('tags', [])]), unsafe_allow_html=True)
                st.markdown(f"<div class='gbc-source'><b>Quelle:</b> {entry.get('quelle','ohne Quelle')}</div>", unsafe_allow_html=True)

    with table_tab:
        df = pd.DataFrame(results if results else all_entries)
        cols = [c for c in ['bereich','titel','kurz','quelle','typ','status'] if c in df.columns]
        st.dataframe(df[cols], use_container_width=True, hide_index=True)

with tab_wiki:
    st.subheader('Thema aus Wikipedia suchen und ins Lexikon übernehmen')
    st.caption('Die Suche nutzt die öffentliche MediaWiki-API der deutschsprachigen Wikipedia.')
    q = st.text_input('Wikipedia-Suche', placeholder='z. B. Drainage, Staude, Pflaster, Berufsbildungsgesetz')
    limit = st.slider('Trefferzahl', 3, 10, 5)

    if st.button('Wikipedia durchsuchen', type='primary', use_container_width=True) and q.strip():
        try:
            st.session_state.wiki_hits = wiki_search(q.strip(), limit=limit)
        except Exception as e:
            st.error(f'Wikipedia konnte nicht erreicht werden: {e}')

    hits = st.session_state.get('wiki_hits', [])
    for hit in hits:
        with st.container(border=True):
            st.subheader(hit['title'])
            st.write(hit.get('snippet', ''))
            if st.button(f'Zusammenfassung laden und übernehmen: {hit["title"]}', key=f'add_{hit["title"]}', use_container_width=True):
                try:
                    entry = wiki_summary(hit['title'])
                    st.session_state.wiki_extra_entries.append(entry)
                    st.success(f'„{entry["titel"]}“ wurde für diese Sitzung ergänzt.')
                    st.rerun()
                except Exception as e:
                    st.error(f'Konnte Artikel nicht laden: {e}')

with tab_upload:
    st.subheader('Eigene Unterlagen hochladen und als Lexikon-Notizen prüfen')
    st.caption('Unterstützt direkt: .txt, .md, .csv. PDF/DOCX bitte vorher als Text kopieren oder exportieren.')
    uploaded = st.file_uploader('Datei hochladen', type=['txt', 'md', 'csv'])

    if uploaded:
        text = read_uploaded_file(uploaded)
        if not text:
            st.error('Diese Datei konnte ohne Zusatzpakete nicht gelesen werden. Bitte als .txt oder .md hochladen.')
        else:
            candidates = split_uploaded_text(text, uploaded.name)
            st.info(f'{len(candidates)} mögliche Lexikon-Einträge gefunden.')

            for i, c in enumerate(candidates, start=1):
                with st.container(border=True):
                    st.caption(f"Fachbezug-Score: {c['score']} · Statusvorschlag: {c['status']}")
                    title = st.text_input('Titel', value=c['title'], key=f'up_title_{i}')
                    content = st.text_area('Inhalt prüfen/bearbeiten', value=c['content'], height=160, key=f'up_content_{i}')
                    status = st.selectbox('Status', ['geprüft', 'prüfen'], index=0 if c['status'] == 'geprüft' else 1, key=f'up_status_{i}')
                    if st.button('Diesen Eintrag speichern', key=f'save_upload_{i}', use_container_width=True):
                        save_custom_entry(title, content, c['source'], status=status)
                        st.success('Eintrag gespeichert. Er erscheint im Lexikon.')
                        st.rerun()

with tab_sources:
    st.subheader('Verwendete Quellen und Schnittstellen')
    st.markdown('**Wikipedia/MediaWiki:** Automatische Suche und Zusammenfassungen werden über die öffentliche deutschsprachige Wikipedia geladen. Bei jedem übernommenen Artikel wird die Artikel-URL als Quelle angezeigt.')
    st.divider()
    for s in LEXICON_SOURCES:
        st.markdown(f"**[{s['label']}]({s['url']})**")
        st.caption(s['note'])
    st.divider()
    st.subheader('Schnellfragen für den Chatbot')
    for question in QUICK_QUESTIONS:
        st.code(question, language=None)
