from app.graph.workflow import build_graph
from app.graph.nodes import chatbot

graph = build_graph()


def default_state(user_input: str):
    return {
        "user_input": user_input,
        "intent": "",
        "response": "",
        "reservation": None,
        "admin_required": False,
        "approved": False,
        "mcp_synced": False,
        "reservation_complete": False,
        "next_step": "",
    }


# ----------------------------------------------------
# Greeting Workflow
# ----------------------------------------------------

def test_greeting_workflow():

    chatbot.agent.reset_agent()
    chatbot.active_reservation = False

    result = graph.invoke(
        default_state("Hi")
    )

    assert result["response"] != ""
    assert "welcome" in result["response"].lower()
    assert "smartpark ai" in result["response"].lower()


# ----------------------------------------------------
# RAG Workflow
# ----------------------------------------------------

def test_rag_workflow():

    chatbot.agent.reset_agent()
    chatbot.active_reservation = False

    result = graph.invoke(
        default_state("What are the parking charges for SUV in Delhi?")
    )

    assert result["response"] != ""
    assert isinstance(result["response"], str)


# ----------------------------------------------------
# Reservation Workflow
# ----------------------------------------------------

def test_reservation_workflow():

    chatbot.agent.reset_agent()
    chatbot.active_reservation = False

    result = graph.invoke(
        default_state("Book a parking slot in Delhi")
    )

    assert "first name" in result["response"].lower()

    assert result["admin_required"] is False


# ----------------------------------------------------
# Guardrail Workflow
# ----------------------------------------------------

def test_guardrail_workflow():

    chatbot.agent.reset_agent()
    chatbot.active_reservation = False

    result = graph.invoke(
        default_state("<script>alert('hack')</script>")
    )

    assert result["response"] != ""