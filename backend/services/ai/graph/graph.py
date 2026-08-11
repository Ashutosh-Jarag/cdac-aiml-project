"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file constructs and compiles the primary LangGraph execution graph (`chat_graph`) for processing chat workflows.
It wires node tasks sequentially: loading session message history, retrieving vector search context, generating AI responses, 
persisting updated chat messages, and optionally auto-generating session titles.

Workflow Pipeline Nodes:
  1. history: `load_history` — Loads existing message history for the session into the state.
  2. retrieve: `retrieve_context` — Queries relevant vector embeddings and updates state context.
  3. generate: `generate_answer` — Generates the LLM completion response based on query and context.
  4. save: `save_messages` — Persists both user input and AI response messages to the database.
  5. title: `generate_title` — Generates or updates the chat session title when applicable.

Exports:
  - chat_graph: Compiled, debug-enabled LangGraph state graph ready to execute chat sessions.
"""

from langgraph.graph import END, StateGraph

from services.ai.graph.state import ChatState
from services.ai.graph.nodes import (
    load_history,
    retrieve_context,
    generate_answer,
    save_messages,
    generate_title,
)

# Initialize the StateGraph workflow parameterised with ChatState schema
workflow = StateGraph(ChatState)

# Register execution nodes
workflow.add_node(
    "history",
    load_history,
)

workflow.add_node(
    "retrieve",
    retrieve_context,
)

workflow.add_node(
    "generate",
    generate_answer,
)

workflow.add_node(
    "save",
    save_messages,
)

workflow.add_node(
    "title",
    generate_title,
)

# Define entry point and sequential edge execution pipeline
workflow.set_entry_point("history")

workflow.add_edge(
    "history",
    "retrieve",
)

workflow.add_edge(
    "retrieve",
    "generate",
)

workflow.add_edge(
    "generate",
    "save",
)

workflow.add_edge(
    "save",
    "title",
)

workflow.add_edge(
    "title",
    END,
)

# Compile the workflow graph with debug tracing enabled
chat_graph = workflow.compile(
    debug=True,
)