import random
import pandas as pd

intents = {
    "refund_request": [
        "I want a refund for my order",
        "Please return my money",
        "Refund my recent purchase"
    ],
    "login_issue": [
        "I cannot login",
        "Password reset not working",
        "My account is locked"
    ],
    "bug_report": [
        "The app crashes",
        "Dashboard is broken",
        "Payment page not loading"
    ],
    "billing_fraud": [
        "Unauthorized charge on my card",
        "Fraudulent transaction detected",
        "Unknown payment from my account"
    ],
    "subscription_cancel": [
        "Cancel my subscription",
        "Stop auto renewal",
        "I want to end my plan"
    ]
}

urgency_map = {
    "refund_request": "medium",
    "login_issue": "medium",
    "bug_report": "high",
    "billing_fraud": "critical",
    "subscription_cancel": "low"
}

data = []

for intent, examples in intents.items():
    for _ in range(150):
        text = random.choice(examples)
        data.append({
            "ticket_text": text,
            "intent": intent,
            "urgency": urgency_map[intent]
        })

df = pd.DataFrame(data)
df.to_csv("tickets.csv", index=False)
print("Dataset generated.")