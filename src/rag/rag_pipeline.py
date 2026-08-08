from src.vectorstore.chroma_client import retrieve_papers
from src.prompts.rag_prompt import build_prompt
from src.llm.gemini_client import ask_gemini


def build_context(results: dict) -> str:
    """
    Convert retrieved papers into a prompt-friendly context.
    """

    context = ""

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for i, (doc, meta) in enumerate(zip(documents, metadatas), start=1):

        context += "=" * 80 + "\n"
        context += f"Paper {i}\n"
        context += "=" * 80 + "\n\n"

        context += f"Title:\n{meta['title']}\n\n"
        context += f"Authors:\n{meta['authors']}\n\n"
        context += f"Category:\n{meta['category']}\n\n"

        context += f"Abstract:\n{doc}\n\n"

    return context


def ask_question(
    question: str,
    top_k: int = 5
):
    """
    Complete RAG Pipeline.
    """

    # Step 1
    results = retrieve_papers(
        question,
        top_k
    )

    # Step 2
    context = build_context(
        results
    )

    # Step 3
    prompt = build_prompt(
        context=context,
        question=question
    )

    # Step 4
    answer = ask_gemini(
        prompt
    )

    return answer