import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import data_utils as du


def show():

    settings = du.load_settings()

    curr = settings.get("currency", "₹")

    st.title("📊 Reports")

    st.caption(
        "Weekly & monthly profit & loss — your financial proof"
    )

    sales = du.load_sales()

    expenses = du.load_expenses()

    if sales.empty and expenses.empty:

        st.info(
            "No data yet. Start adding sales and expenses to generate reports."
        )

        return

    # ─────────────────────────────────────────────
    # PERIOD SELECTOR
    # ─────────────────────────────────────────────
    period = st.radio(
        "Report Period",
        [
            "This Week",
            "This Month",
            "Last Month",
            "Custom Range"
        ],
        horizontal=True
    )

    today = date.today()

    if period == "This Week":

        start = today - timedelta(days=today.weekday())

        end = today

    elif period == "This Month":

        start = today.replace(day=1)

        end = today

    elif period == "Last Month":

        first_this = today.replace(day=1)

        last_prev = first_this - timedelta(days=1)

        start = last_prev.replace(day=1)

        end = last_prev

    else:

        c1, c2 = st.columns(2)

        with c1:

            start = st.date_input(
                "From",
                value=today - timedelta(days=30)
            )

        with c2:

            end = st.date_input(
                "To",
                value=today
            )

    # ─────────────────────────────────────────────
    # FILTER DATA
    # ─────────────────────────────────────────────
    def filter_df(df, start, end, column):

        if df.empty:

            return df

        return df[
            (df[column].dt.date >= start)
            &
            (df[column].dt.date <= end)
        ]

    period_sales = (
        filter_df(
            sales,
            start,
            end,
            "created_at"
        )
        if not sales.empty
        else pd.DataFrame()
    )

    period_exp = (
        filter_df(
            expenses,
            start,
            end,
            "date"
        )
        if not expenses.empty
        else pd.DataFrame()
    )

    total_sales = (
        period_sales["total"].sum()
        if not period_sales.empty
        else 0
    )

    total_exp = (
        period_exp["amount"].sum()
        if not period_exp.empty
        else 0
    )

    net_profit = total_sales - total_exp

    margin = (
        (net_profit / total_sales) * 100
        if total_sales > 0
        else 0
    )

    # ─────────────────────────────────────────────
    # KPI CARDS
    # ─────────────────────────────────────────────
    st.markdown(
        f"### Period: "
        f"{start.strftime('%d %b')} "
        f"→ "
        f"{end.strftime('%d %b %Y')}"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Sales",
        f"{curr}{total_sales:,.2f}"
    )

    c2.metric(
        "Total Expenses",
        f"{curr}{total_exp:,.2f}"
    )

    c3.metric(
        "Net Profit",
        f"{curr}{net_profit:,.2f}"
    )

    c4.metric(
        "Profit Margin",
        f"{margin:.1f}%"
    )

    # ─────────────────────────────────────────────
    # DAILY TREND CHART
    # ─────────────────────────────────────────────
    if not period_sales.empty or not period_exp.empty:

        date_range = pd.date_range(
            start=start,
            end=end
        ).date

        daily_sales = pd.Series(
            0.0,
            index=date_range
        )

        daily_exp = pd.Series(
            0.0,
            index=date_range
        )

        if not period_sales.empty:

            s = period_sales.copy()

            s["day"] = s["created_at"].dt.date

            g = s.groupby("day")["total"].sum()

            daily_sales = daily_sales.add(
                g,
                fill_value=0
            )

        if not period_exp.empty:

            e = period_exp.copy()

            e["day"] = e["date"].dt.date

            g = e.groupby("day")["amount"].sum()

            daily_exp = daily_exp.add(
                g,
                fill_value=0
            )

        dates_str = [
            d.strftime("%d %b")
            for d in date_range
        ]

        profit_line = (
            daily_sales.values
            -
            daily_exp.values
        )

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name="Sales",
            x=dates_str,
            y=daily_sales.values
        ))

        fig.add_trace(go.Bar(
            name="Expenses",
            x=dates_str,
            y=daily_exp.values
        ))

        fig.add_trace(go.Scatter(
            name="Net Profit",
            x=dates_str,
            y=profit_line,
            mode="lines+markers"
        ))

        fig.update_layout(
            barmode="group",
            height=350,
            title="Daily Sales vs Expenses"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ─────────────────────────────────────────────
    # TOP ITEMS
    # ─────────────────────────────────────────────
    if not period_sales.empty:

        st.subheader("🏆 Top Selling Items")

        top_items = (
            period_sales.groupby("item")
            .agg(
                Total_Revenue=("total", "sum"),
                Units_Sold=("qty", "sum"),
                Transactions=("total", "count")
            )
            .sort_values(
                "Total_Revenue",
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        top_items["Total_Revenue"] = top_items[
            "Total_Revenue"
        ].apply(
            lambda x: f"{curr}{x:,.2f}"
        )

        st.dataframe(
            top_items.rename(columns={
                "item": "Item",
                "Total_Revenue": "Revenue",
                "Units_Sold": "Units Sold",
                "Transactions": "Transactions"
            }),
            use_container_width=True,
            hide_index=True
        )

    # ─────────────────────────────────────────────
    # PROFIT & LOSS
    # ─────────────────────────────────────────────
    st.markdown("---")

    st.subheader("📄 Profit & Loss Statement")

    p1, p2, p3 = st.columns(3)

    p1.metric(
        "Gross Revenue",
        f"{curr}{total_sales:,.2f}"
    )

    p2.metric(
        "Expenses",
        f"{curr}{total_exp:,.2f}"
    )

    p3.metric(
        "Net Profit",
        f"{curr}{net_profit:,.2f}"
    )

    # ─────────────────────────────────────────────
    # EXPORTS
    # ─────────────────────────────────────────────
    st.markdown("---")

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

    st.markdown("---")

    import payment

    payment.premium_upgrade()
   
  
