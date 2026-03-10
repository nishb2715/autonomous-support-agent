Autonomous AI Customer Support Agent

An Agentic AI system that automatically processes customer support queries across multiple communication channels such as WhatsApp and Gmail.
The system analyzes user queries using machine learning models, retrieves relevant knowledge, decides the best action using an LLM decision agent, executes support tools when needed, and generates intelligent responses.

This project demonstrates how modern AI techniques such as LLMs, Retrieval-Augmented Generation (RAG), decision agents, and automated tool execution can be combined to build a scalable customer support system.

Features

• Multi-channel support (WhatsApp + Gmail)
• Intent detection using transformer-based models
• Urgency classification
• Confidence estimation
• Retrieval-Augmented Generation (RAG)
• LLM-based decision engine
• Automated support tools (password reset, refund, etc.)
• Conversation memory for contextual responses
• Reflection layer for safer decision making
• Modular architecture for easy extension

System Architecture
User Query
    │
    ▼
Intent Classification
    │
    ▼
Urgency Detection
    │
    ▼
Confidence Estimation
    │
    ▼
Knowledge Retrieval (RAG)
    │
    ▼
LLM Decision Agent
    │
    ├── AUTO_RESOLVE
    ├── ASK_CLARIFICATION
    └── ESCALATE
    │
    ▼
Tool Execution
    │
    ▼
Response Generation
    │
    ▼
Reply Sent to User
Project Structure
app/
│
├── classification/
│   ├── intent_classifier.py
│   ├── urgency_detector.py
│   ├── confidence_estimator.py
│   ├── model.py
│   └── train.py
│
├── decision_engine/
│   ├── decision_agent.py
│   ├── reflection_agent.py
│   └── tool_guardrail.py
│
├── retrieval/
│   └── retriever.py
│
├── response_generator/
│   └── response_builder.py
│
├── tools/
│   └── tool_executor.py
│
├── integrations/
│   ├── whatsapp_handler.py
│   └── gmail_handler.py
│
├── memory/
│   └── conversation_memory.py
│
├── feedback/
│   └── feedback_store.py
│
├── agent_pipeline.py
├── email_worker.py
└── main_api.py
Installation

Clone the repository

git clone https://github.com/yourusername/autonomous-support-agent.git
cd autonomous-support-agent

Create virtual environment

python -m venv supagent
supagent\Scripts\activate

Install dependencies

pip install -r requirements.txt
Environment Setup

Create a .env file in the root folder.

Example:

GROQ_API_KEY=your_groq_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
Running the API Server

Start the FastAPI server

python -m uvicorn app.main_api:app --reload

Server will run at:

http://127.0.0.1:8000
WhatsApp Bot Setup

Install ngrok

Run ngrok

ngrok http 8000

Copy the generated HTTPS URL.

Example:

https://abc123.ngrok-free.app

Go to Twilio Console → WhatsApp Sandbox

Set webhook:

https://abc123.ngrok-free.app/whatsapp

Now you can send messages to the WhatsApp sandbox number.

Gmail Integration

The Gmail integration allows the system to automatically process incoming support emails.

Run the email worker:

python -m app.email_worker

The system will:

Fetch incoming emails

Process them through the AI pipeline

Generate responses

Send reply emails automatically

Example Queries

Login Issue

I cannot log into my account

Order Tracking

Where is my order?

Refund Request

I was charged twice for my order

Subscription Cancellation

Please cancel my subscription
Model Files

Trained model weights are excluded from the repository due to GitHub file size limits.

Ignored files include:

*.pt
*.pkl

To regenerate models:

python app/classification/train.py
Future Improvements



Technologies Used

Python
FastAPI
Groq API (LLM)
Transformers
Sentence Transformers
FAISS
Twilio API
Gmail API
OAuth2 Authentication
