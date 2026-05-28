import streamlit as st
from sqlite3 import IntegrityError
from .db import init_db, create_user, verify_user


def _admin_login(username: str, password: str):
    """Optionaler Admin-Login über Streamlit Secrets."""
    admin_user = st.secrets.get("ADMIN_USER", None)
    admin_password = st.secrets.get("ADMIN_PASSWORD", None)

    if admin_user and admin_password:
        if username == str(admin_user).strip() and password == str(admin_password):
            return {"id": st.secrets.get("USER_ID", "admin"), "username": username, "role": "admin"}

    return None


def require_login():
    init_db()
    if 'user' not in st.session_state:
        st.session_state.user = None
    if st.session_state.user:
        return st.session_state.user

    st.markdown(
        """
        <div class="gbc-hero">
            <h1>🌿 GaLaBau Coach</h1>
            <p>Lernplattform, Pflanzenbuch und Nachschlagewerk für deine Ausbildung im Garten- und Landschaftsbau.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_login, tab_register = st.tabs(['Einloggen', 'Registrieren'])
    with tab_login:
        username = st.text_input('Benutzername', key='login_user')
        password = st.text_input('Passwort', type='password', key='login_pw')
        if st.button('Einloggen', type='primary', use_container_width=True):
            username_clean = username.strip()

            admin = _admin_login(username_clean, password)
            if admin:
                st.session_state.user = admin
                st.rerun()

            user = verify_user(username_clean, password)
            if user:
                st.session_state.user = {'id': user['id'], 'username': user['username'], 'role': 'user'}
                st.rerun()
            st.error('Login fehlgeschlagen. Prüfe Benutzername und Passwort oder erstelle einen neuen Account.')
    with tab_register:
        new_user = st.text_input('Neuer Benutzername')
        new_pw = st.text_input('Neues Passwort', type='password')
        if st.button('Account erstellen', use_container_width=True):
            if not new_user.strip():
                st.warning('Bitte einen Benutzernamen eingeben.')
            elif len(new_pw) < 6:
                st.warning('Bitte mindestens 6 Zeichen verwenden.')
            else:
                try:
                    uid = create_user(new_user.strip(), new_pw)
                    st.session_state.user = {'id': uid, 'username': new_user.strip(), 'role': 'user'}
                    st.rerun()
                except IntegrityError:
                    st.error('Benutzername ist bereits vergeben.')
    st.stop()


def sidebar_user():
    user = st.session_state.get('user')
    if user:
        st.sidebar.markdown(
            f"""
            <div class="gbc-brand">
              <div class="gbc-brand-title">🌿 GaLaBau Coach</div>
              <div class="gbc-brand-sub">Lernen · Pflanzen · Baustelle</div>
            </div>
            <div class="gbc-user-card">
              <strong>{'🛡️' if user.get('role') == 'admin' else '👤'} {user['username']}</strong>
              <small>angemeldet</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.sidebar.button('🚪 Abmelden', use_container_width=True):
            st.session_state.user = None
            st.rerun()
        st.sidebar.divider()
        st.sidebar.caption('Tipp: Im Lexikon findest du kurze, quellenbasierte Lernnotizen.')
