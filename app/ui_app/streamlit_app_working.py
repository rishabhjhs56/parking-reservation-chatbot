import streamlit as st
from app.graph.workflow import build_graph
from app.agents.admin_agent import AdminAgent
import pandas as pd
from app.graph.workflow import build_graph
from app.utils.config import ADMIN_PANEL_PASSWORD

# ----------------------------
# Build LangGraph once
# ----------------------------
graph = build_graph()
admin = AdminAgent()

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

    mode = st.radio("Select Module",["User Chat", "Admin Dashboard"])

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

# ==========================================================
# USER CHAT
# ==========================================================

if mode == "User Chat":

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
    # Previous Messages
    # ----------------------------
    for msg in st.session_state.messages:

        avatar = "👤" if msg["role"] == "user" else "🚗"

        with st.chat_message(msg["role"], avatar=avatar):

            if msg["role"] == "assistant" and msg.get("reservation"):

                reservation = msg["reservation"]

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

                st.info(f"**Status:** {reservation.get('Status','Pending Admin Approval ⏳')}")

            else:

                st.markdown(msg["content"])

    # ----------------------------
    # Chat Input
    # ----------------------------
    prompt = st.chat_input(
        "Ask about parking, charges, availability or book a parking slot..."
    )

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

        # -----------------------------------
        # Reservation Summary Formatter
        # -----------------------------------

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
        

        reservation = format_reservation_summary(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "reservation": reservation
            }
        )

        with st.chat_message("assistant"):

            #reservation = format_reservation_summary(answer)

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

    st.divider()

# ==========================================================
# ADMIN Dashboard
# ==========================================================

if mode == "Admin Dashboard":

    st.header("🔐 SmartPark AI - Admin Dashboard")

    password = st.text_input(
        "Admin Password",
        type="password"
    )

    if password != ADMIN_PANEL_PASSWORD:
        st.warning("Please enter the correct Admin Password.")
        st.stop()

    st.success("✅ Logged in as Administrator")

    tab1, tab2, tab3 = st.tabs(
        [
            "🟡 Pending Reservations",
            "🟢 Approved Reservations",
            "🔴 Rejected Reservations"
        ]
    )

    # ==========================================================
    # PENDING TAB
    # ==========================================================

    with tab1:

        reservations = admin.db.get_pending_reservations()

        if len(reservations) == 0:

            st.info("No Pending Reservations.")

        else:

            df = pd.DataFrame([dict(x) for x in reservations])

            st.dataframe(
                df,
                use_container_width=True
            )

            selected = st.multiselect(
                "Select Pending Reservation IDs",
                df["reservation_id"].tolist(),
                key="pending_ids"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Approve Selected",
                    use_container_width=True
                ):

                    if len(selected) == 0:
                        st.warning("Select at least one reservation.")

                    else:

                        for rid in selected:
                            admin.approve_reservation(rid)

                        st.success("Reservation(s) Approved Successfully.")
                        st.rerun()

            with col2:

                if st.button(
                    "❌ Reject Selected",
                    use_container_width=True
                ):

                    if len(selected) == 0:
                        st.warning("Select at least one reservation.")

                    else:

                        for rid in selected:
                            admin.reject_reservation(rid)

                        st.success("Reservation(s) Rejected Successfully.")
                        st.rerun()

    # ==========================================================
    # APPROVED TAB
    # ==========================================================

    with tab2:

        reservations = admin.db.get_approved_reservations()

        if len(reservations) == 0:

            st.info("No Approved Reservations.")

        else:

            df = pd.DataFrame([dict(x) for x in reservations])

            st.dataframe(
                df,
                use_container_width=True
            )

            selected = st.multiselect(
                "Select Approved Reservation IDs",
                df["reservation_id"].tolist(),
                key="approved_ids"
            )

            if st.button(
                "↩ Move Selected To Pending",
                use_container_width=True
            ):

                if len(selected) == 0:

                    st.warning("Select at least one reservation.")

                else:

                    for rid in selected:
                        admin.pending_reservation(rid)

                    st.success("Reservation(s) moved back to Pending.")
                    st.rerun()

    # ==========================================================
    # REJECTED TAB
    # ==========================================================

    with tab3:

        reservations = admin.db.get_rejected_reservations()

        if len(reservations) == 0:

            st.info("No Rejected Reservations.")

        else:

            df = pd.DataFrame([dict(x) for x in reservations])

            st.dataframe(
                df,
                use_container_width=True
            )

            selected = st.multiselect(
                "Select Rejected Reservation IDs",
                df["reservation_id"].tolist(),
                key="rejected_ids"
            )

            if st.button(
                "↩ Move Selected To Pending",
                key="reject_pending",
                use_container_width=True
            ):

                if len(selected) == 0:

                    st.warning("Select at least one reservation.")

                else:

                    for rid in selected:
                        admin.pending_reservation(rid)

                    st.success("Reservation(s) moved back to Pending.")
                    st.rerun()

    st.caption(
        "🚗 SmartPark AI • LangGraph • Azure OpenAI • Milvus • SQLite"
    )

