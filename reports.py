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

    st.markdown("""
    <div class='section-header'>📊 Reports</div>

    <div class='section-sub'>
        Weekly & monthly profit & loss —
        your financial proof
    </div>
    """, unsafe_allow_html=True)

    sales = du.load_sales()

    expenses = du.load_expenses()

    if sales.empty and expenses.empty:

        st.info(
            "No data yet. Start adding sales and expenses to generate reports."
        )

        return

    # ─────────────────────────────────────────────────────────────
    # PERIOD SELECTOR
    # ─────────────────────────────────────────────────────────────
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

    # ─────────────────────────────────────────────────────────────
    # FILTER DATA
    # ─────────────────────────────────────────────────────────────
    def filter_df(df, start, end, column):

        if df.empty:
            return df

        return df[
            (df[column].dt.date >= start)
            &
            (df[column].dt.date <= end)
        ]

    period_sales = filter_df(
        sales,
        start,
        end,
        "created_at"
    ) if not sales.empty else pd.DataFrame()

    period_exp = filter_df(
        expenses,
        start,
        end,
        "date"
    ) if not expenses.empty else pd.DataFrame()

    total_sales = (
        period_sales["total"].sum()
        if not period_sales.empty else 0
    )

    total_exp = (
        period_exp["amount"].sum()
        if not period_exp.empty else 0
    )

    net_profit = total_sales - total_exp

    margin = (
        (net_profit / total_sales) * 100
        if total_sales > 0 else 0
    )

    # ─────────────────────────────────────────────────────────────
    # KPI CARDS
    # ─────────────────────────────────────────────────────────────
    st.markdown(
        f"#### Period: "
        f"{start.strftime('%d %b')} "
        f"→ "
        f"{end.strftime('%d %b %Y')}"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Sales",
            f"{curr}{total_sales:,.2f}"
        )

    with c2:
        st.metric(
            "Total Expenses",
            f"{curr}{total_exp:,.2f}"
        )

    with c3:
        st.metric(
            "Net Profit",
            f"{curr}{net_profit:,.2f}",
            delta=f"{'profit' if net_profit >= 0 else 'loss'}"
        )

    with c4:
        st.metric(
            "Profit Margin",
            f"{margin:.1f}%"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────
    # DAILY TREND CHART
    # ─────────────────────────────────────────────────────────────
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
            y=daily_sales.values,
            marker_color="#0d5c44",
            opacity=0.8
        ))

        fig.add_trace(go.Bar(
            name="Expenses",
            x=dates_str,
            y=daily_exp.values,
            marker_color="#e05c5c",
            opacity=0.75
        ))

        fig.add_trace(go.Scatter(
            name="Net Profit",
            x=dates_str,
            y=profit_line,
            mode="lines+markers",
            line=dict(
                color="#f0a500",
                width=2.5
            ),
            marker=dict(size=6)
        ))

        fig.update_layout(
            barmode="group",
            height=320,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                family="Plus Jakarta Sans, sans-serif",
                size=12
            ),
            margin=dict(
                l=10,
                r=10,
                t=30,
                b=10
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                x=1,
                xanchor="right"
            ),
            yaxis=dict(
                gridcolor="#f0f0f0",
                tickprefix=curr
            ),
            xaxis=dict(
                gridcolor="#f0f0f0"
            ),
            title="Daily Sales vs Expenses"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ─────────────────────────────────────────────────────────────
    # CATEGORY BREAKDOWN
    # ─────────────────────────────────────────────────────────────
    col_l, col_r = st.columns(2)

    with col_l:

        st.markdown("#### 🏷️ Sales by Category")

        if not period_sales.empty:

            cat_sales = (
                period_sales
                .groupby("category")["total"]
                .sum()
                .reset_index()
            )

            fig2 = px.bar(
                cat_sales,
                x="total",
                y="category",
                orientation="h",
                color="total",
                color_continuous_scale=[
                    "#9fe1cb",
                    "#0d5c44"
                ]
            )

            fig2.update_layout(
                height=250,
                margin=dict(
                    l=0,
                    r=0,
                    t=0,
                    b=0
                ),
                paper_bgcolor="white",
                plot_bgcolor="white",
                coloraxis_showscale=False,
                xaxis=dict(
                    tickprefix=curr,
                    gridcolor="#f0f0f0"
                ),
                yaxis=dict(title=""),
                font=dict(
                    family="Plus Jakarta Sans, sans-serif",
                    size=12
                )
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        else:

            st.info(
                "No sales in this period."
            )

    with col_r:

        st.markdown("#### 💸 Expenses by Category")

        if not period_exp.empty:

            cat_exp = (
                period_exp
                .groupby("category")["amount"]
                .sum()
                .reset_index()
            )

            fig3 = px.bar(
                cat_exp,
                x="amount",
                y="category",
                orientation="h",
                color="amount",
                color_continuous_scale=[
                    "#fdd",
                    "#c0392b"
                ]
            )

            fig3.update_layout(
                height=250,
                margin=dict(
                    l=0,
                    r=0,
                    t=0,
                    b=0
                ),
                paper_bgcolor="white",
                plot_bgcolor="white",
                coloraxis_showscale=False,
                xaxis=dict(
                    tickprefix=curr,
                    gridcolor="#f0f0f0"
                ),
                yaxis=dict(title=""),
                font=dict(
                    family="Plus Jakarta Sans, sans-serif",
                    size=12
                )
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

        else:

            st.info(
                "No expenses in this period."
            )

    # ─────────────────────────────────────────────────────────────
    # TOP ITEMS
    # ─────────────────────────────────────────────────────────────
    if not period_sales.empty:

        st.markdown("#### 🏆 Top Selling Items")

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

    # ─────────────────────────────────────────────────────────────
    # PROFIT & LOSS
    # ─────────────────────────────────────────────────────────────
    st.markdown("---")

    st.markdown("#### 📄 Profit & Loss Statement")

    st.markdown(f"""
    <div style='background:white;
                border:1px solid #e0ede8;
                border-radius:14px;
                padding:24px;
                max-width:500px'>

        <div style='font-weight:700;
                    font-size:16px;
                    color:#0a3d2e;
                    margin-bottom:16px'>

            P&L —
            {start.strftime('%d %b')}
            to
            {end.strftime('%d %b %Y')}

        </div>

        <div style='display:flex;
                    justify-content:space-between;
                    padding:8px 0;
                    border-bottom:1px solid #f0f0f0'>

            <span style='color:#333'>
                Gross Revenue
            </span>

            <span style='font-weight:600;
                         color:#0d5c44'>

                {curr}{total_sales:,.2f}

            </span>

        </div>

        <div style='display:flex;
                    justify-content:space-between;
                    padding:8px 0;
                    border-bottom:1px solid #f0f0f0'>

            <span style='color:#333'>
                Total Expenses
            </span>

            <span style='font-weight:600;
                         color:#c0392b'>

                − {curr}{total_exp:,.2f}

            </span>

        </div>

        <div style='display:flex;
                    justify-content:space-between;
                    padding:12px 0;
                    margin-top:4px;
                    border-top:2px solid #0d5c44'>

            <span style='font-weight:700;
                         font-size:16px;
                         color:#0a3d2e'>

                Net Profit

            </span>

            <span style='font-weight:700;
                         font-size:18px;
                         color:{"#0d5c44" if net_profit >= 0 else "#c0392b"}'>

                {curr}{net_profit:,.2f}

            </span>

        </div>

        <div style='font-size:12px;
                    color:#6b7c74;
                    margin-top:8px'>

            Profit Margin:
            {margin:.1f}%

        </div>

    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────
    # EXPORTS
    # ─────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    col_e1, col_e2 = st.columns(2)

    with col_e1:

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

    with col_e2:

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
