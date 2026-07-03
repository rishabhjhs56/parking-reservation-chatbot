from app.rag.retriever import ParkingRetriever
from app.agents.reservation_agent import ReservationAgent
from app.guardrails.input_filter import Guardrails
from app.agents.admin_agent import AdminAgent
from app.utils.logger import logger


class ChatOrchestrator:

    def __init__(self,
    retriever=None,
    reservation_agent=None,
    guardrails=None,
    admin=None,):

        self.retriever = retriever or ParkingRetriever()
        self.agent = reservation_agent or ReservationAgent()
        self.guardrails = guardrails or Guardrails()
        self.admin = admin or AdminAgent()

        self.active_reservation = False

        self.known_locations = {
            "jhansi",
            "delhi",
            "mumbai",
            "bengaluru",
            "hyderabad",
            "noida",
            "pune",
            "bkc"
        }

    # -----------------------------------------------------
    # Intent Detection
    # -----------------------------------------------------

    def detect_intent(self, user_input: str) -> str:

        text = user_input.lower().strip()

        reservation_keywords = [
            "book",
            "booking",
            "reserve",
            "reservation",
            "slot",
            "parking slot",
            "parking space"
        ]

        if any(keyword in text for keyword in reservation_keywords):
            return "reservation"

        greetings = {
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "greetings"
        }

        if text in greetings:
            return "greeting"

        return "rag"

    # -----------------------------------------------------
    # Main Router
    # -----------------------------------------------------

    def process(self, user_input: str, llm):

        text = user_input.lower().strip()

        # -------------------------------------------------
        # Admin Commands
        # -------------------------------------------------

        if text == "admin":

            self.admin.show_pending_reservations()

            return (
                "Admin Mode\n\n"
                "Commands:\n"
                "approve <reservation_id>\n"
                "reject <reservation_id>"
            )

        if text.startswith("approve"):

            try:

                reservation_id = int(text.split()[1])

                self.admin.approve_reservation(reservation_id)

                return f"✅ Reservation {reservation_id} Approved."

            except Exception:

                return "Usage: approve <reservation_id>"

        if text.startswith("reject"):

            try:

                reservation_id = int(text.split()[1])

                self.admin.reject_reservation(reservation_id)

                return f"❌ Reservation {reservation_id} Rejected."

            except Exception:

                return "Usage: reject <reservation_id>"

        # -------------------------------------------------
        # Guardrails
        # -------------------------------------------------

        is_valid, error_message = self.guardrails.validate_input(user_input)

        if not is_valid:
            return error_message

        # -------------------------------------------------
        # Reservation Already Running
        # -------------------------------------------------

        if self.active_reservation:

            if text in [
                "cancel",
                "stop",
                "quit",
                "exit booking"
            ]:

                logger.info("Reservation Cancelled By User")

                self.agent.reset_agent()

                self.active_reservation = False

                return "❌ Booking cancelled successfully."

            response = self.agent.handle_input(user_input)

            if "Pending Admin Approval" in response:

                self.active_reservation = False

            return response

        # -------------------------------------------------
        # Detect Intent
        # -------------------------------------------------

        intent = self.detect_intent(user_input)

        # -------------------------------------------------
        # Greeting
        # -------------------------------------------------

        if intent == "greeting":

            return (
                "👋 Hello! Welcome to SmartPark AI.\n\n"
                "I can help you with:\n"
                "• Parking charges\n"
                "• Parking availability\n"
                "• Parking locations\n"
                "• Booking a parking slot\n\n"
                "Example:\n"
                "Book a slot in Pune"
            )

        # -------------------------------------------------
        # Reservation
        # -------------------------------------------------

        if intent == "reservation":

            self.active_reservation = True

            mentioned_location = None

            for location in self.known_locations:

                if location in text:

                    mentioned_location = location.title()

                    break

            return self.agent.start_reservation(
                prefilled_location=mentioned_location
            )

        # -------------------------------------------------
        # RAG
        # -------------------------------------------------

        docs = self.retriever.retrieve(user_input)

        if docs:

            context = "\n\n".join(docs)

            prompt = f"""
You are SmartPark AI.

Rules:

- Answer ONLY using the provided context.
- Do not make up information.
- Keep answers short and professional.
- Use bullet points whenever appropriate.
- If the answer is unavailable, say:
  "Sorry, I couldn't find that information."

Context:
{context}

Question:
{user_input}
"""

            response = llm.invoke(prompt)

            return response.content

        return (
            "Sorry, I couldn't find any information related to your question. "
            "Please try rephrasing it."
        )