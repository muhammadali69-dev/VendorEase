import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_utils as du

def show():
    settings = du.load_settings()
    curr = settings.get("currency", "₹")
    cats = [c.strip() for c in settings.get("categories", "Food,Beverages,Snacks,Vegetables,Other").split(",")]

    st.markdown("""
    <div class='section-header'>➕ Add Sale</div>
    <div class='section-sub'>Record a new transaction quickly</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("### 🧾 New Transaction")
        with st.form("add_sale_form", clear_on_submit=True):
            item = st.text_input("Item Name", placeholder="e.g. Masala Tea, Vada Pav...")
            category = st.selectbox("Category", cats)
            c1, c2 = st.columns(2)
            with c1:
                qty = st.number_input("Quantity", min_value=0.5, value=1.0, step=0.5)
            with c2:
                price = st.number_input(f"Price per unit ({curr})", min_value=0.0, value=0.0, step=1.0)

            total = qty * price
            st.markdown(f"""
            <div style='background:#e8f5f0; border-radius:10px; padding:14px 18px; margin:8px 0'>
                <span style='font-size:13px; color:#0a3d2e'>Total Amount</span><br>
                <span style='font-size:26px; font-weight:700; color:#0d5c44'>{curr}{total:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)

            submitted = st.form_submit_button("✅ Record Sale", use_container_width=True)

            if submitted:
                if not item.strip():
                    st.error("Please enter an item name.")
                elif price <= 0:
                    st.error("Please enter a valid price.")
                else:
                    du.add_sale(item.strip(), category, qty, price)
                    st.success(f"✅ Sale recorded: {qty}x {item} = {curr}{total:,.2f}")
                    # Update inventory if item exists
                    inventory = du.load_inventory()
                    if item in inventory["item"].values:
                        inventory.loc[inventory["item"] == item, "quantity"] -= qty
                        inventory["quantity"] = inventory["quantity"].clip(lower=0)
                        du.save_inventory(inventory)

    with col2:
        st.markdown("### 📋 Today's Sales")
        sales = du.load_sales()
        from datetime import date
        today = date.today()
        if not sales.empty:
            today_sales = sales[sales["date"].dt.date == today].sort_values("date", ascending=False)
            if not today_sales.empty:
                today_total = today_sales["total"].sum()
                st.markdown(f"""
                <div style='background:#0d5c44; border-radius:12px; padding:16px; color:white; margin-bottom:14px'>
                    <div style='font-size:12px; opacity:0.8'>Today's Total</div>
                    <div style='font-size:28px; font-weight:700'>{curr}{today_total:,.2f}</div>
                    <div style='font-size:12px; opacity:0.8'>{len(today_sales)} transactions</div>
                </div>
                """, unsafe_allow_html=True)

                for idx, row in today_sales.iterrows():
                    st.markdown(f"""
                    <div style='border:1px solid #e0ede8; border-radius:10px; padding:10px 14px; margin-bottom:8px; background:white'>
                        <div style='font-weight:600; color:#0a3d2e'>{row['item']}</div>
                        <div style='font-size:12px; color:#6b7c74'>{row['qty']} × {curr}{row['price']} &nbsp;·&nbsp; {row['category']}</div>
                        <div style='font-size:15px; font-weight:700; color:#0d5c44; float:right; margin-top:-28px'>{curr}{row['total']}</div>
                        <div style='clear:both'></div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No sales recorded today yet.")
        else:
            st.info("No sales yet. Add your first one!")

    # ── Full Sales History ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📅 Sales History")
    if not sales.empty:
        col_f1, col_f2 = st.columns([1, 1])
        with col_f1:
            filter_cat = st.selectbox("Filter by category", ["All"] + cats, key="hist_cat")
        with col_f2:
            n_rows = st.slider("Show last N records", 10, 200, 50)

        display = sales.copy().sort_values("date", ascending=False).head(n_rows)
        if filter_cat != "All":
            display = display[display["category"] == filter_cat]

        display["date"] = display["date"].dt.strftime("%d %b %Y %H:%M")
        display["total"] = curr + display["total"].astype(str)
        display["price"] = curr + display["price"].astype(str)
        st.dataframe(
            display[["date","item","category","qty","price","total"]].rename(columns={
                "date":"Date","item":"Item","category":"Category",
                "qty":"Qty","price":"Unit Price","total":"Total"
            }),
            use_container_width=True, hide_index=True
        )
        csv = sales.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Sales CSV", csv, "sales.csv", "text/csv")
    else:
        st.info("No sales history yet.")
