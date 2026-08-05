from services.ai.document.loader import document_loader
from services.ai.document.chunker import document_chunker
from services.ai.document.embedding import embedding_service
from services.ai.document.vector_store import vector_store

documents = document_loader.load("demo/sample.txt")

chunks = document_chunker.split(documents)

embeddings = embedding_service.embed_documents(
    [chunk.page_content for chunk in chunks]
)

vector_store.add_documents(
    collection_name="demo",
    chunks=chunks,
    embeddings=embeddings
)

query = embedding_service.embed_query(
    "What is Artificial Intelligence?"
)

results = vector_store.search(
    "demo",
    query
)

print(results)