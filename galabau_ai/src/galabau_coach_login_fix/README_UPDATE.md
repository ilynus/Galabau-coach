# GaLaBau Coach Login-Fix

Diese ZIP enthält die überarbeitete Datei:

galabau_ai/src/auth.py

Änderung:
- Der Login prüft jetzt zuerst den festen Admin-Login aus Streamlit Secrets:
  - ADMIN_USER
  - ADMIN_PASSWORD
  - USER_ID optional
- Danach funktioniert weiterhin der normale Datenbank-Login über Registrierung.

Einbau:
1. In GitHub öffnen: galabau_ai/src/auth.py
2. Datei komplett durch die Version aus dieser ZIP ersetzen.
3. Commit changes klicken.
4. Streamlit-App neu starten.

Wichtig:
Das Passwort aus dem Screenshot sollte in Streamlit Secrets geändert werden.
