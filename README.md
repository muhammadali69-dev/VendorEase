# 📈 VendorEase — Smart Profit & Sales Tracker

A Streamlit web app for street vendors to track sales, expenses, inventory and profit.

## 🚀 Deploy to Streamlit Cloud (5 minutes)

### Step 1 — Create GitHub repo
1. Go to https://github.com/new
2. Name it `vendorease`
3. Set to **Public**
4. Click **Create repository**

### Step 2 — Upload files
Upload these files maintaining the folder structure:
```
vendorease/
├── app.py
├── data_utils.py
├── requirements.txt
├── seed_data.py
├── pages_code/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── add_sale.py
│   ├── expenses.py
│   ├── inventory.py
│   ├── reports.py
│   └── settings.py
```

To upload: In your GitHub repo click **Add file → Upload files**, drag all files, commit.

For the `pages_code/` folder: click **Add file → Create new file**, type `pages_code/__init__.py` as the filename, leave it empty, commit. Then upload the other pages_code files.

### Step 3 — Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **New app**
4. Select your `vendorease` repo
5. Set **Main file path** to `app.py`
6. Click **Deploy!**

Your app will be live at: `https://your-username-vendorease-app-xxxx.streamlit.app`

## 🖥️ Run Locally
```bash
pip install -r requirements.txt
python seed_data.py   # optional: adds 14 days of sample data
streamlit run app.py
```

## 📱 Features
- **Dashboard** — daily KPIs, profit, weekly chart, recent transactions
- **Add Sale** — quick transaction entry with live total calculation
- **Expenses** — log costs by category with pie chart breakdown
- **Inventory** — stock tracking with low-stock alerts
- **Reports** — weekly/monthly P&L with charts and CSV export
- **Settings** — stall name, currency, categories
