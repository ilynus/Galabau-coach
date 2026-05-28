import streamlit as st
from src.theme import apply_theme
from src.auth import require_login, sidebar_user
from src.gamification import stats, BADGES, ACTIVITIES, add_daily_checkin

st.set_page_config(page_title='Lernfortschritt', page_icon='🏆', layout='wide')
apply_theme()
user = require_login(); sidebar_user()

game = stats(user['id'])
progress_percent = int(game['progress'] * 100)

st.markdown(
    f"""
    <div class="gbc-premium-hero">
      <div class="gbc-hero-grid">
        <div>
          <div class="gbc-eyebrow">Gamification</div>
          <h1>🏆 Dein Lernfortschritt</h1>
          <p>Sammle Punkte, halte deine Lernserie und schalte Badges frei.</p>
        </div>
        <div class="gbc-glass">
          <div style="font-weight:900;font-size:1.05rem;">Level {game['level']} · {game['points']} Punkte</div>
          <div class="gbc-progress-track"><div class="gbc-progress-fill" style="width:{progress_percent}%"></div></div>
          <div style="font-size:.86rem;opacity:.86;">Noch {max(0, game['next']-game['points'])} Punkte bis Level {game['level']+1}</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)
c1.metric('Punkte', game['points'])
c2.metric('Level', game['level'])
c3.metric('Streak', f"{game['streak']} Tage")

if st.button('🔥 Heutigen Lern-Check-in sichern', type='primary', use_container_width=True):
    gained = add_daily_checkin(user['id'])
    if gained:
        st.success(f'Check-in gespeichert. +{gained} Punkte')
    else:
        st.info('Heute schon erledigt.')

st.subheader('Badges')
earned_ids = {b['id'] for b in game['badges']}
cols = st.columns(3)
for i, badge in enumerate(BADGES):
    with cols[i % 3]:
        unlocked = badge['id'] in earned_ids
        st.markdown(
            f"""
            <div class="gbc-dashboard-card" style="opacity:{'1' if unlocked else '.55'}">
              <div style="font-size:2rem;">{badge['emoji']}</div>
              <h3>{badge['name']}</h3>
              <p>{badge['desc']}</p>
              <b>{'Freigeschaltet' if unlocked else 'Noch offen'}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.subheader('So bekommst du Punkte')
for key, info in ACTIVITIES.items():
    st.markdown(
        f"""
        <div class="gbc-quest">
          <div class="gbc-quest-emoji">{info['emoji']}</div>
          <div>
            <div class="gbc-quest-title">{info['label']}</div>
            <div class="gbc-quest-sub">+{info['points']} Punkte</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader('Letzte Aktivitäten')
if game['recent']:
    for e in game['recent']:
        st.write(f"{e['emoji']} **{e['label']}** · +{e['points']} Punkte · {e['created_at']}")
else:
    st.info('Noch keine Aktivitäten.')
