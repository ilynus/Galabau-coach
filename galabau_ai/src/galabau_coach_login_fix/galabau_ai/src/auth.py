import streamlit as st
from sqlite3 import IntegrityError
from .db import init_db, create_user, verify_user


def _admin_login(username: str, password: str):
    """Prüft festen Admin-Login über Streamlit Secrets."""
    admin_user = st.secrets.get("ADMIN_USER", None)
    admin_password = st.secrets.get("ADMIN_PASSWORD", None)

    if admin_user and admin_password:
        if username == str(admin_user).strip() and password == str(admin_password):
            return {"id": st.secrets.get("USER_ID", "admin"), "username": username}

    return None


def require_login():
    init_db()

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        return st.session_state.user

    st.title("🌿 GaLaBau Coach")
    st.caption("Lernplattform für die Ausbildung im Garten- und Landschaftsbau")

    tab_login, tab_register = st.tabs(["Einloggen", "Registrieren"])

    with tab_login:
        username = st.text_input("Benutzername", key="login_user")
        password = st.text_input("Passwort", type="password", key="login_pw")

        if st.button("Einloggen", type="primary"):
            username_clean = username.strip()

            # 1. Fester Admin-Login aus Streamlit Secrets
            admin_user = _admin_login(username_clean, password)
            if admin_user:
                st.session_state.user = admin_user
                st.rerun()

            # 2. Normaler Login über Datenbank
            user = verify_user(username_clean, password)
            if user:
                st.session_state.user = {
                    "id": user["id"],
                    "username": user["username"],
                }
                st.rerun()

            st.error("Login fehlgeschlagen.")

    with tab_register:
        new_user = st.text_input("Neuer Benutzername")
        new_pw = st.text_input("Neues Passwort", type="password")

        if st.button("Account erstellen"):
            if len(new_pw) < 6:
                st.warning("Bitte mindestens 6 Zeichen verwenden.")
            else:
                try:
                    uid = create_user(new_user.strip(), new_pw)
                    st.session_state.user = {
                        "id": uid,
                        "username": new_user.strip(),
                    }
                    st.rerun()
                except IntegrityError:
                    st.error("Benutzername ist bereits vergeben.")

    st.stop()


def sidebar_user():
    user = st.session_state.get("user")

    if user:
        st.sidebar.success(f"Angemeldet als {user['username']}")

        if st.sidebar.button("Abmelden"):
            st.session_state.user = None
            st.rerun()
