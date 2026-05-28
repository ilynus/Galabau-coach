# Login-Fix

Diese ZIP ist die ursprüngliche App, aber repariert.

Behoben:
- `ModuleNotFoundError: No module named 'src.auth'`
- Admin-Login über Streamlit Secrets
- normaler Registrieren/Login-Flow bleibt erhalten

## In Streamlit Secrets eintragen

ADMIN_USER = "admin"
ADMIN_PASSWORD = "NEUES_PASSWORT_HIER"
USER_ID = "admin"

Bitte ein neues Passwort verwenden.

## Streamlit Main file path

galabau_ai/app.py

## GitHub

Den kompletten Ordner `galabau_ai` aus dieser ZIP hochladen bzw. die alte Version ersetzen.
