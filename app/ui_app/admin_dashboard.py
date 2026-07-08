import streamlit as st

from app.utils.config import ADMIN_PANEL_PASSWORD

from app.ui_app.admin_components import (
    show_pending_tab,
    show_approved_tab,
    show_rejected_tab,
)


def show_admin_dashboard(admin):

    st.header("🔐 SmartPark AI - Admin Dashboard")

    password = st.text_input(
        "Admin Password",
        type="password",
    )

    if password != ADMIN_PANEL_PASSWORD:
        st.warning("Please enter the correct Admin Password.")
        st.stop()

    st.success("✅ Logged in as Administrator")

    tab1, tab2, tab3 = st.tabs(
        [
            "🟡 Pending Reservations",
            "🟢 Approved Reservations",
            "🔴 Rejected Reservations",
        ]
    )

    with tab1:
        show_pending_tab()

    with tab2:
        show_approved_tab()

    with tab3:
        show_rejected_tab()

    st.divider()

    st.caption(
        "🚗 SmartPark AI • LangGraph • Azure OpenAI • Milvus • SQLite"
    )