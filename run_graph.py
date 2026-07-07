import os
import sys

# Set environment variables before any imports
os.environ['GRPC_VERBOSITY'] = 'NONE'
os.environ['GRPC_TRACE'] = ''
os.environ['GLOG_minloglevel'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Redirect stderr temporarily to suppress C++ level logs
import io
from contextlib import redirect_stderr

from app.graph.workflow import build_graph


graph = build_graph()

print("\n🚗 SmartPark AI Parking Assistant Started\n")

print("""
👋 Hello! Welcome to SmartPark AI Parking Services.

I can help you with:
• Checking parking availability
• Parking charges & pricing
• Locations (Delhi, Mumbai, Bengaluru, Hyderabad, Noida, Pune, Jhansi)
• Booking a parking reservation

👉 Type your query to get started
(e.g. Book a slot in Jhansi)

Type 'exit' to quit.
""")

while True:

    user = input("\nYou : ")

    if user.lower() == "exit":
        break

    result = graph.invoke(
        {
            "user_input": user,
            "intent": "",
            "response": "",
            "reservation": None,
            "admin_required": False,
            "approved": False,
            "mcp_synced": False,
            "reservation_complete": False,
            "next_step": "",
        }
    )

    #print("Warmup complete")

    print("\nBot :", result["response"])