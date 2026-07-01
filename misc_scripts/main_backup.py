from app.agents.chat_orchestrator import ChatOrchestrator
from app.utils.azure_llm import llm


def main():

    bot = ChatOrchestrator()

    print("\n🚗 SmartPark AI Parking Assistant Started\n")

    # 🔥 INITIAL BOT GREETING (IMPORTANT FIX)
    welcome_message = """
👋 Hello! Welcome to SmartPark AI Parking Services.

I can help you with:
• Parking availability
• Charges & pricing
• Locations
• Reservation booking

👉 Type your query to get started.
"""

    print("Bot:", welcome_message)

    print("\nType 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        response = bot.process(user_input, llm)

        print("\nBot:", response)


if __name__ == "__main__":
    main()