import streamlit as st
from app.graph.workflow import build_graph
from app.agents.admin_agent import AdminAgent
from app.ui_app.user_mode import render_user_chat
from app.ui_app.admin_dashboard import show_admin_dashboard

# ----------------------------
# Build LangGraph once
# ----------------------------
@st.cache_resource
def load_graph():
    return build_graph()


@st.cache_resource
def load_admin():
    return AdminAgent()


graph = load_graph()
admin = load_admin()
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

    mode = st.radio(
        "Select Module",
        [
            "User Chat",
            "Admin Dashboard"
        ]
    )

    st.markdown("---")

    st.markdown("""
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
""")

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
# Routing
# ----------------------------

if mode == "User Chat":
    render_user_chat(graph)

else:
    show_admin_dashboard(admin)

# ----------------------------
# Footer
# ----------------------------

st.divider()

st.caption(
    "🚗 SmartPark AI • LangGraph • Azure OpenAI • Milvus • SQLite"
)