from fastapi import FastAPI
from pydantic import BaseModel

# Routers
from app.integrations.whatsapp_handler import router as whatsapp_router
from app.integrations.telegram_handler import router as telegram_router

# Core pipeline
from app.agent_pipeline import process_ticket_pipeline

# Feedback DB
from app.feedback.feedback_store import init_db, log_human_feedback
from app.integrations.telegram_handler import router as telegram_router
# Initialize DB
init_db()

# Create FastAPI app FIRST
app = FastAPI()

# Then attach routers
app.include_router(whatsapp_router)
app.include_router(telegram_router)


class TicketRequest(BaseModel):
    customer_id: str
    ticket_text: str


class FeedbackRequest(BaseModel):
    ticket_id: int
    human_action: str


@app.post("/process_ticket")
def process_ticket_api(request: TicketRequest):

    result = process_ticket_pipeline(
        request.customer_id,
        request.ticket_text
    )

    return result


@app.post("/submit_feedback")
def submit_feedback(feedback: FeedbackRequest):

    log_human_feedback(
        feedback.ticket_id,
        feedback.human_action
    )

    return {
        "status": "feedback recorded",
        "ticket_id": feedback.ticket_id,
        "human_action": feedback.human_action
    }