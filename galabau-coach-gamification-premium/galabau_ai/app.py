import streamlit as st
from src.theme import apply_theme
from src.auth import require_login, sidebar_user
from src.db import init_db, get_profile
from src.lexicon_data import LEXICON, QUICK_QUESTIONS
from src.dynamic_lexicon import load_custom_entries
from src.gamification import init_gamification_db, stats, add_daily_checkin

st.set_page_config(page_title='GaLaBau Coach', page_icon='🌿', layout='wide')
apply_theme()
init_db()
init_gamification_db()
user = require_login()
sidebar_user()
profile = get_profile(user['id'])

if st.session_state.get("daily_checkin_done") is None:
    gained = add_daily_checkin(user['id'])
    st.session_state.daily_checkin_done = True
    if gained:
        st.toast(f"🔥 Täglicher Check-in: +{gained} Punkte")

game = stats(user['id'])
progress_percent = int(game["progress"] * 100)
custom_count = len(load_custom_entries())

st.markdown(
    f"""
    <div class="gbc-premium-hero">
      <div class="gbc-hero-grid">
        <div>
          <div class="gbc-eyebrow">Ausbildungs-Dashboard</div>
          <h1>🌿 Willkommen zurück, {user['username']}!</h1>
          <p>Trainiere Pflanzenkunde, Baustellenwissen, WIPO und Prüfungsthemen – mit Lexikon, Enzyklopädie und Lernfortschritt.</p>
        </div>
        <div class="gbc-glass">
          <div style="font-weight:900;font-size:1.05rem;">Level {game['level']} · {game['points']} Punkte</div>
          <div class="gbc-progress-track"><div class="gbc-progress-fill" style="width:{progress_percent}%"></div></div>
          <div style="font-size:.86rem;opacity:.86;">{game['points']} / {game['next']} Punkte bis zum nächsten Level</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"<div class='gbc-dashboard-card'><div class='gbc-mini-label'>Level</div><div class='gbc-big-number'>{game['level']}</div><p>Dein aktueller Lernrang</p></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='gbc-dashboard-card'><div class='gbc-mini-label'>Punkte</div><div class='gbc-big-number'>{game['points']}</div><p>Gesammelte Lern-XP</p></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='gbc-dashboard-card'><div class='gbc-mini-label'>Streak</div><div class='gbc-big-number'>{game['streak']}🔥</div><p>Tage Lernserie</p></div>", unsafe_allow_html=True)
with m4:
    st.markdown(f"<div class='gbc-dashboard-card'><div class='gbc-mini-label'>Lexikon</div><div class='gbc-big-number'>{len(LEXICON)+custom_count}</div><p>Einträge + Uploads</p></div>", unsafe_allow_html=True)

st.divider()

st.subheader("Heute sinnvoll weitermachen")
a1, a2, a3 = st.columns(3)
with a1:
    st.markdown("""
    <div class="gbc-action-card">
      <div class="gbc-action-icon">📚</div>
      <h3>Lexikon vertiefen</h3>
      <p>Suche nach Pflaster, Boden, Pflanzen oder Prüfungsbegriffen.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/6_Themenbibliothek.py", label="Zur Themenbibliothek", icon="📚", use_container_width=True)
with a2:
    st.markdown("""
    <div class="gbc-action-card">
      <div class="gbc-action-icon">🤖</div>
      <h3>Chatbot fragen</h3>
      <p>Lass dir Themen prüfungsnah erklären und Beispiele erstellen.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Chatbot.py", label="Zum Chatbot", icon="🤖", use_container_width=True)
with a3:
    st.markdown("""
    <div class="gbc-action-card">
      <div class="gbc-action-icon">🃏</div>
      <h3>Karteikarten lernen</h3>
      <p>Wiederhole Fachbegriffe und baue kleine Lernroutinen auf.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/5_Karteikarten.py", label="Zu den Karteikarten", icon="🃏", use_container_width=True)

st.subheader("Deine Quests")
quests = [
    ("👤", "Profil vervollständigen", "Fülle Ausbildungsjahr, Bundesland und Interessen aus.", "pages/1_Profil.py"),
    ("🌐", "Ein Thema aus Wikipedia ergänzen", "Übernimm einen passenden Artikel in dein Lexikon.", "pages/6_Themenbibliothek.py"),
    ("📝", "Eigene Unterlage prüfen", "Lade eine .txt/.md Lernnotiz hoch und speichere einen geprüften Eintrag.", "pages/6_Themenbibliothek.py"),
]
for emoji, title, desc, page in quests:
    st.markdown(
        f"""
        <div class="gbc-quest">
          <div class="gbc-quest-emoji">{emoji}</div>
          <div>
            <div class="gbc-quest-title">{title}</div>
            <div class="gbc-quest-sub">{desc}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

left, right = st.columns([1, 1])
with left:
    st.subheader("Badges")
    if game["badges"]:
        st.markdown(" ".join([f"<span class='gbc-badge'>{b['emoji']} {b['name']}</span>" for b in game["badges"][:8]]), unsafe_allow_html=True)
    else:
        st.info("Sammle deine ersten Punkte, um Badges freizuschalten.")
with right:
    st.subheader("Letzte Aktivitäten")
    if game["recent"]:
        for e in game["recent"][:5]:
            st.markdown(f"**{e['emoji']} {e['label']}** · +{e['points']} Punkte")
    else:
        st.info("Noch keine Aktivitäten.")

st.subheader("Beispielfragen")
cols = st.columns(3)
for i, question in enumerate(QUICK_QUESTIONS[:3]):
    with cols[i]:
        st.info(question)

st.markdown(
    """
    <div class="gbc-callout">
    <b>Hinweis:</b> Lexikon- und Enzyklopädie-Inhalte sind Lernnotizen. Normen, VOB/B, BBiG/BGB-Fragen,
    Pflanzenschutz und Prüfungsanforderungen bitte immer mit aktueller Originalquelle,
    Unterrichtsmaterial oder Ausbilder/in abgleichen.
    </div>
    """,
    unsafe_allow_html=True,
)
