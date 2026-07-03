from app.agents.admin_agent import AdminAgent


class TestAdminAgent:

    def test_show_pending_reservations(self):
        """
        Positive Test:
        Should execute pending reservation listing.
        """

        admin = AdminAgent()

        admin.show_pending_reservations()

        assert True


    def test_approve_invalid_reservation(self):
        """
        Negative Test:
        Invalid reservation id should not crash.
        """

        admin = AdminAgent()

        admin.approve_reservation(999999)

        assert True