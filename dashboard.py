import streamlit as st
import plotly.graph_objects as go
import sys
import os

from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import data_utils as du


def show():

    summary = du.today_summary()

    curr = summary["currency"]

    settings = du.load_settings()

    # ─────────────────────────────────────────────
    # PREMIUM STATUS
    # ─────────────────────────────────────────────
    if settings.get("premium"):

        st.success("💎 Premium User")

    else:

        st.warning("🆓 Free Plan")

    # ─────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────
    st.title(f"👋 Good day, {summary['stall_name']}")

    st.caption(
        f"Here's how your business is doing today — "
        f"{date.today().strftime('%d %B %Y')}"
    )

    # ─────────────────────────────────────────────
    # KPI ROW
    # ─────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Today's Sales",
        f"{curr}{summary['total_sales']:,.2f}"
    )

    c2.metric(
        "💸 Today's Expenses",
        f"{curr}{summary['total_expenses']:,.2f}"
    )

    c3.metric(
        "📈 Net Profit",
        f"{curr}{summary['profit']:,.2f}"
    )

    c4.metric(
        "🏆 Top Item",
        summary["top_item"]
    )

    st.markdown("---")

    # ─────────────────────────────────────────────
    # WEEKLY CHART
    # ─────────────────────────────────────────────
    weekly = du.weekly_summary()

    col_left, col_right = st.columns([2, 1])

    with col_left:

        st.subheader("📅 Last 7 Days")

        if not weekly.empty:

            fig = go.Figure()

            dates_str = [
                d.strftime("%a %d")
                for d in weekly["date"]
            ]

            fig.add_trace(go.Bar(
                name="Sales",
                x=dates_str,
                y=weekly["Sales"]
            ))

            fig.add_trace(go.Bar(
                name="Expenses",
                x=dates_str,
                y=weekly["Expenses"]
            ))

            fig.add_trace(go.Scatter(
                name="Profit",
                x=dates_str,
                y=weekly["Profit"],
                mode="lines+markers"
            ))

            fig.update_layout(
                barmode="group",
                height=320
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No data yet. Add your first sale!"
            )

    # ─────────────────────────────────────────────
    # WEEKLY SUMMARY
    # ─────────────────────────────────────────────
    with col_right:

        st.subheader("📊 This Week")

        if not weekly.empty:

            week_sales = weekly["Sales"].sum()

            week_exp = weekly["Expenses"].sum()

            week_profit = weekly["Profit"].sum()

            margin = (
                (week_profit / week_sales) * 100
                if week_sales > 0 else 0
            )

            st.metric(
                "Total Sales",
                f"{curr}{week_sales:,.0f}"
            )

            st.metric(
                "Total Expenses",
                f"{curr}{week_exp:,.0f}"
            )

            st.metric(
                "Net Profit",
                f"{curr}{week_profit:,.0f}"
            )

            st.metric(
                "Profit Margin",
                f"{margin:.1f}%"
            )

        else:

            st.info(
                "No weekly data available."
            )

    st.markdown("---")

    # ─────────────────────────────────────────────
    # RECENT TRANSACTIONS
    # ─────────────────────────────────────────────
    st.subheader("🕒 Recent Transactions")

    sales = du.load_sales()

    if not sales.empty:

        recent = sales.sort_values(
            "created_at",
            ascending=False
        ).head(8).copy()

        recent["created_at"] = recent[
            "created_at"
        ].dt.strftime("%d %b %H:%M")

        recent["total"] = (
            curr + recent["total"].astype(str)
        )

        recent["price"] = (
            curr + recent["price"].astype(str)
        )

        st.dataframe(
            recent[
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
                "price": "Unit Price",
                "total": "Total"
            }),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No sales recorded yet."
        )

    # ─────────────────────────────────────────────
    # LOW STOCK ALERTS
    # ─────────────────────────────────────────────
    inventory = du.load_inventory()

    if not inventory.empty:

        low = inventory[
            inventory["quantity"]
            <= inventory["low_stock_alert"]
        ]

        if not low.empty:

            st.markdown("---")

            st.subheader("⚠️ Low Stock Alerts")

            for _, row in low.iterrows():

                st.warning(
                    f"{row['item']} is running low — "
                    f"{row['quantity']} {row['unit']} left"
                )
