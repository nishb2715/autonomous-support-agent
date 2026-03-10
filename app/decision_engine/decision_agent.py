import os
import json
from dotenv import load_dotenv
from groq import Groq

#initialize environment variables
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

#llm decision agent function

def llm_decide_action(ticket_text, intent, urgency, confidence, retrieved_docs, history):

    # rag

    context = "\n\n".join(
        [doc["content"] for doc in retrieved_docs]
    )

    #convo context 

    conversation_context = ""

    if history:

        lines = []

        for msg in history:

            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
                lines.append(f"{role}: {content}")

            else:
                lines.append(str(msg))

        conversation_context = "\n".join(lines)

    else:
        conversation_context = "No previous conversation."
    #syste prompt for the decision agent

    system_prompt = """
You are an intelligent customer support decision agent.

You must choose ONE of the following actions:

AUTO_RESOLVE
ASK_CLARIFICATION
ESCALATE

You may optionally select ONE tool:

lock_account
unlock_account
reset_password
verify_identity
process_refund
issue_partial_refund
cancel_subscription
check_subscription_status
apply_discount
check_order_status
resend_invoice
update_shipping_address
flag_suspicious_activity
temporarily_suspend_account
mark_case_high_priority
escalate_ticket

Rules:

1. Ask clarification only if the problem is unclear.
2. Do NOT ask more than 2 clarifying questions.
3. If the user already provided enough context, choose AUTO_RESOLVE.
4. Duplicate charges, billing issues, refunds → AUTO_RESOLVE using process_refund.
5. Password issues → use reset_password.
6. Order status queries → use check_order_status.
7. Account lockouts → use unlock_account.
8. Fraud, hacking, suspicious activity → ESCALATE or lock_account.
9. If urgency is critical → escalate.

Return STRICT JSON ONLY in this format:

{
 "action": "...",
 "reasoning": "...",
 "risk_level": "...",
 "tool": "...",
 "tool_arguments": {}
}
"""

    #user prompt 

    user_prompt = f"""
Conversation History:
{conversation_context}

Current User Message:
{ticket_text}

Predicted Intent: {intent}
Predicted Urgency: {urgency}
Model Confidence: {confidence}

Relevant Knowledge Base:
{context}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=400
        )

        raw_output = response.choices[0].message.content.strip()

        #json output parsing 

        parsed = json.loads(raw_output)

        return parsed

    except Exception as e:

        #safe fallback 

        return {
            "action": "ESCALATE",
            "reasoning": "Fallback triggered due to parsing or API error.",
            "risk_level": "high",
            "tool": "escalate_ticket",
            "tool_arguments": {}
        }