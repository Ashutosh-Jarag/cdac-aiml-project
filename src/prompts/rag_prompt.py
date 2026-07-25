SYSTEM_PROMPT = """
You are an AI Research Assistant.

Your task is to answer the user's question ONLY using the retrieved research papers.

Instructions

- Use ONLY the information present in the context.
- Never use outside knowledge.
- If the answer is unavailable, reply:

"I couldn't find enough information in the retrieved papers."

- Mention paper titles whenever appropriate.
- Keep answers concise and scientifically accurate.
"""


def build_prompt(
    context: str,
    question: str
):

    return f"""
{SYSTEM_PROMPT}

================================================================================
Retrieved Research Papers
================================================================================

{context}

================================================================================
User Question
================================================================================

{question}
"""