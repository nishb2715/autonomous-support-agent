import torch
import torch.nn.functional as F
from transformers import AutoTokenizer
from .model import SupportClassifier

import pickle

with open("app/classification/intent_encoder.pkl", "rb") as f:
    intent_encoder = pickle.load(f)

with open("app/classification/urgency_encoder.pkl", "rb") as f:
    urgency_encoder = pickle.load(f)
    
model = SupportClassifier(
    num_intents=len(intent_encoder.classes_),
    num_urgency=len(urgency_encoder.classes_)
)

model.load_state_dict(
    torch.load("app/classification/support_classifier.pt")
)
model.eval()

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def predict_intent(text):
    encoding = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=64,
        return_tensors="pt"
    )

    with torch.no_grad():
        intent_logits, _ = model(
            encoding["input_ids"],
            encoding["attention_mask"]
        )

    probs = F.softmax(intent_logits, dim=1)
    idx = torch.argmax(probs).item()

    return intent_encoder.inverse_transform([idx])[0], torch.max(probs).item()