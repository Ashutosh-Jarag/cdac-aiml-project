import os

from services.ml.models.recommendation.recommendation import (
    model,
    index,
)

import google.generativeai as genai


class MLChatService:

    def chat(
        self,
        question: str,
        provider: str | None,
        api_key: str | None
    ):

        # ---------------------------------------------
        # 1. Embed question
        # ---------------------------------------------

        query_embedding = model.encode(
            [question],
            convert_to_numpy=True
        )

        # ---------------------------------------------
        # 2. Retrieve papers from Pinecone
        # ---------------------------------------------

        results = index.query(
            vector=query_embedding.tolist()[0],
            top_k=3,
            namespace="research-papers",
            include_metadata=True,
        )

        papers = []

        for match in results.get("matches", []):

            metadata = match.get("metadata", {})

            papers.append({
                "id": match.get("id", ""),
                "title": metadata.get("title", ""),
                "authors": metadata.get("authors", ""),
                "category": metadata.get("category", ""),
                "update_date": metadata.get("update_date", ""),
                "similarity": round(
                    match.get("score", 0) * 100,
                    2
                ),
            })

        # ---------------------------------------------
        # 3. Build research context
        # ---------------------------------------------

        context = "\n\n".join(
            f"""
Paper:
{paper["title"]}

Authors:
{paper["authors"]}

Category:
{paper["category"]}

Publication Date:
{paper["update_date"]}
"""
            for paper in papers
        )

        # ---------------------------------------------
        # 4. Gemini
        # ---------------------------------------------

        if api_key:
            genai.configure(api_key=api_key)
        else:
            genai.configure(
                api_key=os.getenv("GEMINI_API_KEY")
            )

        prompt = f"""
You are an AI research assistant.

Answer the user's question in a useful and
educational way.

Use the retrieved research-paper information
below as supporting research context.

Do NOT simply list the papers.

Instead, explain the answer naturally and
connect it to the retrieved research topics.

When appropriate, mention phrases such as:
"Based on the retrieved research..."
or
"The retrieved papers discuss..."

Do not invent specific experimental results,
numbers, or claims that are not present in the
provided context.

User question:
{question}

Retrieved research papers:
{context}
"""

        gemini = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        try:
            response = gemini.generate_content(prompt)
            answer = response.text
        except Exception as e:
            print(f"Gemini generation failed: {e}")

            if papers:
                paper_names = "\n".join(
                    f"- {paper['title']}"
                    for paper in papers
                )

                answer = (
                    "Based on the research papers retrieved from "
                    "the ResearchAI knowledge base, the question "
                    "is related to the following research areas:\n\n"
                    f"{paper_names}\n\n"
                    "These papers provide relevant research context "
                    "for understanding the topic. The retrieved "
                    "papers can be explored below for more detailed "
                    "information."
                )
            else:
                answer = (
                    "I could not find relevant research information "
                    "for this question in the knowledge base."
                )

        # ---------------------------------------------
        # 5. References
        # ---------------------------------------------

        references = [
            {
                "title": paper["title"],
                "paper_url": (
                    f"https://arxiv.org/abs/{paper['id']}"
                ),
            }
            for paper in papers
        ]

        return {
            "answer": answer,
            "references": references,
        }


ml_chat_service = MLChatService()