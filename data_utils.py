import pandas as pd
import os
from datetime import datetime, date

DATA_DIR = "data"
SALES_FILE      = os.path.join(DATA_DIR, "sales.csv")
EXPENSES_FILE   = os.path.join(DATA_DIR, "expenses.csv")
INVENTORY_FILE  = os.path.join(DATA_DIR, "inventory.csv")
SETTINGS_FILE   = os.path.join(DATA_DIR, "settings.csv")

# ── Bootstrap ────────────────────────────────────────────────────────────────
def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def init_files():
    ensure_data_dir()

    if not os.path.exists(SALES_FILE):
        df = pd.DataFrame(columns=["date", "item", "category", "qty", "price", "total"])
        df.to_csv(SALES_FILE, index=False)

    if not os.path.exists(EXPENSES_FILE):
        df = pd.DataFrame(columns=["date", "description", "category", "amount"])
        df.to_csv(EXPENSES_FILE, index=False)

    if not os.path.exists(INVENTORY_FILE):
        df = pd.DataFrame(columns=["item", "category", "quantity", "unit", "low_stock_alert"])
        df.to_csv(INVENTORY_FILE, index=False)

    if not os.path.exists(SETTINGS_FILE):
        df = pd.DataFrame([{
            "stall_name": "My Stall",
            "currency": "₹",
            "owner_name": "",
            "categories": "Food,Beverages,Snacks,Vegetables,Other"
        }])
        df.to_csv(SETTINGS_FILE, index=False)

# ── Sales ────────────────────────────────────────────────────────────────────
def load_sales() -> pd.DataFrame:

    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("vendorease.db")

    try:
        df = pd.read_sql_query(
            "SELECT * FROM sales ORDER BY date DESC",
            conn
        )

        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])

        return df

    except:
        return pd.DataFrame(columns=[
            "date",
            "item",
            "category",
            "qty",
            "price",
            "total"
        ])

    finally:
        conn.close()

def add_sale(item: str, category: str, qty: float, price: float):
    init_files()
    df = load_sales()
    new_row = pd.DataFrame([{
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "item": item,
        "category": category,
        "qty": qty,
        "price": price,
        "total": round(qty * price, 2)
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(SALES_FILE, index=False)

def add_sale(item: str, category: str, qty: float, price: float):

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("vendorease.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        item TEXT,
        category TEXT,
        qty REAL,
        price REAL,
        total REAL
    )
    """)

    total = round(qty * price, 2)

    # Insert sale data
    cursor.execute("""
    INSERT INTO sales (date, item, category, qty, price, total)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        item,
        category,
        qty,
        price,
        total
    ))

    conn.commit()
    conn.close()


def delete_sale(index: int):
    df = load_sales()
    df = df.drop(index=index).reset_index(drop=True)
    df.to_csv(SALES_FILE, index=False)

# ── Expenses ─────────────────────────────────────────────────────────────────
def load_expenses() -> pd.DataFrame:
    init_files()
    df = pd.read_csv(EXPENSES_FILE)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df

def add_expense(description: str, category: str, amount: float):
    init_files()
    df = load_expenses()
    new_row = pd.DataFrame([{
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": description,
        "category": category,
        "amount": round(amount, 2)
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(EXPENSES_FILE, index=False)

def delete_expense(index: int):
    df = load_expenses()
    df = df.drop(index=index).reset_index(drop=True)
    df.to_csv(EXPENSES_FILE, index=False)

# ── Inventory ─────────────────────────────────────────────────────────────────
def load_inventory() -> pd.DataFrame:
    init_files()
    return pd.read_csv(INVENTORY_FILE)

def save_inventory(df: pd.DataFrame):
    df.to_csv(INVENTORY_FILE, index=False)

def add_inventory_item(item: str, category: str, quantity: float, unit: str, low_stock_alert: float):
    init_files()
    df = load_inventory()
    # Update if item exists
    if item in df["item"].values:
        df.loc[df["item"] == item, "quantity"] += quantity
    else:
        new_row = pd.DataFrame([{
            "item": item,
            "category": category,
            "quantity": quantity,
            "unit": unit,
            "low_stock_alert": low_stock_alert
        }])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(INVENTORY_FILE, index=False)

# ── Settings ──────────────────────────────────────────────────────────────────
def load_settings() -> dict:
    init_files()
    df = pd.read_csv(SETTINGS_FILE)
    return df.iloc[0].to_dict()

def save_settings(stall_name: str, currency: str, owner_name: str, categories: str):
    df = pd.DataFrame([{
        "stall_name": stall_name,
        "currency": currency,
        "owner_name": owner_name,
        "categories": categories
    }])
    df.to_csv(SETTINGS_FILE, index=False)

# ── Analytics helpers ─────────────────────────────────────────────────────────
def today_summary():
    settings = load_settings()
    sales = load_sales()
    expenses = load_expenses()
    today = date.today()

    today_sales = sales[sales["date"].dt.date == today] if not sales.empty else pd.DataFrame()
    today_exp   = expenses[expenses["date"].dt.date == today] if not expenses.empty else pd.DataFrame()

    total_sales    = today_sales["total"].sum() if not today_sales.empty else 0
    total_expenses = today_exp["amount"].sum() if not today_exp.empty else 0
    profit         = total_sales - total_expenses
    top_item       = today_sales.groupby("item")["total"].sum().idxmax() if not today_sales.empty else "—"

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

    sales["day"] = sales["date"].dt.date
    expenses["day"] = expenses["date"].dt.date if not expenses.empty else None

    last7 = pd.date_range(end=date.today(), periods=7).date

    daily_sales = sales.groupby("day")["total"].sum().reindex(last7, fill_value=0)
    daily_exp   = expenses.groupby("day")["amount"].sum().reindex(last7, fill_value=0) if not expenses.empty else pd.Series(0, index=last7)

    df = pd.DataFrame({
        "date": last7,
        "Sales": daily_sales.values,
        "Expenses": daily_exp.values
    })
    df["Profit"] = df["Sales"] - df["Expenses"]
    return df
