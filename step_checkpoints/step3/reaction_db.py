# reaction_db.py
# The Typing Sprint's database functions.
# Programs import what they need from this file.

import sqlite3
from datetime import datetime

DB_FILE = "reactions.db"


# ----- functions from Class 1 (complete) -----


def create_table():
    connection = sqlite3.connect(DB_FILE)
    connection.execute("""CREATE TABLE IF NOT EXISTS reactions (
        id INTEGER PRIMARY KEY,
        stamp TEXT,
        seconds REAL NOT NULL,
        player TEXT NOT NULL DEFAULT 'guest',
        UNIQUE (stamp, seconds)
    )""")
    connection.commit()
    connection.close()


def add_reaction(seconds, player="guest"):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        connection = sqlite3.connect(DB_FILE)
        connection.execute("INSERT INTO reactions (stamp, seconds, player) VALUES (?, ?, ?)",
                           (stamp, seconds, player))
        connection.commit()
        connection.close()
    except sqlite3.Error:
        print("Could not save this round.")
        return False
    return True


def import_log(filename, player="guest"):
    imported = 0
    damaged = 0
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("No log file to import.")
        return 0, 0
    connection = sqlite3.connect(DB_FILE)
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) != 2:
            damaged = damaged + 1
            continue
        try:
            seconds = float(parts[1])
        except ValueError:
            damaged = damaged + 1
            continue
        cursor = connection.execute(
            "INSERT OR IGNORE INTO reactions (stamp, seconds, player) VALUES (?, ?, ?)",
            (parts[0], seconds, player))
        imported = imported + cursor.rowcount
    connection.commit()
    connection.close()
    return imported, damaged


def summary():
    connection = sqlite3.connect(DB_FILE)
    row = connection.execute(
        "SELECT COUNT(*), MIN(seconds), MAX(seconds), AVG(seconds) FROM reactions").fetchone()
    connection.close()
    if row[0] == 0:
        return None
    return row


def fastest(count):
    connection = sqlite3.connect(DB_FILE)
    rows = connection.execute(
        "SELECT seconds, stamp FROM reactions ORDER BY seconds LIMIT ?", (count,)).fetchall()
    connection.close()
    return rows


def rounds_since(day):
    connection = sqlite3.connect(DB_FILE)
    count = connection.execute(
        "SELECT COUNT(*) FROM reactions WHERE stamp >= ?", (day,)).fetchone()[0]
    connection.close()
    return count


# ----- functions written in this lab -----


def valid_player(name):
    return 3 <= len(name) <= 15 and name.isalnum()


def player_summary(player):
    connection = sqlite3.connect(DB_FILE)
    row = connection.execute(
        "SELECT COUNT(*), MIN(seconds), MAX(seconds), AVG(seconds) FROM reactions WHERE player = ?",
        (player,)).fetchone()
    connection.close()
    if row[0] == 0:
        return None
    return row


# Step 4: write leaderboard() here.


# Step 5: write rename_player and delete_player() here.
