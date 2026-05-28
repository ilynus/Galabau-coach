"""Gamification-System für den GaLaBau Coach.

Speichert Lernpunkte, Streaks, Badges und erledigte Aktivitäten lokal in SQLite.
"""
from __future__ import annotations

import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

DB_PATH = Path("galabau_coach.db")

ACTIVITIES = {
    "profile_update": {"points": 20, "label": "Profil gepflegt", "emoji": "👤"},
    "chat_question": {"points": 10, "label": "Chatbot-Frage gestellt", "emoji": "🤖"},
    "lexicon_search": {"points": 5, "label": "Lexikon genutzt", "emoji": "📚"},
    "wiki_added": {"points": 20, "label": "Wikipedia-Thema ergänzt", "emoji": "🌐"},
    "upload_entry": {"points": 30, "label": "Eigene Notiz geprüft", "emoji": "📝"},
    "flashcard_session": {"points": 15, "label": "Karteikarten gelernt", "emoji": "🃏"},
    "plant_entry": {"points": 25, "label": "Pflanzenbuch erweitert", "emoji": "🌱"},
    "daily_checkin": {"points": 10, "label": "Täglicher Lern-Check-in", "emoji": "🔥"},
}

BADGES = [
    {"id": "starter", "name": "Starter", "emoji": "🌱", "points": 10, "desc": "Erste Lernpunkte gesammelt."},
    {"id": "profil_profi", "name": "Profil-Profi", "emoji": "👤", "activity": "profile_update", "count": 1, "desc": "Ausbildungsprofil angelegt."},
    {"id": "wissenssucher", "name": "Wissenssucher", "emoji": "🔎", "activity": "lexicon_search", "count": 5, "desc": "Fünfmal im Lexikon recherchiert."},
    {"id": "baustellen_denker", "name": "Baustellen-Denker", "emoji": "🏗️", "activity": "chat_question", "count": 5, "desc": "Fünf Lernfragen gestellt."},
    {"id": "pflanzenfreund", "name": "Pflanzenfreund", "emoji": "🌿", "activity": "plant_entry", "count": 3, "desc": "Drei Pflanzenbucheinträge erstellt."},
    {"id": "notizmeister", "name": "Notizmeister", "emoji": "📝", "activity": "upload_entry", "count": 3, "desc": "Drei eigene Notizen geprüft."},
    {"id": "lexikon_bauer", "name": "Lexikon-Bauer", "emoji": "📚", "activity": "wiki_added", "count": 3, "desc": "Drei Themen ergänzt."},
    {"id": "durchstarter", "name": "Durchstarter", "emoji": "🚀", "points": 150, "desc": "150 Lernpunkte erreicht."},
    {"id": "meisterschueler", "name": "Meisterschüler", "emoji": "🏆", "points": 400, "desc": "400 Lernpunkte erreicht."},
    {"id": "streak_3", "name": "3-Tage-Serie", "emoji": "🔥", "streak": 3, "desc": "Drei Tage hintereinander gelernt."},
]


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_gamification_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS gamification_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            activity TEXT NOT NULL,
            points INTEGER NOT NULL,
            created_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS gamification_badges (
            user_id TEXT NOT NULL,
            badge_id TEXT NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, badge_id)
        )
        """
    )
    conn.commit()
    conn.close()


def add_event(user_id, activity: str, points: int | None = None):
    init_gamification_db()
    info = ACTIVITIES.get(activity, {"points": 5})
    pts = int(points if points is not None else info["points"])
    today = date.today().isoformat()

    conn = _conn()
    conn.execute(
        "INSERT INTO gamification_events (user_id, activity, points, created_date) VALUES (?, ?, ?, ?)",
        (str(user_id), activity, pts, today),
    )
    conn.commit()
    conn.close()
    update_badges(user_id)
    return pts


def add_daily_checkin(user_id):
    init_gamification_db()
    today = date.today().isoformat()
    conn = _conn()
    exists = conn.execute(
        "SELECT 1 FROM gamification_events WHERE user_id=? AND activity='daily_checkin' AND created_date=?",
        (str(user_id), today),
    ).fetchone()
    conn.close()
    if exists:
        return 0
    return add_event(user_id, "daily_checkin")


def total_points(user_id) -> int:
    init_gamification_db()
    conn = _conn()
    row = conn.execute(
        "SELECT COALESCE(SUM(points), 0) AS points FROM gamification_events WHERE user_id=?",
        (str(user_id),),
    ).fetchone()
    conn.close()
    return int(row["points"])


def activity_count(user_id, activity: str) -> int:
    init_gamification_db()
    conn = _conn()
    row = conn.execute(
        "SELECT COUNT(*) AS c FROM gamification_events WHERE user_id=? AND activity=?",
        (str(user_id), activity),
    ).fetchone()
    conn.close()
    return int(row["c"])


def streak_days(user_id) -> int:
    init_gamification_db()
    conn = _conn()
    rows = conn.execute(
        "SELECT DISTINCT created_date FROM gamification_events WHERE user_id=? ORDER BY created_date DESC",
        (str(user_id),),
    ).fetchall()
    conn.close()
    dates = {date.fromisoformat(r["created_date"]) for r in rows}
    if not dates:
        return 0
    today = date.today()
    # If no activity today, count from yesterday.
    start = today if today in dates else today - timedelta(days=1)
    streak = 0
    d = start
    while d in dates:
        streak += 1
        d -= timedelta(days=1)
    return streak


def level_for_points(points: int):
    # Every level needs more points; simple and motivational.
    thresholds = [0, 50, 120, 220, 350, 520, 750, 1050, 1400, 1850]
    level = 1
    for i, t in enumerate(thresholds, start=1):
        if points >= t:
            level = i
    current = thresholds[level - 1]
    nxt = thresholds[level] if level < len(thresholds) else thresholds[-1] + 500
    progress = min(1.0, (points - current) / max(1, nxt - current))
    return {"level": level, "current": current, "next": nxt, "progress": progress}


def update_badges(user_id):
    init_gamification_db()
    pts = total_points(user_id)
    streak = streak_days(user_id)
    earned = set(b["id"] for b in earned_badges(user_id))
    conn = _conn()

    for badge in BADGES:
        ok = False
        if "points" in badge and pts >= badge["points"]:
            ok = True
        if "streak" in badge and streak >= badge["streak"]:
            ok = True
        if "activity" in badge and activity_count(user_id, badge["activity"]) >= badge.get("count", 1):
            ok = True
        if ok and badge["id"] not in earned:
            conn.execute(
                "INSERT OR IGNORE INTO gamification_badges (user_id, badge_id) VALUES (?, ?)",
                (str(user_id), badge["id"]),
            )

    conn.commit()
    conn.close()


def earned_badges(user_id):
    init_gamification_db()
    conn = _conn()
    rows = conn.execute(
        "SELECT badge_id, earned_at FROM gamification_badges WHERE user_id=? ORDER BY earned_at DESC",
        (str(user_id),),
    ).fetchall()
    conn.close()
    by_id = {b["id"]: b for b in BADGES}
    result = []
    for r in rows:
        badge = dict(by_id.get(r["badge_id"], {"id": r["badge_id"], "name": r["badge_id"], "emoji": "🏅", "desc": ""}))
        badge["earned_at"] = r["earned_at"]
        result.append(badge)
    return result


def recent_events(user_id, limit=8):
    init_gamification_db()
    conn = _conn()
    rows = conn.execute(
        "SELECT activity, points, created_at FROM gamification_events WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
        (str(user_id), limit),
    ).fetchall()
    conn.close()
    events = []
    for r in rows:
        info = ACTIVITIES.get(r["activity"], {"label": r["activity"], "emoji": "✨"})
        events.append({"activity": r["activity"], "label": info["label"], "emoji": info["emoji"], "points": r["points"], "created_at": r["created_at"]})
    return events


def stats(user_id):
    update_badges(user_id)
    pts = total_points(user_id)
    lvl = level_for_points(pts)
    return {
        "points": pts,
        "level": lvl["level"],
        "progress": lvl["progress"],
        "current": lvl["current"],
        "next": lvl["next"],
        "streak": streak_days(user_id),
        "badges": earned_badges(user_id),
        "recent": recent_events(user_id),
    }
