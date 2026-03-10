import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def create_execution_plan(ticket_text, decision, customer_history):

    system_prompt = """
You are a planning agent for a customer support AI system.

Given a decision, create a structured execution plan.

You must:
- Break the solution into logical steps.
- Identify which tools need to be executed (if any).
- Keep steps short and operational.

Return STRICT JSON:

{
  "plan_steps": ["step1", "step2", ...],
  "tools_to_execute": ["tool_name1", "tool_name2"]
}
"""

    user_prompt = f"""
Customer History:
{customer_history}

Ticket:
{ticket_text}

Decision:
{decision}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )

        raw = response.choices[0].message.content.strip()
        return json.loads(raw)

    except:
        return {
            "plan_steps": ["Escalate case to human agent"],
            "tools_to_execute": ["escalate_ticket"]
        }