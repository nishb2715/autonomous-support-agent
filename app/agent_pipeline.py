from app.classification.intent_classifier import predict_intent
from app.classification.urgency_detector import predict_urgency
from app.classification.confidence_estimator import calculate_confidence

from app.retrieval.retriever import Retriever

from app.decision_engine.decision_agent import llm_decide_action
from app.decision_engine.reflection_agent import review_decision
from app.decision_engine.tool_guardrail import enforce_tool_rules

from app.response_generator.response_builder import build_response

from app.memory.conversation_memory import add_message, get_history
from app.feedback.feedback_store import get_customer_history

from app.tools.tool_executor import execute_tool


#initializing retriever 

retriever = Retriever()


#main agent pipeline fn 

def process_ticket_pipeline(customer_id, ticket_text):

    #storing previous convo in short term memory 

    add_message(customer_id, "user", ticket_text)

    #intent classification 

    intent, intent_conf = predict_intent(ticket_text)

    #urgency detection 

    urgency, urgency_conf = predict_urgency(ticket_text)

    #confidence estimation 

    confidence = calculate_confidence(intent_conf, urgency_conf)

    #retrieving short term convo history 

    history = get_history(customer_id)

    #retrieving long term customer history 

    customer_history = get_customer_history(customer_id)

    #rag 

    docs = retriever.retrieve(ticket_text)

    #llm decision agent 

    decision = llm_decide_action(
        ticket_text,
        intent,
        urgency,
        confidence,
        docs,
        history
    )

    #reflection agent to review decision 

    decision = review_decision(ticket_text, decision)

    #safety layer 

    decision = enforce_tool_rules(intent, decision)

    #tool execution 

    tool_result = None

    if decision.get("tool"):

        tool_result = execute_tool(
            decision["tool"],
            decision.get("tool_arguments", {}),
            ticket_text
        )

    #fn to generate responses 

    response = build_response(
        ticket_text,
        intent,
        urgency,
        decision,
        docs,
        confidence
    )

    # Override response if tool executed
    if tool_result and tool_result.get("message"):

        response["response_message"] = tool_result["message"]

    #storing responses in memory 

    try:

        add_message(
            customer_id,
            "assistant",
            response["response_message"]
        )

    except:

        pass

    #final output layout

    return {

        "intent": intent,
        "urgency": urgency,
        "confidence": confidence,

        "decision": decision,

        "tool_executed": decision.get("tool"),
        "tool_result": tool_result,

        "response": response
    }