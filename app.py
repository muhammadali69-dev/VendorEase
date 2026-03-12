import streamlit as st

st.set_page_config(
    page_title="VendorEase",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0a3d2e 0%, #0d5c44 100%);
}
[data-testid="stSidebar"] * {
    color: #e0f5ee !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 15px !important;
    padding: 8px 0 !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e8f5f0;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,100,60,0.06);
}

/* Buttons */
.stButton > button {
    background: #0d5c44;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 28px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    font-size: 14px;
    transition: background 0.2s;
}
.stButton > button:hover {
    background: #0a3d2e;
    color: white;
}

/* DataFrames */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Section headers */
.section-header {
    font-size: 22px;
    font-weight: 700;
    color: #0a3d2e;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 14px;
    color: #6b7c74;
    margin-bottom: 20px;
}

/* Alert boxes */
.alert-green {
    background: #e8f5f0;
    border-left: 4px solid #0d5c44;
    border-radius: 8px;
    padding: 12px 16px;
    color: #0a3d2e;
    font-size: 14px;
}
.alert-red {
    background: #fef0f0;
    border-left: 4px solid #d9534f;
    border-radius: 8px;
    padding: 12px 16px;
    color: #7a1f1f;
    font-size: 14px;
}

/* Hide default header */
header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📈 VendorEase")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Dashboard", "➕ Add Sale", "💸 Expenses", "📦 Inventory", "📊 Reports", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("<small style='opacity:0.6'>Smart Profit & Sales Tracker<br>for Street Vendors</small>", unsafe_allow_html=True)

# ── Page Routing ─────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    import dashboard
    dashboard.show()

elif page == "➕ Add Sale":
    import add_sale
    add_sale.show()

elif page == "💸 Expenses":
    import expenses
    expenses.show()

elif page == "📦 Inventory":
    import inventory
    inventory.show()

elif page == "📊 Reports":
    import reports
    reports.show()

elif page == "⚙️ Settings":
    import settings
    settings.show()
