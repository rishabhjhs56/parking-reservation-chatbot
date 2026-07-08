import sys
from app.agents.chat_orchestrator import ChatOrchestrator
from app.utils.azure_llm import get_llm

llm = get_llm()

def main():
    # 1. Create our chatbot brain
    bot = ChatOrchestrator()

    print("\n🚗 SmartPark AI Parking Assistant Started\n")

    # 2. Friendly Welcome Message
    welcome_message = """
👋 Hello! Welcome to SmartPark AI Parking Services.

I can help you with:
• Checking parking availability
• Parking charges & pricing
• Locations (Delhi, Mumbai, Bengaluru, Hyderabad, Noida, Pune, Jhansi)
• Booking a parking reservation

👉 Type your query to get started (e.g., 'book a slot in Jhansi' or 'What are the charges?').
"""
    print("Bot:", welcome_message)
    print("Type 'exit' to quit.\n")

    # 3. Endless loop to keep chat running until user types 'exit'
    while True:
        try:
            # Get input from the user
            user_input = input("You: ").strip()

            # Exit condition
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nBot: Thank you for using SmartPark AI. Drive safely! 🚗")
                break
            
            # If user just presses Enter without typing anything, ignore it
            if not user_input:
                continue

            # Pass the input to the orchestrator to decide what to do
            response = bot.process(user_input, llm)

            print("\nBot:", response)

        # This catches when you press Ctrl+C to forcefully stop the program
        except KeyboardInterrupt:
            print("\n\nBot: Session terminated. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()