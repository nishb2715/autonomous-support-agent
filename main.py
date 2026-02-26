from app.classification.intent_classifier import predict_intent
from app.classification.urgency_detector import predict_urgency
from app.classification.confidence_estimator import calculate_confidence
from app.retrieval.retriever import Retriever
from app.decision_engine.decision_logic import decide_action
from app.response_generator.response_builder import build_response

from pprint import pprint

retriever = Retriever()

def process_ticket(ticket_text):

    # Step 1: Classification
    intent, intent_conf = predict_intent(ticket_text)
    urgency, urgency_conf = predict_urgency(ticket_text)
    confidence = calculate_confidence(intent_conf, urgency_conf)

    # Step 2: Retrieval
    retrieved_docs = retriever.retrieve(ticket_text)

    # Step 3: Decision
    decision = decide_action(
        intent,
        urgency,
        confidence,
        ticket_text,
        retrieved_docs
    )

    # Step 4: LLM Response
    response_json = build_response(
        ticket_text,
        intent,
        urgency,
        decision,
        retrieved_docs,
        confidence
    )

    return {
    "ticket_text": ticket_text,
    "intent": intent,
    "urgency": urgency,
    "confidence": confidence,
    "decision": decision,
    "response": response_json
    }


if __name__ == "__main__":
    text = "Something is wrong"
    result = process_ticket(text)
    pprint(result)