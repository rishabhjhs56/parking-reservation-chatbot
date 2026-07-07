from app.graph.graph_state import GraphState

from app.agents.chat_orchestrator import ChatOrchestrator
from app.agents.admin_agent import AdminAgent
from app.mcp.client import MCPClient

from app.utils.azure_llm import llm
from app.utils.logger import logger


# ---------------------------------------------------------
# Shared Objects
# ---------------------------------------------------------

chatbot = ChatOrchestrator()
admin = AdminAgent()
mcp = MCPClient()


# ---------------------------------------------------------
# Chatbot Node
# ---------------------------------------------------------

def chatbot_node(state: GraphState):

    logger.info("LangGraph | Chatbot Node Started")

    response = chatbot.process(
        state["user_input"],
        llm
    )

    state["response"] = response

    state["admin_required"] = False
    state["reservation"] = None

    # Reservation completed?
    if "Pending Admin Approval" in response:

        reservation = chatbot.agent.reservation

        if reservation is not None:

            state["reservation"] = reservation
            state["admin_required"] = True

            logger.info(
                f"LangGraph | Reservation {reservation.reservation_id} requires admin approval"
            )

    logger.info("LangGraph | Chatbot Node Completed")

    return state


# ---------------------------------------------------------
# Human-in-the-loop Admin Node
# ---------------------------------------------------------

def admin_node(state: GraphState):

    logger.info("LangGraph | Admin Node Started")

    reservation = state.get("reservation")

    if reservation is not None:

        admin.notify_admin(reservation)

    logger.info("LangGraph | Admin Node Completed")

    return state


# ---------------------------------------------------------
# MCP Synchronization Node
# ---------------------------------------------------------

def mcp_node(state: GraphState):

    logger.info("LangGraph | MCP Synchronization Started")

    mcp.sync_all()

    state["mcp_synced"] = True

    logger.info("LangGraph | MCP Synchronization Completed")

    return state