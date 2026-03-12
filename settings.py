import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_utils as du

def show():
    st.markdown("""
    <div class='section-header'>⚙️ Settings</div>
    <div class='section-sub'>Customize VendorEase for your stall</div>
    """, unsafe_allow_html=True)

    settings = du.load_settings()

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("### 🏪 Stall Information")
        with st.form("settings_form"):
            stall_name  = st.text_input("Stall Name",   value=settings.get("stall_name", "My Stall"))
            owner_name  = st.text_input("Owner Name",   value=settings.get("owner_name", ""))
            currency    = st.selectbox("Currency Symbol",["₹", "$", "€", "£", "৳", "රු"],
                                       index=["₹","$","€","£","৳","රු"].index(settings.get("currency","₹"))
                                       if settings.get("currency","₹") in ["₹","$","€","£","৳","රු"] else 0)
            st.markdown("**Product Categories** (comma-separated)")
            categories  = st.text_area("Categories",
                                       value=settings.get("categories","Food,Beverages,Snacks,Vegetables,Other"),
                                       help="These show up in the Add Sale and Inventory dropdowns")

            saved = st.form_submit_button("💾 Save Settings", use_container_width=True)
            if saved:
                du.save_settings(stall_name, currency, owner_name, categories)
                st.success("✅ Settings saved!")
                st.rerun()

    with col2:
        st.markdown("### 📱 Your Profile")
        sname = settings.get("stall_name","My Stall")
        oname = settings.get("owner_name","")
        curr  = settings.get("currency","₹")
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#0a3d2e,#0d5c44);border-radius:16px;
                    padding:28px;color:white;text-align:center'>
            <div style='font-size:48px'>🏪</div>
            <div style='font-size:22px;font-weight:700;margin-top:8px'>{sname}</div>
            {f"<div style='font-size:14px;opacity:0.8;margin-top:4px'>Owner: {oname}</div>" if oname else ""}
            <div style='font-size:13px;opacity:0.7;margin-top:4px'>Currency: {curr}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📊 Data Summary")
        sales     = du.load_sales()
        expenses  = du.load_expenses()
        inventory = du.load_inventory()

        st.markdown(f"""
        <div style='border:1px solid #e0ede8;border-radius:12px;padding:20px;background:white'>
            <div style='display:flex;justify-content:space-between;padding:8px 0;
                        border-bottom:1px solid #f0f0f0'>
                <span style='color:#666'>Total Sale Records</span>
                <span style='font-weight:600;color:#0d5c44'>{len(sales)}</span>
            </div>
            <div style='display:flex;justify-content:space-between;padding:8px 0;
                        border-bottom:1px solid #f0f0f0'>
                <span style='color:#666'>Total Expense Records</span>
                <span style='font-weight:600;color:#c0392b'>{len(expenses)}</span>
            </div>
            <div style='display:flex;justify-content:space-between;padding:8px 0'>
                <span style='color:#666'>Inventory Items</span>
                <span style='font-weight:600;color:#0a3d2e'>{len(inventory)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── About ──────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center;padding:20px;color:#6b7c74;font-size:13px'>
        <strong style='color:#0a3d2e'>VendorEase</strong> — Smart Profit & Sales Tracker for Street Vendors<br>
        Helping India's 10M+ street vendors digitize their business 📈
    </div>
    """, unsafe_allow_html=True)
