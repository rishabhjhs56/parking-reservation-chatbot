from app.agents.reservation_agent import ReservationAgent


class TestReservationAgent:

    def test_start_reservation(self):

        agent = ReservationAgent()

        response = agent.start_reservation()

        assert "parking reservation" in response.lower()
        assert agent.step == "location"

    def test_invalid_location(self):

        agent = ReservationAgent()

        agent.start_reservation()

        response = agent.handle_input("London")

        assert "don't operate" in response.lower()
        assert agent.step == "location"