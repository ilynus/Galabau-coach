from __future__ import annotations
import sqlite3, hashlib, secrets, json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'
DB_PATH = DATA_DIR / 'galabau.db'
DATA_DIR.mkdir(exist_ok=True)


def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    with conn() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS profiles(
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            ausbildungsjahr INTEGER,
            bundesland TEXT,
            schwerpunkte TEXT,
            staerken TEXT,
            schwaechen TEXT,
            pruefungsziel TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS plants(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            deutscher_name TEXT,
            botanischer_name TEXT,
            familie TEXT,
            standort TEXT,
            boden TEXT,
            bluetezeit TEXT,
            verwendung TEXT,
            pflege TEXT,
            merkmale TEXT,
            bildpfad TEXT,
            bildquelle TEXT,
            status TEXT DEFAULT 'Entwurf',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS flashcards(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            thema TEXT,
            frage TEXT,
            antwort TEXT,
            fach TEXT,
            interval_days INTEGER DEFAULT 1,
            ease REAL DEFAULT 2.5,
            due_at TEXT DEFAULT CURRENT_TIMESTAMP,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS uploads(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT,
            category TEXT,
            note TEXT,
            path TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        ''')


def _hash(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 120_000).hex()


def create_user(username: str, password: str) -> int:
    salt = secrets.token_hex(16)
    with conn() as c:
        cur = c.execute('INSERT INTO users(username,password_hash,salt) VALUES(?,?,?)', (username, _hash(password, salt), salt))
        uid = int(cur.lastrowid)
        c.execute('INSERT INTO profiles(user_id) VALUES(?)', (uid,))
        return uid


def verify_user(username: str, password: str) -> dict[str, Any] | None:
    with conn() as c:
        row = c.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
        if row and row['password_hash'] == _hash(password, row['salt']):
            return dict(row)
    return None


def get_or_create_user(username: str, password: str) -> dict[str, Any]:
    """Erstellt oder aktualisiert einen festen Secret-User und gibt ihn zurück."""
    salt = secrets.token_hex(16)
    password_hash = _hash(password, salt)

    with conn() as c:
        row = c.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()

        if row:
            c.execute(
                'UPDATE users SET password_hash=?, salt=? WHERE username=?',
                (password_hash, salt, username),
            )
            uid = int(row['id'])
            c.execute('INSERT OR IGNORE INTO profiles(user_id) VALUES(?)', (uid,))
            return {'id': uid, 'username': username}

        cur = c.execute(
            'INSERT INTO users(username,password_hash,salt) VALUES(?,?,?)',
            (username, password_hash, salt),
        )
        uid = int(cur.lastrowid)
        c.execute('INSERT OR IGNORE INTO profiles(user_id) VALUES(?)', (uid,))
        return {'id': uid, 'username': username}


def get_profile(user_id: int) -> dict[str, Any]:
    with conn() as c:
        row = c.execute('SELECT * FROM profiles WHERE user_id=?', (user_id,)).fetchone()
        return dict(row) if row else {}


def save_profile(user_id: int, **data):
    keys = ['name','ausbildungsjahr','bundesland','schwerpunkte','staerken','schwaechen','pruefungsziel']
    vals = [data.get(k, '') for k in keys]
    with conn() as c:
        c.execute(f'''INSERT INTO profiles(user_id,{','.join(keys)}) VALUES(?,?,?,?,?,?,?,?)
        ON CONFLICT(user_id) DO UPDATE SET {','.join([k+'=excluded.'+k for k in keys])}''', [user_id, *vals])


def insert_plant(user_id: int, data: dict[str, Any]) -> int:
    keys = ['deutscher_name','botanischer_name','familie','standort','boden','bluetezeit','verwendung','pflege','merkmale','bildpfad','bildquelle','status']
    vals = [data.get(k, '') for k in keys]
    with conn() as c:
        cur = c.execute(f"INSERT INTO plants(user_id,{','.join(keys)}) VALUES({','.join(['?']*(len(keys)+1))})", [user_id, *vals])
        return int(cur.lastrowid)


def list_plants(user_id: int):
    with conn() as c:
        return [dict(r) for r in c.execute('SELECT * FROM plants WHERE user_id=? ORDER BY created_at DESC', (user_id,))]


def insert_flashcard(user_id: int, thema: str, frage: str, antwort: str, fach: str='Allgemein'):
    with conn() as c:
        c.execute('INSERT INTO flashcards(user_id,thema,frage,antwort,fach) VALUES(?,?,?,?,?)', (user_id,thema,frage,antwort,fach))


def list_flashcards(user_id: int, fach: str | None = None):
    with conn() as c:
        if fach:
            return [dict(r) for r in c.execute('SELECT * FROM flashcards WHERE user_id=? AND fach=? ORDER BY created_at DESC', (user_id, fach))]
        return [dict(r) for r in c.execute('SELECT * FROM flashcards WHERE user_id=? ORDER BY created_at DESC', (user_id,))]
