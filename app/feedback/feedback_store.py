import sqlite3

DB_PATH = "feedback.db"


#initialize database

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
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


#log prediction using main agent pipeline 

def log_prediction(customer_id, ticket_text, intent, urgency, confidence, action):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ticket_logs
    (customer_id, ticket_text, predicted_intent, predicted_urgency, confidence, predicted_action, human_action, was_correct)
    VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)
    """, (customer_id, ticket_text, intent, urgency, confidence, action))

    ticket_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return ticket_id


#human feedback logging fn 

def log_human_feedback(ticket_id, human_action):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get predicted action
    cursor.execute("""
    SELECT predicted_action FROM ticket_logs WHERE id = ?
    """, (ticket_id,))

    row = cursor.fetchone()

    if not row:
        conn.close()
        return

    predicted_action = row[0]

    # Determine correctness
    was_correct = 1 if predicted_action == human_action else 0

    # Update record
    cursor.execute("""
    UPDATE ticket_logs
    SET human_action = ?, was_correct = ?
    WHERE id = ?
    """, (human_action, was_correct, ticket_id))

    conn.commit()
    conn.close()


#long term memory retrieval fn

def get_customer_history(customer_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT ticket_text, predicted_action
    FROM ticket_logs
    WHERE customer_id = ?
    ORDER BY id DESC
    LIMIT 5
    """, (customer_id,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No previous history."

    history = ""
    for ticket, action in rows:
        history += f"Previous Ticket: {ticket}\nAction Taken: {action}\n\n"

    return history.strip()