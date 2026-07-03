from app.agents.chat_orchestrator import ChatOrchestrator


class DummyRetriever:
    pass


class DummyReservationAgent:
    pass


class DummyGuardrails:
    pass


class DummyAdmin:
    pass


class TestChatOrchestrator:

    def create_bot(self):
        return ChatOrchestrator(
            retriever=DummyRetriever(),
            reservation_agent=DummyReservationAgent(),
            guardrails=DummyGuardrails(),
            admin=DummyAdmin(),
        )

    def test_detect_reservation_intent(self):
        """
        Positive Test:
        Reservation-related query should be identified correctly.
        """

        bot = self.create_bot()

        intent = bot.detect_intent("I want to book a parking slot")

        assert intent == "reservation"

    def test_detect_normal_rag_query(self):
        """
        Negative Test:
        Normal parking question should NOT trigger reservation flow.
        """

        bot = self.create_bot()

        intent = bot.detect_intent("What are the parking charges?")

        assert intent == "rag"