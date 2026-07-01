# ==========================================
# FILE: app/agents/chat_orchestrator.py
# PURPOSE: Acts as the intent router and traffic cop. 
#          Ensures booking flows are handled by the FSM Agent,
#          while general knowledge queries are sent to RAG.
# ==========================================

from app.rag.retriever import ParkingRetriever
from app.agents.reservation_agent import ReservationAgent

class ChatOrchestrator:
    def __init__(self):
        self.retriever = ParkingRetriever()
        self.agent = ReservationAgent()
        # Active reservation switch
        self.active_reservation = False

    def detect_intent(self, user_input: str) -> str:
        """
        Determines the user's goal based on simple, flexible keyword matching.
        """
        text = user_input.lower().strip()

        # 1. Greeting Check
        greetings = ["hi", "hello", "hey", "greetings", "start"]
        if any(word in text for word in greetings):
            return "greeting"

        # 2. Reservation Check (catches shorthand or typos like 'parjking')
        reservation_keywords = ["book", "reserve", "reservation", "slot", "parking space", "parjking"]
        if any(word in text for word in reservation_keywords):
            return "reservation"

        # 3. Default fallback
        return "rag"

    def process(self, user_input: str, llm) -> str:
        """
        Main routing function called by app/main.py.
        """
        text = user_input.lower().strip()

        # Allow user to abort the booking flow at any time
        if self.active_reservation and text in ["cancel", "stop", "exit booking", "quit"]:
            self.active_reservation = False
            self.agent.reset_agent()
            return "❌ Booking cancelled. How else can I help you today?"

        # If booking flow is currently active, route directly to the FSM Agent
        if self.active_reservation:
            response = self.agent.handle_input(user_input)
            
            # If the FSM indicates completion, turn off active state
            if "Completed" in response:
                self.active_reservation = False
                
            return response

        # Otherwise, process the standard conversation flow
        intent = self.detect_intent(user_input)

        if intent == "greeting":
            return "👋 Hello! You can ask me about parking locations, charges, or say 'book a slot' to start a reservation."

        if intent == "reservation":
            self.active_reservation = True
            
            # Smart extraction: Check if a known location is already in the query
            locations = ["jhansi", "delhi", "mumbai", "bkc", "bengaluru", "noida", "pune", "hyderabad"]
            mentioned_location = None
            for loc in locations:
                if loc in text:
                    mentioned_location = loc.title()
                    break
            
            return self.agent.start_reservation(prefilled_location=mentioned_location)

        # RAG Search Flow
        docs = self.retriever.retrieve(user_input)
        if docs:
            context = "\n".join(docs)
            response = llm.invoke(
                f"You are SmartPark AI Assistant. Answer ONLY using the context below. Keep it short.\n\nContext:\n{context}\n\nQuestion: {user_input}"
            )
            return response.content

        return "I'm sorry, I couldn't find any information about that in our knowledge base. Can you try rephrasing your question?"