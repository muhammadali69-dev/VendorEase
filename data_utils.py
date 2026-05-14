import pandas as pd
import os
from datetime import datetime, date

DATA_DIR = "data"

EXPENSES_FILE = os.path.join(DATA_DIR, "expenses.csv")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.csv")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.csv")


# ── Bootstrap ────────────────────────────────────────────────────────────────
def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def init_files():

    ensure_data_dir()

    if not os.path.exists(EXPENSES_FILE):

        df = pd.DataFrame(
            columns=[
                "date",
                "description",
                "category",
                "amount"
            ]
        )

        df.to_csv(EXPENSES_FILE, index=False)

    if not os.path.exists(INVENTORY_FILE):

        df = pd.DataFrame(
            columns=[
                "item",
                "category",
                "quantity",
                "unit",
                "low_stock_alert"
            ]
        )

        df.to_csv(INVENTORY_FILE, index=False)

    if not os.path.exists(SETTINGS_FILE):

        df = pd.DataFrame([{
            "stall_name": "My Stall",
            "currency": "₹",
            "owner_name": "",
            "categories": "Food,Beverages,Snacks,Vegetables,Other"
        }])

        df.to_csv(SETTINGS_FILE, index=False)


# ── SALES (SUPABASE) ─────────────────────────────────────────────────────────
def load_sales():

    import pandas as pd
    import streamlit as st
    from supabase_client import supabase

    user = st.session_state.get("user")

    user_email = user.email if user else ""

    response = (
        supabase.table("sales")
        .select("*")
        .eq("user_email", user_email)
        .execute()
    )

    df = pd.DataFrame(response.data)

    if not df.empty:

        df["created_at"] = pd.to_datetime(
            df["created_at"]
        )

    return df


def add_sale(item, category, qty, price):

    import streamlit as st
    from supabase_client import supabase

    total = round(qty * price, 2)

    user = st.session_state.get("user")

    user_email = user.email if user else "unknown"

    supabase.table("sales").insert({
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "item": item,
        "category": category,
        "qty": qty,
        "price": price,
        "total": total,
        "user_email": user_email
    }).execute()


# ── EXPENSES (SUPABASE) ─────────────────────────────────────────────
def load_expenses():

    import pandas as pd
    import streamlit as st
    from supabase_client import supabase

    user = st.session_state.get("user")

    user_email = user.email if user else ""

    response = (
        supabase.table("expenses")
        .select("*")
        .eq("user_email", user_email)
        .execute()
    )

    df = pd.DataFrame(response.data)

    if not df.empty:

        df["date"] = pd.to_datetime(
            df["date"]
        )

    return df


def add_expense(description, category, amount):

    import streamlit as st
    from supabase_client import supabase

    user = st.session_state.get("user")

    user_email = user.email if user else "unknown"

    supabase.table("expenses").insert({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": description,
        "category": category,
        "amount": round(amount, 2),
        "user_email": user_email
    }).execute()
# ── INVENTORY (SUPABASE) ────────────────────────────────────────────
def load_inventory():

    import pandas as pd
    import streamlit as st
    from supabase_client import supabase

    user = st.session_state.get("user")

    user_email = user.email if user else ""

    response = (
        supabase.table("inventory")
        .select("*")
        .eq("user_email", user_email)
        .execute()
    )

    df = pd.DataFrame(response.data)

    return df


def add_inventory_item(
    item,
    category,
    quantity,
    unit,
    low_stock_alert
):

    import streamlit as st
    from supabase_client import supabase

    user = st.session_state.get("user")

    user_email = user.email if user else "unknown"

    existing = (
        supabase.table("inventory")
        .select("*")
        .eq("item", item)
        .eq("user_email", user_email)
        .execute()
    )

    if existing.data:

        current_qty = existing.data[0]["quantity"]

        new_qty = current_qty + quantity

        supabase.table("inventory").update({
            "quantity": new_qty
        }).eq(
            "id",
            existing.data[0]["id"]
        ).execute()

    else:

        supabase.table("inventory").insert({
            "item": item,
            "category": category,
            "quantity": quantity,
            "unit": unit,
            "low_stock_alert": low_stock_alert,
            "user_email": user_email
        }).execute()


def save_inventory(df):

    pass


# ── SETTINGS ─────────────────────────────────────────────────────────────────
# ── SETTINGS (SUPABASE) ─────────────────────────────────────────────
def load_settings():

    import streamlit as st
    from supabase_client import supabase

    user = st.session_state.get("user")

    user_email = user.email if user else ""

    response = (
        supabase.table("settings")
        .select("*")
        .eq("user_email", user_email)
        .execute()
    )

    if response.data:

        return response.data[0]

    default_settings = {
        "stall_name": "My Stall",
        "currency": "₹",
        "owner_name": "",
        "categories": "Food,Beverages,Snacks,Vegetables,Other",
        "user_email": user_email
    }

    supabase.table("settings").insert(
        default_settings
    ).execute()

    return default_settings


def save_settings(
    stall_name,
    currency,
    owner_name,
    categories
):

    import streamlit as st
    from supabase_client import supabase

    user = st.session_state.get("user")

    user_email = user.email if user else ""

    existing = (
        supabase.table("settings")
        .select("*")
        .eq("user_email", user_email)
        .execute()
    )

    data = {
        "stall_name": stall_name,
        "currency": currency,
        "owner_name": owner_name,
        "categories": categories,
        "user_email": user_email
    }

    if existing.data:

        supabase.table("settings").update(
            data
        ).eq(
            "user_email",
            user_email
        ).execute()

    else:

        supabase.table("settings").insert(
            data
        ).execute()

# ── ANALYTICS ────────────────────────────────────────────────────────────────
def today_summary():

    settings = load_settings()

    sales = load_sales()

    expenses = load_expenses()

    today = date.today()

    today_sales = (
        sales[sales["created_at"].dt.date == today]
        if not sales.empty
        else pd.DataFrame()
    )

    today_exp = (
        expenses[expenses["date"].dt.date == today]
        if not expenses.empty
        else pd.DataFrame()
    )

    total_sales = (
        today_sales["total"].sum()
        if not today_sales.empty
        else 0
    )

    total_expenses = (
        today_exp["amount"].sum()
        if not today_exp.empty
        else 0
    )

    profit = total_sales - total_expenses

    top_item = (
        today_sales.groupby("item")["total"]
        .sum()
        .idxmax()
        if not today_sales.empty
        else "—"
    )

    return {
        "currency": settings.get("currency", "₹"),
        "stall_name": settings.get("stall_name", "My Stall"),
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        "profit": profit,
        "top_item": top_item,
        "num_transactions": len(today_sales)
    }

def weekly_summary():

    sales = load_sales()

    expenses = load_expenses()

    if sales.empty:

        return pd.DataFrame()

    sales["day"] = sales["created_at"].dt.date

    if not expenses.empty:

        expenses["day"] = expenses["date"].dt.date

    last7 = pd.date_range(
        end=date.today(),
        periods=7
    ).date

    daily_sales = (
        sales.groupby("day")["total"]
        .sum()
        .reindex(last7, fill_value=0)
    )

    daily_exp = (
        expenses.groupby("day")["amount"]
        .sum()
        .reindex(last7, fill_value=0)
        if not expenses.empty
        else pd.Series(0, index=last7)
    )

    df = pd.DataFrame({
        "date": last7,
        "Sales": daily_sales.values,
        "Expenses": daily_exp.values
    })

    df["Profit"] = (
        df["Sales"] - df["Expenses"]
    )

    return df
