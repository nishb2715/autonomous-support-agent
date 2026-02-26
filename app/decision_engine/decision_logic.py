from .risk_assessor import assess_risk

AUTO_RESOLVABLE_INTENTS = [
    "refund_request",
    "login_issue",
    "subscription_cancel"
]

CONFIDENCE_THRESHOLD = 0.65
HIGH_RISK_THRESHOLD = 0.75

def decide_action(intent, urgency, confidence, ticket_text, retrieved_docs):
    risk_score = assess_risk(intent, ticket_text)

    reasoning = []

    # 1. High urgency always escalates
    if urgency == "critical":
        reasoning.append("Critical urgency detected")
        return build_decision("ESCALATE", reasoning, risk_score)

    # 2. High risk content escalates
    if risk_score >= HIGH_RISK_THRESHOLD:
        reasoning.append("High risk detected")
        return build_decision("ESCALATE", reasoning, risk_score)

    # 3. Low confidence → ask clarification
    if confidence < CONFIDENCE_THRESHOLD:
        reasoning.append("Low model confidence")
        return build_decision("ASK_CLARIFICATION", reasoning, risk_score)

    # 4. Auto resolvable intents
    if intent in AUTO_RESOLVABLE_INTENTS:
        reasoning.append("Intent eligible for auto resolution")
        return build_decision("AUTO_RESOLVE", reasoning, risk_score)

    # 5. Default fallback
    reasoning.append("Default escalation fallback")
    return build_decision("ESCALATE", reasoning, risk_score)


def build_decision(action, reasoning, risk_score):
    return {
        "action": action,
        "reasoning": reasoning,
        "risk_score": risk_score
    }