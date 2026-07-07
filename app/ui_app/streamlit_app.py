from langchain_groq import data
import streamlit as st

from app.graph.workflow import build_graph

# ----------------------------
# Build LangGraph once
# ----------------------------
graph = build_graph()

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="SmartPark AI",
    page_icon="🚗",
    layout="wide",
)

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:

    st.title("🚗 SmartPark AI")

    st.markdown("---")

    st.markdown(
        """
### 🚀 Services

- 🚗 Parking Charges
- 📍 Parking Locations
- 🅿️ Parking Availability
- 📅 Parking Reservation

---

### 🌍 Supported Cities

- Delhi
- Mumbai
- Bengaluru
- Hyderabad
- Noida
- Pune
- Jhansi

---

### 💡 Sample Questions

• Hi

• Parking charges

• Parking availability

• Book parking

• Book parking in Pune
"""
    )

# ----------------------------
# Header
# ----------------------------
st.title("🚗 SmartPark AI")

st.subheader("AI Powered Parking Reservation Assistant")

st.divider()

# ----------------------------
# Dashboard Metrics
# ----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Cities", "7")

with col2:
    st.metric("Parking Zones", "24")

with col3:
    st.metric("Support", "24×7")

st.divider()

# ----------------------------
# Session State
# ----------------------------
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

# ----------------------------
# Show Previous Messages
# ----------------------------
for msg in st.session_state.messages:

    avatar = "👤" if msg["role"] == "user" else "🚗"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ----------------------------
# Chat Input
# ----------------------------
prompt = st.chat_input(
    "Ask about parking, charges, availability or book a parking slot..."
)

# ----------------------------
# User Message
# ----------------------------
if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    st.session_state.graph_state["user_input"] = prompt

    with st.spinner("🤖 SmartPark AI is thinking..."):

        result = graph.invoke(
            st.session_state.graph_state
        )

    st.session_state.graph_state = result

    answer = result["response"]

    def format_reservation_summary(text: str):

        if "Reservation Completed Successfully" not in text:
            return None

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        data = {}

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()

        return data

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    with st.chat_message("assistant"):

        reservation = format_reservation_summary(answer)

        if reservation:

            st.success("🎉 Reservation Completed Successfully!")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Reservation ID", reservation.get("🆔 Reservation ID", "-"))
                st.write(f"📍 **Location:** {reservation.get('📍 Location', '-')}")
                st.write(f"🗺️ **Zone:** {reservation.get('🗺️ Zone', '-')}")
                st.write(f"🏢 **Block:** {reservation.get('🏢 Block', '-')}")
                st.write(f"🅿️ **Slot:** {reservation.get('🅿️ Slot', '-')}")

            with col2:
                st.write(f"👤 **Name:** {reservation.get('👤 Name', '-')}")
                st.write(f"📱 **Phone:** {reservation.get('📱 Phone', '-')}")
                st.write(f"🚗 **Vehicle:** {reservation.get('🚗 Vehicle', '-')}")
                st.write(f"🪪 **Licence:** {reservation.get('🪪 Driving Licence', '-')}")
                st.write(f"📅 **Date:** {reservation.get('📅 Date', '-')}")
                st.write(f"⏰ **Time:** {reservation.get('⏰ Time', '-')}")

            st.info(f"**Status:** {reservation.get('Status', 'Pending Admin Approval ⏳')}")

        else:
            st.markdown(answer)

# ----------------------------
# Footer
# ----------------------------
st.divider()

st.caption(
    "🚗 SmartPark AI • LangGraph • Azure OpenAI • Milvus • SQLite"
)