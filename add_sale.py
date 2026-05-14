import streamlit as st
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import data_utils as du


def show():

    settings = du.load_settings()

    curr = settings.get("currency", "₹")

    cats = [
        c.strip()
        for c in settings.get(
            "categories",
            "Food,Beverages,Snacks,Vegetables,Other"
        ).split(",")
    ]

    st.markdown("## ➕ Add Sale")

    col1, col2 = st.columns([1.2, 1])

    # ─────────────────────────────────────────────
    # ADD SALE FORM
    # ─────────────────────────────────────────────
    with col1:

        st.markdown("### 🧾 New Transaction")

        with st.form("add_sale_form", clear_on_submit=True):

            item = st.text_input(
                "Item Name",
                placeholder="e.g. Masala Tea"
            )

            category = st.selectbox(
                "Category",
                cats
            )

            c1, c2 = st.columns(2)

            with c1:

                qty = st.number_input(
                    "Quantity",
                    min_value=0.5,
                    value=1.0,
                    step=0.5
                )

            with c2:

                price = st.number_input(
                    f"Price per unit ({curr})",
                    min_value=0.0,
                    value=0.0,
                    step=1.0
                )

            total = qty * price

            st.markdown(
                f"""
                <div style='background:#e8f5f0;
                            border-radius:10px;
                            padding:14px 18px;
                            margin:8px 0'>

                    <span style='font-size:13px;
                                 color:#0a3d2e'>
                        Total Amount
                    </span>

                    <br>

                    <span style='font-size:26px;
                                 font-weight:700;
                                 color:#0d5c44'>
                        {curr}{total:,.2f}
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )

            submitted = st.form_submit_button(
                "✅ Record Sale",
                use_container_width=True
            )

            if submitted:

                if not item.strip():

                    st.error("Please enter item name.")

                elif price <= 0:

                    st.error("Please enter valid price.")

                else:

                    du.add_sale(
                        item.strip(),
                        category,
                        qty,
                        price
                    )

                    st.success(
                        f"Sale added successfully!"
                    )

    # ─────────────────────────────────────────────
    # TODAY SALES
    # ─────────────────────────────────────────────
    with col2:

        st.markdown("### 📋 Today's Sales")

        sales = du.load_sales()

        today = date.today()

        if not sales.empty:

            today_sales = sales[
                sales["created_at"].dt.date == today
            ]

            if not today_sales.empty:

                today_total = today_sales["total"].sum()

                st.metric(
                    "Today's Revenue",
                    f"{curr}{today_total:,.2f}"
                )

                st.metric(
                    "Transactions",
                    len(today_sales)
                )

            else:

                st.info("No sales today yet.")

        else:

            st.info("No sales available.")

    # ─────────────────────────────────────────────
    # SALES HISTORY
    # ─────────────────────────────────────────────
    st.markdown("---")

    st.markdown("### 📅 Sales History")

    if not sales.empty:

        display = sales.copy().sort_values(
            "created_at",
            ascending=False
        )

        display["created_at"] = display[
            "created_at"
        ].dt.strftime("%d %b %Y %H:%M")

        display["price"] = (
            curr + display["price"].astype(str)
        )

        display["total"] = (
            curr + display["total"].astype(str)
        )

        st.dataframe(
            display[
                [
                    "created_at",
                    "item",
                    "category",
                    "qty",
                    "price",
                    "total"
                ]
            ].rename(columns={
                "created_at": "Date",
                "item": "Item",
                "category": "Category",
                "qty": "Qty",
                "price": "Price",
                "total": "Total"
            }),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No sales history available.")
