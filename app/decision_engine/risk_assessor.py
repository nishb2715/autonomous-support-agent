HIGH_RISK_INTENTS = [
    "billing_fraud"
]

HIGH_RISK_KEYWORDS = [
    "fraud",
    "unauthorized",
    "legal",
    "lawsuit",
    "data breach"
]

def assess_risk(intent, ticket_text):
    text_lower = ticket_text.lower()

    if intent in HIGH_RISK_INTENTS:
        return 0.9

    for word in HIGH_RISK_KEYWORDS:
        if word in text_lower:
            return 0.8

    return 0.2