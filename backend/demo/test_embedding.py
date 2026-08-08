from services.ai.document.embedding import embedding_service

vector = embedding_service.embed_query(
    "What is artificial intelligence?"
)

print(len(vector))
print(vector[:10])