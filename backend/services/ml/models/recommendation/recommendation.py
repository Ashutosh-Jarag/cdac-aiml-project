import os
import sys

from dotenv import load_dotenv

load_dotenv()

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from services.ml.models.recommendation import preprocessing


# ==========================================================
# Pinecone
# ==========================================================

pc = Pinecone(
    api_key=os.environ["PINECONE_API_KEY"]
)

index = pc.Index("research-papers")


# ==========================================================
# Sentence-BERT
# ==========================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================================
# Preprocessing
# ==========================================================

sys.path.insert(
    0,
    "/content/drive/MyDrive/Research_Project/"
)




# ==========================================================
# Recommendation Function
# ==========================================================

def recommend(
    title,
    abstract="",
    top_k=10
):

    # ------------------------------------------
    # Combine title + abstract
    # ------------------------------------------

    combined_text = (
        title + ". " + abstract
    )


    # ------------------------------------------
    # Preprocess query
    # ------------------------------------------

    combined_text = preprocessing.preprocess(
        combined_text
    )


    # ------------------------------------------
    # Generate query embedding
    # ------------------------------------------

    query_embedding = model.encode(
        [combined_text],
        convert_to_numpy=True
    )[0]


    # ------------------------------------------
    # Search Pinecone
    # ------------------------------------------

    results = index.query(
        vector=query_embedding.tolist(),
        top_k=top_k,
        namespace="research-papers",
        include_metadata=True
    )


    # ------------------------------------------
    # Format recommendations
    # ------------------------------------------

    recommendations = []

    for match in results["matches"]:

        metadata = match["metadata"]

        recommendations.append(
            {
                "id": match["id"],
                "score": match["score"],
                "title": metadata.get(
                    "title",
                    ""
                ),
                "authors": metadata.get(
                    "authors",
                    ""
                ),
                "category": metadata.get(
                    "category",
                    ""
                ),
                "update_date": metadata.get(
                    "update_date",
                    ""
                )
            }
        )


    return recommendations
