from langgraph.graph import StateGraph, END

from app.graph.graph_state import GraphState
from app.graph.nodes import (
    chatbot_node,
    admin_node,
    mcp_node,
)


# ---------------------------------------------------------
# Router
# ---------------------------------------------------------

def route_after_chatbot(state: GraphState):

    # Reservation complete -> Admin approval
    if state.get("admin_required"):
        return "admin"

    # Normal RAG / Greeting / Reservation conversation
    return END


# ---------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------

def build_graph():

    workflow = StateGraph(GraphState)

    # ---------------- Nodes ----------------

    workflow.add_node("chatbot", chatbot_node)
    workflow.add_node("admin", admin_node)
    workflow.add_node("mcp", mcp_node)

    # ---------------- Entry ----------------

    workflow.set_entry_point("chatbot")

    # ---------------- Routing ----------------

    workflow.add_conditional_edges(
        "chatbot",
        route_after_chatbot,
        {
            "admin": "admin",
            END: END,
        },
    )

    workflow.add_edge("admin", "mcp")

    workflow.add_edge("mcp", END)

    return workflow.compile()