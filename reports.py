import streamlit as st
import pandas as pd
from datetime import date, timedelta

import data_utils as du


def show():

    st.title("📊 Reports")

    st.caption(
        "Analyze your sales and expenses"
    )

    sales = du.load_sales()

    expenses = du.load_expenses()

    curr = du.load_settings().get(
        "currency",
        "₹"
    )

    # DATE FILTER
    st.subheader("🗓️ Select Period")

    c1, c2 = st.columns(2)

    with c1:

        start = st.date_input(
            "Start Date",
            date.today() - timedelta(days=7)
        )

    with c2:

        end = st.date_input(
            "End Date",
            date.today()
        )

    # FILTER SALES
    period_sales = pd.DataFrame()

    if not sales.empty:

        sales["created_at"] = pd.to_datetime(
            sales["created_at"]
        )

        period_sales = sales[
            (
                sales["created_at"].dt.date >= start
            )
            &
            (
                sales["created_at"].dt.date <= end
            )
        ]

    # FILTER EXPENSES
    period_exp = pd.DataFrame()

    if not expenses.empty:

        expenses["created_at"] = pd.to_datetime(
            expenses["created_at"]
        )

        period_exp = expenses[
            (
                expenses["created_at"].dt.date >= start
            )
            &
            (
                expenses["created_at"].dt.date <= end
            )
        ]

    # SUMMARY
    total_sales = (
        period_sales["total"].sum()
        if not period_sales.empty
        else 0
    )

    total_expenses = (
        period_exp["amount"].sum()
        if not period_exp.empty
        else 0
    )

    profit = total_sales - total_expenses

    # METRICS
    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric(
            "💰 Sales",
            f"{curr}{total_sales:,.2f}"
        )

    with m2:

        st.metric(
            "💸 Expenses",
            f"{curr}{total_expenses:,.2f}"
        )

    with m3:

        st.metric(
            "📈 Profit",
            f"{curr}{profit:,.2f}"
        )

    st.markdown("---")

    # SALES TABLE
    st.subheader("🧾 Sales Records")

    if not period_sales.empty:

        st.dataframe(
            period_sales,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No sales records found."
        )

    st.markdown("---")

    # EXPENSE TABLE
    st.subheader("💳 Expense Records")

    if not period_exp.empty:

        st.dataframe(
            period_exp,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No expense records found."
        )

    st.markdown("---")

    # EXPORTS
    st.subheader("⬇️ Export Data")

    e1, e2 = st.columns(2)

    with e1:

        if not period_sales.empty:

            csv = (
                period_sales
                .to_csv(index=False)
                .encode("utf-8")
            )

            st.download_button(
                "⬇️ Download Sales CSV",
                csv,
                f"sales_{start}_{end}.csv",
                "text/csv"
            )

    with e2:

        if not period_exp.empty:

            csv = (
                period_exp
                .to_csv(index=False)
                .encode("utf-8")
            )

            st.download_button(
                "⬇️ Download Expenses CSV",
                csv,
                f"expenses_{start}_{end}.csv",
                "text/csv"
            )
