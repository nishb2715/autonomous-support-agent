import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_response(ticket_text, intent, urgency, decision, retrieved_docs, confidence):

    action = decision["action"]

    context = "\n\n".join([doc["content"] for doc in retrieved_docs])

    system_prompt = """
You are an enterprise customer support AI agent.

STRICT RULES:
- Use ONLY provided knowledge context.
- Return response strictly in valid JSON.
- Do NOT include extra text outside JSON.

Required JSON format:

{
  "final_action": "...",
  "response_message": "...",
  "requires_human": true/false
}

Logic:
- ESCALATE → requires_human = true
- ASK_CLARIFICATION → requires_human = false
- AUTO_RESOLVE → requires_human = false
"""

    user_prompt = f"""
Customer Ticket:
{ticket_text}

Predicted Intent: {intent}
Urgency: {urgency}
Decision Action: {action}
Confidence Score: {confidence}

Knowledge Context:
{context}
"""

    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=400
    )

    raw_output = chat_completion.choices[0].message.content

    try:
        parsed = json.loads(raw_output)
        return parsed
    except:
        # fallback safety
        return {
            "final_action": action,
            "response_message": raw_output,
            "requires_human": action == "ESCALATE"
        }