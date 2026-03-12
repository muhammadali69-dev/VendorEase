import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_utils as du

UNITS = ["kg", "g", "litre", "ml", "pieces", "packets", "dozen", "bundle"]

def show():
    settings = du.load_settings()
    curr = settings.get("currency", "₹")
    cats = [c.strip() for c in settings.get("categories", "Food,Beverages,Snacks,Vegetables,Other").split(",")]

    st.markdown("""
    <div class='section-header'>📦 Inventory</div>
    <div class='section-sub'>Keep track of your stock levels and get low-stock alerts</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.8])

    with col1:
        st.markdown("### ➕ Add / Restock Item")
        with st.form("inventory_form", clear_on_submit=True):
            item     = st.text_input("Item Name", placeholder="e.g. Milk, Tea Leaves...")
            category = st.selectbox("Category", cats)
            c1, c2   = st.columns(2)
            with c1:
                quantity = st.number_input("Quantity", min_value=0.0, value=1.0, step=0.5)
            with c2:
                unit = st.selectbox("Unit", UNITS)
            alert_at = st.number_input("Alert when below", min_value=0.0, value=2.0, step=0.5,
                                       help="You'll see a warning when stock falls below this level")
            submitted = st.form_submit_button("📦 Add to Inventory", use_container_width=True)
            if submitted:
                if not item.strip():
                    st.error("Please enter an item name.")
                else:
                    du.add_inventory_item(item.strip(), category, quantity, unit, alert_at)
                    st.success(f"✅ {item} added/updated in inventory!")
                    st.rerun()

    with col2:
        st.markdown("### 📋 Current Stock")
        inventory = du.load_inventory()

        if not inventory.empty:
            # Summary badges
            total_items = len(inventory)
            low_items   = len(inventory[inventory["quantity"] <= inventory["low_stock_alert"]])
            ok_items    = total_items - low_items

            b1, b2, b3 = st.columns(3)
            with b1:
                st.markdown(f"""<div style='background:#e8f5f0;border-radius:10px;padding:12px;text-align:center'>
                    <div style='font-size:22px;font-weight:700;color:#0d5c44'>{total_items}</div>
                    <div style='font-size:12px;color:#6b7c74'>Total Items</div></div>""", unsafe_allow_html=True)
            with b2:
                st.markdown(f"""<div style='background:#e8f5e8;border-radius:10px;padding:12px;text-align:center'>
                    <div style='font-size:22px;font-weight:700;color:#2e7d32'>{ok_items}</div>
                    <div style='font-size:12px;color:#6b7c74'>In Stock</div></div>""", unsafe_allow_html=True)
            with b3:
                bg = "#fef0f0" if low_items > 0 else "#e8f5f0"
                color = "#c0392b" if low_items > 0 else "#0d5c44"
                st.markdown(f"""<div style='background:{bg};border-radius:10px;padding:12px;text-align:center'>
                    <div style='font-size:22px;font-weight:700;color:{color}'>{low_items}</div>
                    <div style='font-size:12px;color:#6b7c74'>Low Stock</div></div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Editable stock table
            st.markdown("**Edit quantities directly in the table:**")
            edit_df = inventory.copy()
            edited = st.data_editor(
                edit_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "item":           st.column_config.TextColumn("Item"),
                    "category":       st.column_config.SelectboxColumn("Category", options=cats),
                    "quantity":       st.column_config.NumberColumn("Quantity", min_value=0),
                    "unit":           st.column_config.SelectboxColumn("Unit", options=UNITS),
                    "low_stock_alert":st.column_config.NumberColumn("Alert Below", min_value=0),
                }
            )
            if st.button("💾 Save Changes"):
                du.save_inventory(edited)
                st.success("✅ Inventory saved!")
                st.rerun()

            # Low stock alerts
            low_stock = inventory[inventory["quantity"] <= inventory["low_stock_alert"]]
            if not low_stock.empty:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### ⚠️ Low Stock Alerts")
                for _, row in low_stock.iterrows():
                    st.markdown(f"""
                    <div class='alert-red'>
                        ⚠️ <strong>{row['item']}</strong> — only <strong>{row['quantity']} {row['unit']}</strong> remaining
                        (restock alert set at {row['low_stock_alert']} {row['unit']})
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No inventory items yet. Add your first item on the left!")
