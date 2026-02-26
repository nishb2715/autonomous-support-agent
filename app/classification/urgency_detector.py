import torch
import torch.nn.functional as F
from .intent_classifier import model, tokenizer, urgency_encoder

def predict_urgency(text):
    encoding = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=64,
        return_tensors="pt"
    )

    with torch.no_grad():
        _, urgency_logits = model(
            encoding["input_ids"],
            encoding["attention_mask"]
        )

    probs = F.softmax(urgency_logits, dim=1)
    idx = torch.argmax(probs).item()

    return urgency_encoder.inverse_transform([idx])[0], torch.max(probs).item()