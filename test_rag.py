from app.retrieval.retriever import Retriever

retriever = Retriever()

query = "There is an unauthorized charge on my account"
results = retriever.retrieve(query)

for r in results:
    print(r)