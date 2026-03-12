import streamlit as st
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import data_utils as du
from datetime import date

EXPENSE_CATS = ["Raw Materials", "Transport", "Packaging", "Rent/Space", "Utilities", "Labour", "Other"]

def show():
    settings = du.load_settings()
    curr = settings.get("currency", "₹")

    st.markdown("""
    <div class='section-header'>💸 Expenses</div>
    <div class='section-sub'>Track all your costs to know your real profit</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("### ➕ Log Expense")
        with st.form("expense_form", clear_on_submit=True):
            description = st.text_input("Description", placeholder="e.g. Milk purchase, Vegetable stock...")
            category    = st.selectbox("Category", EXPENSE_CATS)
            amount      = st.number_input(f"Amount ({curr})", min_value=0.0, value=0.0, step=1.0)
            submitted   = st.form_submit_button("💸 Log Expense", use_container_width=True)

            if submitted:
                if not description.strip():
                    st.error("Please enter a description.")
                elif amount <= 0:
                    st.error("Please enter a valid amount.")
                else:
                    du.add_expense(description.strip(), category, amount)
                    st.success(f"✅ Expense logged: {description} — {curr}{amount:,.2f}")

    with col2:
        st.markdown("### 📊 Today's Expenses")
        expenses = du.load_expenses()
        today = date.today()
        if not expenses.empty:
            today_exp = expenses[expenses["date"].dt.date == today]
            if not today_exp.empty:
                today_total = today_exp["amount"].sum()
                st.markdown(f"""
                <div style='background:#c0392b; border-radius:12px; padding:16px; color:white; margin-bottom:14px'>
                    <div style='font-size:12px; opacity:0.8'>Today's Total Expenses</div>
                    <div style='font-size:28px; font-weight:700'>{curr}{today_total:,.2f}</div>
                    <div style='font-size:12px; opacity:0.8'>{len(today_exp)} entries</div>
                </div>
                """, unsafe_allow_html=True)
                for _, row in today_exp.sort_values("date", ascending=False).iterrows():
                    st.markdown(f"""
                    <div style='border:1px solid #fdd; border-radius:10px; padding:10px 14px; margin-bottom:8px; background:white'>
                        <div style='font-weight:600; color:#7a1f1f'>{row['description']}</div>
                        <div style='font-size:12px; color:#999'>{row['category']}</div>
                        <div style='font-size:15px; font-weight:700; color:#c0392b; float:right; margin-top:-28px'>{curr}{row['amount']}</div>
                        <div style='clear:both'></div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No expenses logged today.")
        else:
            st.info("No expenses recorded yet.")

    # ── History & Chart ───────────────────────────────────────────────────────
    st.markdown("---")
    expenses = du.load_expenses()
    if not expenses.empty:
        col_chart, col_table = st.columns([1, 1.5])
        with col_chart:
            st.markdown("### 🥧 Expenses by Category")
            cat_totals = expenses.groupby("category")["amount"].sum().reset_index()
            fig = px.pie(cat_totals, values="amount", names="category",
                         color_discrete_sequence=px.colors.qualitative.Set2,
                         hole=0.45)
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(
                showlegend=False,
                margin=dict(l=0, r=0, t=20, b=0),
                height=280,
                paper_bgcolor="white",
                font=dict(family="Plus Jakarta Sans, sans-serif")
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_table:
            st.markdown("### 📅 Expense History")
            n_rows = st.slider("Show last N records", 10, 200, 30, key="exp_slider")
            display = expenses.copy().sort_values("date", ascending=False).head(n_rows)
            display["date"] = display["date"].dt.strftime("%d %b %Y %H:%M")
            display["amount"] = curr + display["amount"].astype(str)
            st.dataframe(
                display[["date","description","category","amount"]].rename(columns={
                    "date":"Date","description":"Description","category":"Category","amount":"Amount"
                }),
                use_container_width=True, hide_index=True
            )
        csv = expenses.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Expenses CSV", csv, "expenses.csv", "text/csv")
    else:
        st.info("No expenses yet. Log your first cost above!")
