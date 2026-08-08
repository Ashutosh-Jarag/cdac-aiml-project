from langgraph.graph import END
from langgraph.graph import StateGraph

from services.ai.graph.state import ChatState

from services.ai.graph.nodes import (
    load_history,
    retrieve_context,
    generate_answer,
    save_messages,
    generate_title
)


workflow = StateGraph(ChatState)

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


chat_graph = workflow.compile(
    debug=True,
)