import torch
import torch.nn as nn
from transformers import AutoModel

class SupportClassifier(nn.Module):
    def __init__(self, num_intents, num_urgency):
        super().__init__()

        self.encoder = AutoModel.from_pretrained("distilbert-base-uncased")
        hidden_size = self.encoder.config.hidden_size

        self.intent_head = nn.Linear(hidden_size, num_intents)
        self.urgency_head = nn.Linear(hidden_size, num_urgency)

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        pooled_output = outputs.last_hidden_state[:, 0]

        intent_logits = self.intent_head(pooled_output)
        urgency_logits = self.urgency_head(pooled_output)

        return intent_logits, urgency_logits