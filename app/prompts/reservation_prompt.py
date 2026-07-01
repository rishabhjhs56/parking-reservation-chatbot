from langchain_core.prompts import ChatPromptTemplate

RESERVATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are collecting reservation information.

Collect the following details one by one:

- First Name
- Last Name
- Car Number
- Reservation Date
- Reservation Time
- Duration

Do not skip any field.

If any information is missing, politely ask for it.
            """,
        ),
        (
            "human",
            "{user_input}",
        ),
    ]
)