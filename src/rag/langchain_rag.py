from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import ChatGoogleGenerativeAI

from src.vectorstore.chroma_client import retrieve_papers

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------
# Gemini
# ---------------------------------------------------

llm = ChatGoogleGenerativeAI(

    model="gemini-2.5-flash",

    api_key=os.getenv("GEMINI_API_KEY"),

    temperature=0

)

# ---------------------------------------------------
# Prompt
# ---------------------------------------------------

prompt = ChatPromptTemplate.from_template("""
You are an AI Research Assistant.

Use ONLY the retrieved research papers to answer the user's question.

Instructions:
- Base your answer only on the provided context.
- Do not use outside knowledge.
- If multiple papers are relevant, combine their findings.
- Mention paper titles when appropriate.
- If the context does not contain enough information to answer the question, reply exactly:

"I couldn't find enough information in the retrieved papers."

Retrieved Papers:

{context}

User Question:

{question}
""")

# ---------------------------------------------------
# Output Parser
# ---------------------------------------------------

parser = StrOutputParser()


# ---------------------------------------------------
# Build Context
# ---------------------------------------------------

def build_context(results):

    context = ""

    docs = results["documents"][0]

    metas = results["metadatas"][0]

    for i, (doc, meta) in enumerate(zip(docs, metas), start=1):

        context += f"""

Paper {i}

Title:
{meta["title"]}

Authors:
{meta["authors"]}

Category:
{meta["category"]}

Abstract:
{doc}

"""

    return context


# ---------------------------------------------------
# LangChain RAG
# ---------------------------------------------------

def ask_question(question):

    results = retrieve_papers(question)

    context = build_context(results)

    chain = (

        prompt

        | llm

        | parser

    )

    response = chain.invoke(

        {

            "context": context,

            "question": question

        }

    )

    return response