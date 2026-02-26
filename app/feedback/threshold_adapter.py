import sqlite3

DB_PATH = "feedback.db"

def calculate_accuracy():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT predicted_action, human_action
    FROM ticket_logs
    WHERE human_action IS NOT NULL
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return 1.0

    correct = sum(1 for p, h in rows if p == h)
    return correct / len(rows)


def adjust_threshold(current_threshold):
    accuracy = calculate_accuracy()

    # If accuracy low → increase threshold (be safer)
    if accuracy < 0.7:
        return min(current_threshold + 0.05, 0.9)

    # If accuracy very high → allow more auto decisions
    if accuracy > 0.9:
        return max(current_threshold - 0.05, 0.5)

    return current_threshold