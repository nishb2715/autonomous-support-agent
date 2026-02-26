from .vector_store import VectorStore

class Retriever:
    def __init__(self):
        self.vector_store = VectorStore()
        self.vector_store.load_documents()
        self.vector_store.build_index()

    def retrieve(self, query, top_k=3):
        return self.vector_store.search(query, top_k)