
import chromadb
from sentence_transformers import SentenceTransformer

import preprocessing


# --------------------------------------------------
# Load Sentence-BERT
# --------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# Connect ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="/content/drive/MyDrive/Research_Project/chroma_db"
)

collection = client.get_collection(
    "research_papers"
)


# --------------------------------------------------
# Recommendation Function
# --------------------------------------------------

def recommend(title, abstract="", top_k=10):

    combined_text = title + ". " + abstract

    combined_text = preprocessing.preprocess(
        combined_text
    )

    query_embedding = model.encode(
        [combined_text],
        convert_to_numpy=True
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    recommendations = []

    ids = results["ids"][0]
    metadata = results["metadatas"][0]

    for paper_id, meta in zip(ids, metadata):

        recommendations.append(
            {
                "id": paper_id,
                "title": meta["title"],
                "authors": meta["authors"],
                "category": meta["category"],
                "update_date": meta["update_date"]
            }
        )

    return recommendations
