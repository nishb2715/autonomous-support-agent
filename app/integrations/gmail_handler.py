import base64
import os
from email import message_from_bytes
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from app.agent_pipeline import process_ticket_pipeline


# allowing reading inbox mails and sending reply emails
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

MAX_EMAIL_LENGTH = 1000


#connecting to gmail api using oauth2 flow and creating service object

def get_gmail_service():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    return service


#send reply of the email fn 

def send_email_reply(service, to_email, subject, message_text):

    message = MIMEText(message_text)

    message["to"] = to_email
    message["subject"] = "Re: " + subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    body = {"raw": raw_message}

    service.users().messages().send(
        userId="me",
        body=body
    ).execute()


#reading emails fn 

def check_emails():

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        print("No new emails.")
        return

    for msg in messages:

        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="raw"
        ).execute()

        raw_msg = base64.urlsafe_b64decode(msg_data["raw"].encode("ASCII"))

        email_message = message_from_bytes(raw_msg)

        sender = email_message.get("from", "unknown_sender")
        subject = email_message.get("subject", "")

        body = ""

        #fn to extract body from email 

        if email_message.is_multipart():

            for part in email_message.walk():
                if part.get_content_type() == "text/plain":

                    try:
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
                    except:
                        pass

        else:

            try:
                body = email_message.get_payload(decode=True).decode(errors="ignore")
            except:
                body = ""

        #cleaning body text

        body = body.replace("\n", " ").replace("\r", " ").strip()

        body = body[:MAX_EMAIL_LENGTH]

        #fn to filter promotional and v short emails 

        promo_keywords = [
            "unsubscribe",
            "newsletter",
            "promotion",
            "linkedin",
            "extern",
            "careerbrew",
            "marketing"
        ]

        if any(k in body.lower() for k in promo_keywords):
            print("Skipping promotional email")
            continue

        if len(body) < 10:
            print("Skipping empty email")
            continue

        print("\n📩 New Email Received")
        print("From:", sender)
        print("Subject:", subject)
        print("Body:", body)

        #creating tiicket text 

        ticket_text = f"{subject}\n{body}"

        try:

            result = process_ticket_pipeline(sender, ticket_text)

            reply = result["response"]["response_message"]

            print("\n🤖 AI Response:")
            print(reply)

            # send reply email
            send_email_reply(service, sender, subject, reply)

            print("📤 Reply email sent")

        except Exception as e:

            print("Error processing email:", str(e))