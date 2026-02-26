from fastapi import FastAPI
from pydantic import BaseModel
from app.classification.intent_classifier import predict_intent
from app.classification.urgency_detector import predict_urgency
from app.classification.confidence_estimator import calculate_confidence
from app.retrieval.retriever import Retriever
from app.decision_engine.decision_logic import decide_action
from app.response_generator.response_builder import build_response
from app.feedback.feedback_store import init_db, log_prediction, log_human_feedback

# Initializing DB
init_db()

app = FastAPI()
retriever = Retriever()



class TicketRequest(BaseModel):
    ticket_text: str


class FeedbackRequest(BaseModel):
    ticket_id: int
    human_action: str


#main ticket processing endpoint

@app.post("/process_ticket")
def process_ticket_api(request: TicketRequest):

    ticket_text = request.ticket_text

    # Classification
    intent, intent_conf = predict_intent(ticket_text)
    urgency, urgency_conf = predict_urgency(ticket_text)
    confidence = calculate_confidence(intent_conf, urgency_conf)

    #  Retrieval
    retrieved_docs = retriever.retrieve(ticket_text)

    # Decision
    decision = decide_action(
        intent,
        urgency,
        confidence,
        ticket_text,
        retrieved_docs
    )

    #  Response Generation
    response_json = build_response(
        ticket_text,
        intent,
        urgency,
        decision,
        retrieved_docs,
        confidence
    )

    #  Log Prediction to DB
    ticket_id = log_prediction(
        ticket_text,
        intent,
        urgency,
        confidence,
        decision["action"]
    )

    return {
        "ticket_id": ticket_id,
        "intent": intent,
        "urgency": urgency,
        "confidence": confidence,
        "decision": decision,
        "response": response_json
    }



# Endpoint to receive human feedback on predictions

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