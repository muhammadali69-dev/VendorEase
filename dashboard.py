import streamlit as st
import plotly.graph_objects as go
from datetime import date
import data_utils as du


def show():

    summary = du.today_summary()

    curr = summary["currency"]

    settings = du.load_settings()

    premium_status = settings.get("premium")

    

    if premium_status:

        st.success("💎 Premium User")

    else:

        st.info("🆓 Free Plan")

    # HEADER
    st.title(f"👋 Good day, {summary['stall_name']}")

    st.caption(
        f"Here's how your business is doing today — "
        f"{date.today().strftime('%d %B %Y')}"
    )

    # KPI ROW
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

    # WEEKLY CHART
    weekly = du.weekly_summary()

    if not weekly.empty:

        fig = go.Figure()

        dates_str = [
            d.strftime("%a")
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
            height=350
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No weekly data available.")

    st.markdown("---")

    # RECENT SALES
    st.subheader("🕒 Recent Transactions")

    sales = du.load_sales()

    if not sales.empty:

        recent = sales.sort_values(
            "created_at",
            ascending=False
        ).head(5)

        st.dataframe(
            recent[
                [
                    "item",
                    "category",
                    "qty",
                    "price",
                    "total"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No sales recorded yet.")
