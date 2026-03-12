import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_utils as du
from datetime import date, timedelta

def show():
    summary = du.today_summary()
    curr = summary["currency"]

    st.markdown(f"""
    <div style='margin-bottom:8px'>
        <div class='section-header'>👋 Good day, {summary['stall_name']}</div>
        <div class='section-sub'>Here's how your business is doing today — {date.today().strftime('%d %B %Y')}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💰 Today's Sales", f"{curr}{summary['total_sales']:,.2f}")
    with c2:
        st.metric("💸 Today's Expenses", f"{curr}{summary['total_expenses']:,.2f}")
    with c3:
        delta_color = "normal" if summary["profit"] >= 0 else "inverse"
        st.metric("📈 Net Profit", f"{curr}{summary['profit']:,.2f}",
                  delta=f"{'+' if summary['profit']>=0 else ''}{curr}{summary['profit']:,.2f}")
    with c4:
        st.metric("🏆 Top Item", summary["top_item"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Weekly Chart ─────────────────────────────────────────────────────────
    weekly = du.weekly_summary()
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("<div class='section-header' style='font-size:16px'>📅 Last 7 Days</div>", unsafe_allow_html=True)
        if not weekly.empty:
            fig = go.Figure()
            dates_str = [d.strftime("%a %d") for d in weekly["date"]]
            fig.add_trace(go.Bar(name="Sales", x=dates_str, y=weekly["Sales"],
                                 marker_color="#0d5c44", opacity=0.85))
            fig.add_trace(go.Bar(name="Expenses", x=dates_str, y=weekly["Expenses"],
                                 marker_color="#e05c5c", opacity=0.7))
            fig.add_trace(go.Scatter(name="Profit", x=dates_str, y=weekly["Profit"],
                                     mode="lines+markers", line=dict(color="#f0a500", width=2.5),
                                     marker=dict(size=7)))
            fig.update_layout(
                barmode="group",
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(family="Plus Jakarta Sans, sans-serif", size=12),
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=280,
                yaxis=dict(gridcolor="#f0f0f0", tickprefix=curr),
                xaxis=dict(gridcolor="#f0f0f0")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet. Add your first sale to see the chart!")

    with col_right:
        st.markdown("<div class='section-header' style='font-size:16px'>📊 This Week</div>", unsafe_allow_html=True)
        if not weekly.empty:
            week_sales = weekly["Sales"].sum()
            week_exp   = weekly["Expenses"].sum()
            week_profit = weekly["Profit"].sum()
            margin = (week_profit / week_sales * 100) if week_sales > 0 else 0

            st.metric("Total Sales", f"{curr}{week_sales:,.0f}")
            st.metric("Total Expenses", f"{curr}{week_exp:,.0f}")
            st.metric("Net Profit", f"{curr}{week_profit:,.0f}")
            st.metric("Profit Margin", f"{margin:.1f}%")
        else:
            st.info("Add sales to see weekly totals.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recent Transactions ───────────────────────────────────────────────────
    st.markdown("<div class='section-header' style='font-size:16px'>🕒 Recent Transactions</div>", unsafe_allow_html=True)
    sales = du.load_sales()
    if not sales.empty:
        recent = sales.sort_values("date", ascending=False).head(8).copy()
        recent["date"] = recent["date"].dt.strftime("%d %b %H:%M")
        recent["total"] = curr + recent["total"].astype(str)
        recent["price"] = curr + recent["price"].astype(str)
        st.dataframe(
            recent[["date", "item", "category", "qty", "price", "total"]].rename(columns={
                "date": "Date", "item": "Item", "category": "Category",
                "qty": "Qty", "price": "Unit Price", "total": "Total"
            }),
            use_container_width=True, hide_index=True
        )
    else:
        st.markdown("""
        <div class='alert-green'>
            No sales recorded yet. Click <strong>➕ Add Sale</strong> in the sidebar to log your first transaction!
        </div>
        """, unsafe_allow_html=True)

    # ── Low Stock Warning ─────────────────────────────────────────────────────
    inventory = du.load_inventory()
    if not inventory.empty:
        low = inventory[inventory["quantity"] <= inventory["low_stock_alert"]]
        if not low.empty:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-header' style='font-size:16px'>⚠️ Low Stock Alerts</div>", unsafe_allow_html=True)
            for _, row in low.iterrows():
                st.markdown(f"""
                <div class='alert-red'>
                    ⚠️ <strong>{row['item']}</strong> is running low — only {row['quantity']} {row['unit']} left
                    (alert threshold: {row['low_stock_alert']})
                </div>
                """, unsafe_allow_html=True)
