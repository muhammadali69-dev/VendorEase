import pandas as pd
import os
from datetime import datetime, timedelta
import random

os.makedirs("data", exist_ok=True)

today = datetime.now()
items = [
    ("Masala Tea",   "Beverages", 10, 20),
    ("Vada Pav",     "Food",       8, 15),
    ("Samosa",       "Snacks",    12, 10),
    ("Cold Drink",   "Beverages",  5, 30),
    ("Cutting Chai", "Beverages", 20, 15),
    ("Bhaji Pav",    "Food",       6, 25),
    ("Biscuits",     "Snacks",     4, 20),
]

sales_rows = []
for day_offset in range(14):
    day = today - timedelta(days=day_offset)
    n_sales = random.randint(8, 20)
    for _ in range(n_sales):
        item, cat, qty, price = random.choice(items)
        qty_sold = random.randint(1, qty)
        t = day.replace(hour=random.randint(8, 20), minute=random.randint(0, 59))
        sales_rows.append({
            "date": t.strftime("%Y-%m-%d %H:%M:%S"),
            "item": item, "category": cat,
            "qty": qty_sold, "price": price,
            "total": round(qty_sold * price, 2)
        })

pd.DataFrame(sales_rows).to_csv("data/sales.csv", index=False)

exp_items = [
    ("Milk purchase",    "Raw Materials", 250),
    ("Vegetable stock",  "Raw Materials", 180),
    ("Tea leaves",       "Raw Materials", 120),
    ("LPG cylinder",     "Utilities",     950),
    ("Packaging bags",   "Packaging",      80),
    ("Auto fare",        "Transport",      60),
]
exp_rows = []
for day_offset in range(14):
    day = today - timedelta(days=day_offset)
    n_exp = random.randint(1, 3)
    for _ in range(n_exp):
        desc, cat, amt = random.choice(exp_items)
        t = day.replace(hour=random.randint(7, 10))
        exp_rows.append({
            "date": t.strftime("%Y-%m-%d %H:%M:%S"),
            "description": desc, "category": cat,
            "amount": amt + random.randint(-20, 20)
        })
pd.DataFrame(exp_rows).to_csv("data/expenses.csv", index=False)

pd.DataFrame([
    {"item":"Milk",        "category":"Beverages","quantity":5,  "unit":"litre",  "low_stock_alert":2},
    {"item":"Tea Leaves",  "category":"Beverages","quantity":1.5,"unit":"kg",     "low_stock_alert":0.5},
    {"item":"Potatoes",    "category":"Vegetables","quantity":3, "unit":"kg",     "low_stock_alert":1},
    {"item":"Bread",       "category":"Food",      "quantity":4, "unit":"packets","low_stock_alert":2},
    {"item":"Oil",         "category":"Raw Materials","quantity":1,"unit":"litre","low_stock_alert":0.5},
]).to_csv("data/inventory.csv", index=False)

pd.DataFrame([{
    "stall_name": "Ali's Stall",
    "currency": "₹",
    "owner_name": "Muhammad Ali",
    "categories": "Food,Beverages,Snacks,Vegetables,Other"
}]).to_csv("data/settings.csv", index=False)

print("✅ Sample data created in data/")
