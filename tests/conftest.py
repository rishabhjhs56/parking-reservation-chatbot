import pytest

from app.graph.nodes import chatbot


@pytest.fixture(autouse=True)
def reset_chatbot():

    chatbot.agent.reset_agent()

    chatbot.active_reservation = False

    yield

    chatbot.agent.reset_agent()

    chatbot.active_reservation = False