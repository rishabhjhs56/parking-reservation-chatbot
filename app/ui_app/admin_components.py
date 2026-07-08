import streamlit as st
import pandas as pd

from app.agents.admin_agent import AdminAgent

admin = AdminAgent()


# ==========================================================
# Pending Reservations
# ==========================================================

def show_pending_tab():

    reservations = admin.db.get_pending_reservations()

    if len(reservations) == 0:
        st.info("No Pending Reservations.")
        return

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
            use_container_width=True,
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
            use_container_width=True,
        ):

            if len(selected) == 0:

                st.warning("Select at least one reservation.")

            else:

                for rid in selected:
                    admin.reject_reservation(rid)

                st.success("Reservation(s) Rejected Successfully.")
                st.rerun()


# ==========================================================
# Approved Reservations
# ==========================================================

def show_approved_tab():

    reservations = admin.db.get_approved_reservations()

    if len(reservations) == 0:
        st.info("No Approved Reservations.")
        return

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
        use_container_width=True,
    ):

        if len(selected) == 0:

            st.warning("Select at least one reservation.")

        else:

            for rid in selected:
                admin.pending_reservation(rid)

            st.success("Reservation(s) moved back to Pending.")
            st.rerun()


# ==========================================================
# Rejected Reservations
# ==========================================================

def show_rejected_tab():

    reservations = admin.db.get_rejected_reservations()

    if len(reservations) == 0:
        st.info("No Rejected Reservations.")
        return

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
        use_container_width=True,
    ):

        if len(selected) == 0:

            st.warning("Select at least one reservation.")

        else:

            for rid in selected:
                admin.pending_reservation(rid)

            st.success("Reservation(s) moved back to Pending.")
            st.rerun()