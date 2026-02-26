import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from model import SupportClassifier
import torch.nn as nn

# Loading dataset
df = pd.read_csv("../../data/tickets.csv")

# Encoding labels
intent_encoder = LabelEncoder()
urgency_encoder = LabelEncoder()

df["intent_label"] = intent_encoder.fit_transform(df["intent"])
df["urgency_label"] = urgency_encoder.fit_transform(df["urgency"])

import pickle

with open("intent_encoder.pkl", "wb") as f:
    pickle.dump(intent_encoder, f)

with open("urgency_encoder.pkl", "wb") as f:
    pickle.dump(urgency_encoder, f)

train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

class TicketDataset(Dataset):
    def __init__(self, dataframe):
        self.texts = dataframe["ticket_text"].tolist()
        self.intent_labels = dataframe["intent_label"].tolist()
        self.urgency_labels = dataframe["urgency_label"].tolist()

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = tokenizer(
            self.texts[idx],
            padding="max_length",
            truncation=True,
            max_length=64,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "intent_label": torch.tensor(self.intent_labels[idx]),
            "urgency_label": torch.tensor(self.urgency_labels[idx])
        }

train_loader = DataLoader(TicketDataset(train_df), batch_size=16, shuffle=True)

model = SupportClassifier(
    num_intents=len(intent_encoder.classes_),
    num_urgency=len(urgency_encoder.classes_)
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
loss_fn = nn.CrossEntropyLoss()

epochs = 3

for epoch in range(epochs):
    model.train()
    total_loss = 0

    for batch in train_loader:
        optimizer.zero_grad()

        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        intent_labels = batch["intent_label"].to(device)
        urgency_labels = batch["urgency_label"].to(device)

        intent_logits, urgency_logits = model(input_ids, attention_mask)

        loss = loss_fn(intent_logits, intent_labels) + \
               loss_fn(urgency_logits, urgency_labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader)}")

torch.save(model.state_dict(), "support_classifier.pt")
print("Training complete.")