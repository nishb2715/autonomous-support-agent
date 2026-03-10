from fastapi import APIRouter, Request
from app.agent_pipeline import process_ticket_pipeline

router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):

    data = await request.json()

    message = data["message"]["text"]
    sender = str(data["message"]["chat"]["id"])

    result = process_ticket_pipeline(sender, message)

    reply = result["response"]["response_message"]

    return {
        "method": "sendMessage",
        "chat_id": sender,
        "text": reply
    }