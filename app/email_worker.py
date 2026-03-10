import time
from app.integrations.gmail_handler import check_emails

print("Gmail worker started...")

while True:
    try:
        check_emails()
    except Exception as e:
        print("Error checking emails:", e)

    # wait 60 seconds before checking again
    time.sleep(60)