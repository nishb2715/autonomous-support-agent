import sqlite3
import os

DB_PATH = "feedback.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_text TEXT,
        predicted_intent TEXT,
        predicted_urgency TEXT,
        confidence REAL,
        predicted_action TEXT,
        human_action TEXT,
        was_correct INTEGER
    )
    """)

    conn.commit()
    conn.close()


def log_prediction(ticket_text, intent, urgency, confidence, action):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ticket_logs
    (ticket_text, predicted_intent, predicted_urgency, confidence, predicted_action, human_action, was_correct)
    VALUES (?, ?, ?, ?, ?, NULL, NULL)
    """, (ticket_text, intent, urgency, confidence, action))

    ticket_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return ticket_id


def log_human_feedback(ticket_id, human_action):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE ticket_logs
    SET human_action = ?
    WHERE id = ?
    """, (human_action, ticket_id))

    conn.commit()
    conn.close()