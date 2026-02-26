def calculate_confidence(intent_conf, urgency_conf):
    return round((intent_conf + urgency_conf) / 2, 3)