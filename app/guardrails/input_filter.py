import re


class Guardrails:

    def __init__(self):

        self.blocked_requests = [

            # Customer privacy
            "all reservations",
            "all bookings",
            "customer list",
            "all customers",
            "vehicle numbers",
            "all vehicle numbers",

            # System information
            "api key",
            "database password",
            "connection string",
            "secret key"
        ]

        # Basic profanity list
        self.profanity_words = [
            "fuck",
            "shit",
            "bitch",
            "asshole",
            "bastard"
        ]

    # --------------------------
    # Input Validation
    # --------------------------

    def validate_input(self, text: str):

        lower_text = text.lower()

        # Confidential requests
        for keyword in self.blocked_requests:
            if keyword in lower_text:
                return (
                    False,
                    "Sorry, I can't share confidential customer or system information."
                )

        # Profanity
        for word in self.profanity_words:
            if word in lower_text:
                return (
                    False,
                    "Please use respectful language."
                )

        return True, None

    # --------------------------
    # Output Masking
    # --------------------------

    def mask_output(self, text: str):

        # Email
        text = re.sub(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            '[EMAIL MASKED]',
            text
        )

        # Mobile Number
        text = re.sub(
            r'\b[6-9]\d{9}\b',
            '[MOBILE NUMBER MASKED]',
            text
        )

        # Vehicle Registration Number
        text = re.sub(
            r'\b[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}\b',
            '[VEHICLE NUMBER MASKED]',
            text,
            flags=re.IGNORECASE
        )

        # Credit / Debit Card
        text = re.sub(
            r'\b(?:\d[ -]*?){13,16}\b',
            '[CARD NUMBER MASKED]',
            text
        )

        # Driving Licence (Approx. Indian Format)
        text = re.sub(
            r'\b[A-Z]{2}[0-9]{13}\b',
            '[DRIVING LICENCE MASKED]',
            text,
            flags=re.IGNORECASE
        )

        return text