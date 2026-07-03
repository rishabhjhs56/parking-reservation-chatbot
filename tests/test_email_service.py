from app.utils.email_service import EmailService


class TestEmailService:

    def test_email_service_created(self):
        """
        Positive Test:
        Email service object should initialize successfully.
        """

        email = EmailService()

        assert email is not None


    def test_email_service_has_notification_method(self):
        """
        Negative Test:
        Verify notification method exists.
        """

        email = EmailService()

        assert hasattr(email, "send_admin_notification")