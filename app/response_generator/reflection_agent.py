import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def reflect_on_response(ticket_text, response_json):

    system_prompt = """
You are a safety review agent.

Review the generated response and decide:

- APPROVED
- REGENERATE
- ESCALATE

Return strict JSON:
{
  "review_decision": "...",
  "reason": "..."
}
"""

    user_prompt = f"""
Ticket:
{ticket_text}

Generated Response:
{response_json}
"""

    result = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    raw = result.choices[0].message.content

    try:
        return json.loads(raw)
    except:
        return {"review_decision": "APPROVED", "reason": "Fallback approval"}