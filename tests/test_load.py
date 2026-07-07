import time

from fastapi.testclient import TestClient

from app.graph.workflow import build_graph
from app.mcp.server import app
from app.utils.config import FastAPI_MCP_API_KEY


graph = build_graph()
client = TestClient(app)


def graph_state(user_input: str):
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
# TC-01
# LangGraph Chatbot Load Test
# ----------------------------------------------------

def test_langgraph_load():

    total_requests = 10

    start = time.perf_counter()

    for _ in range(total_requests):

        result = graph.invoke(
            graph_state("What are parking charges in Delhi?")
        )

        assert result["response"] != ""

    end = time.perf_counter()

    avg_time = (end - start) / total_requests

    print(f"\nAverage LangGraph response time: {avg_time:.3f} sec")

    # Change threshold if needed
    assert avg_time < 10


# ----------------------------------------------------
# TC-02
# MCP Server Load Test
# ----------------------------------------------------

def test_mcp_load():

    total_requests = 10

    start = time.perf_counter()

    for _ in range(total_requests):

        response = client.post(
            "/sync-all",
            headers={
                "x-api-key": FastAPI_MCP_API_KEY
            }
        )

        assert response.status_code == 200

    end = time.perf_counter()

    avg_time = (end - start) / total_requests

    print(f"\nAverage MCP response time: {avg_time:.3f} sec")

    assert avg_time < 10