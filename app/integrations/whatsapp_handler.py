from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from app.agent_pipeline import process_ticket_pipeline

router = APIRouter()

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):

    form = await request.form()

    message = form.get("Body")
    sender = form.get("From")

    result = process_ticket_pipeline(sender, message)

    # Extract clean response message
    reply = None

    if isinstance(result.get("response"), dict):
        reply = result["response"].get("response_message")

    if not reply:
        reply = str(result)

    resp = MessagingResponse()
    resp.message(reply)

    return Response(
        content=str(resp),
        media_type="application/xml"
    )