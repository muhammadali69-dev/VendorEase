import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import data_utils as du


def show():

    st.title("⚙️ Settings")

    st.caption(
        "Customize VendorEase for your stall"
    )

    settings = du.load_settings()

    col1, col2 = st.columns([1.2, 1])

    # ─────────────────────────────────────────────
    # SETTINGS FORM
    # ─────────────────────────────────────────────
    with col1:

        st.subheader("🏪 Stall Information")

        with st.form("settings_form"):

            stall_name = st.text_input(
                "Stall Name",
                value=settings.get(
                    "stall_name",
                    "My Stall"
                )
            )

            owner_name = st.text_input(
                "Owner Name",
                value=settings.get(
                    "owner_name",
                    ""
                )
            )

            currencies = [
                "₹",
                "$",
                "€",
                "£",
                "৳",
                "රු"
            ]

            current_currency = settings.get(
                "currency",
                "₹"
            )

            currency = st.selectbox(
                "Currency Symbol",
                currencies,
                index=(
                    currencies.index(current_currency)
                    if current_currency in currencies
                    else 0
                )
            )

            categories = st.text_area(
                "Product Categories",
                value=settings.get(
                    "categories",
                    "Food,Beverages,Snacks,Vegetables,Other"
                ),
                help="Comma-separated categories"
            )

            saved = st.form_submit_button(
                "💾 Save Settings",
                use_container_width=True
            )

            if saved:

                du.save_settings(
                    stall_name,
                    currency,
                    owner_name,
                    categories
                )

                st.success(
                    "✅ Settings saved successfully!"
                )

                st.rerun()

    # ─────────────────────────────────────────────
    # PROFILE PANEL
    # ─────────────────────────────────────────────
    with col2:

        st.subheader("🪪 Your Profile")

        st.markdown("## 🏪")

        st.markdown(
            f"### {settings.get('stall_name', 'My Stall')}"
        )

        if settings.get("owner_name"):

            st.write(
                f"Owner: {settings.get('owner_name')}"
            )

        st.write(
            f"Currency: {settings.get('currency', '₹')}"
        )

        if settings.get("premium"):

            st.success("💎 Premium Account")

        else:

            st.info("🆓 Free Plan")

        st.markdown("---")

        st.subheader("📊 Data Summary")

        sales = du.load_sales()

        expenses = du.load_expenses()

        inventory = du.load_inventory()

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Sales",
            len(sales)
        )

        c2.metric(
            "Expenses",
            len(expenses)
        )

        c3.metric(
            "Inventory",
            len(inventory)
        )

    # ─────────────────────────────────────────────
    # ABOUT SECTION
    # ─────────────────────────────────────────────
    st.markdown("---")

    st.info(
        "VendorEase — Smart Profit & Sales Tracker "
        "for Street Vendors 📈"
    )
