import streamlit as st

from app.ui_app.components import show_reservation_card
from app.utils.reservation_parser import parse_reservation_summary


def render_user_chat(graph):
    """
    Render SmartPark AI User Chat Interface
    """

    # --------------------------------------------------
    # Initialize Session State
    # --------------------------------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "graph_state" not in st.session_state:
        st.session_state.graph_state = {
            "user_input": "",
            "intent": "",
            "response": "",
            "reservation": None,
            "admin_required": False,
            "approved": False,
            "mcp_synced": False,
            "reservation_complete": False,
            "next_step": "",
        }

    # --------------------------------------------------
    # Display Previous Conversation
    # --------------------------------------------------

    for msg in st.session_state.messages:

        avatar = "👤" if msg["role"] == "user" else "🚗"

        with st.chat_message(msg["role"], avatar=avatar):

            if msg["role"] == "assistant" and msg.get("reservation"):
                show_reservation_card(msg["reservation"])
            else:
                st.markdown(msg["content"])

    # --------------------------------------------------
    # Chat Input
    # --------------------------------------------------

    prompt = st.chat_input(
        "Ask about parking, charges, availability or book a parking slot..."
    )

    if not prompt:
        return

    # --------------------------------------------------
    # Display User Message
    # --------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # --------------------------------------------------
    # Invoke LangGraph
    # --------------------------------------------------

    st.session_state.graph_state["user_input"] = prompt

    with st.spinner("🤖 SmartPark AI is thinking..."):

        result = graph.invoke(
            st.session_state.graph_state
        )

    st.session_state.graph_state = result

    answer = result["response"]

    reservation = parse_reservation_summary(answer)

    # --------------------------------------------------
    # Store Assistant Response
    # --------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "reservation": reservation,
        }
    )

    # --------------------------------------------------
    # Display Assistant Response
    # --------------------------------------------------

    with st.chat_message("assistant", avatar="🚗"):

        if reservation:
            show_reservation_card(reservation)
        else:
            st.markdown(answer)