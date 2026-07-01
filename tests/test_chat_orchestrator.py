from app.agents.chat_orchestrator import ChatOrchestrator


class TestChatOrchestrator:

    def test_detect_reservation_intent(self):
        """
        Positive Test:
        Reservation-related query should be identified correctly.
        """

        bot = ChatOrchestrator()

        intent = bot.detect_intent("I want to book a parking slot")

        assert intent == "reservation"

    def test_detect_normal_rag_query(self):
        """
        Negative Test:
        Normal parking question should NOT trigger reservation flow.
        It should be routed to the RAG pipeline.
        """

        bot = ChatOrchestrator()

        intent = bot.detect_intent("What are the parking charges?")

        assert intent == "rag"