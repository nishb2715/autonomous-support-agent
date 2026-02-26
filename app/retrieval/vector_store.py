import os
import faiss
import numpy as np
from .embedder import Embedder

class VectorStore:
    def __init__(self, kb_path="data/knowledge_base"):
        self.kb_path = kb_path
        self.embedder = Embedder()
        self.documents = []
        self.metadata = []
        self.index = None

    def load_documents(self):
        for file in os.listdir(self.kb_path):
            if file.endswith(".txt"):
                path = os.path.join(self.kb_path, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    chunks = self.chunk_text(content)
                    for chunk in chunks:
                        self.documents.append(chunk)
                        self.metadata.append({"source": file})

    def chunk_text(self, text, chunk_size=100):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append(chunk)
        return chunks

    def build_index(self):
        embeddings = self.embedder.encode(self.documents)
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings.astype(np.float32))

    def search(self, query, top_k=3):
        query_embedding = self.embedder.encode([query]).astype(np.float32)
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            results.append({
                "content": self.documents[idx],
                "source": self.metadata[idx]["source"],
                "similarity_score": float(dist)
            })

        return results