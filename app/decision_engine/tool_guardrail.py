def enforce_tool_rules(intent, decision):

    if intent == "billing_issue":
        decision["tool"] = "process_refund"

    if intent == "password_reset":
        decision["tool"] = "reset_password"

    if intent == "account_compromised":
        decision["tool"] = "lock_account"

    return decision