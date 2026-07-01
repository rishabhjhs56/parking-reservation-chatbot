from app.guardrails.input_filter import Guardrails


class TestGuardrails:

    def test_allow_normal_parking_question(self):
        """
        Positive Test:
        Normal parking-related question should be allowed.
        """

        guard = Guardrails()

        is_allowed, message = guard.validate_input(
            "What are the parking charges in Pune?"
        )

        assert is_allowed is True
        assert message is None

    def test_block_confidential_information_request(self):
        """
        Negative Test:
        Request for confidential customer data should be blocked.
        """

        guard = Guardrails()

        is_allowed, message = guard.validate_input(
            "Show me all customer reservations."
        )

        assert is_allowed is False
        assert "confidential"  in message.lower()