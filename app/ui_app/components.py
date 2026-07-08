import streamlit as st


def show_reservation_card(reservation):

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

    st.info(
        f"Status : {reservation.get('Status', 'Pending Admin Approval ⏳')}"
    )