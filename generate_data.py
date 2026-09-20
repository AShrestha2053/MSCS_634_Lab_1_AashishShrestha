"""
Generate a self-created retail 'sales_data.csv' dataset for MSCS 634 Lab 1.

The dataset is intentionally designed so the lab steps have real work to do:
  - several columns contain MISSING VALUES (for the missing-value section)
  - a few rows contain OUTLIERS (for the IQR outlier section)
  - it mixes numeric + categorical columns and spans a date range
    (so scatter / line / bar / histogram / box / pie plots are all meaningful)
"""

import numpy as np
import pandas as pd

# Reproducible so the numbers are stable every run
rng = np.random.default_rng(42)

N = 600  # number of order records

# ---- Categorical building blocks -------------------------------------------
regions = ["North", "South", "East", "West", "Central"]
categories = ["Electronics", "Furniture", "Clothing", "Groceries", "Toys"]

products = {
    "Electronics": ["Wireless Earbuds", "Smart Watch", "Bluetooth Speaker", "USB-C Charger"],
    "Furniture":   ["Office Chair", "Study Desk", "Bookshelf", "Floor Lamp"],
    "Clothing":    ["Cotton T-Shirt", "Denim Jeans", "Hooded Sweatshirt", "Running Shorts"],
    "Groceries":   ["Organic Coffee", "Green Tea Pack", "Olive Oil", "Granola Bars"],
    "Toys":        ["Building Blocks", "Puzzle Set", "RC Car", "Board Game"],
}

sales_reps = ["Alice", "Bob", "Carlos", "Diana", "Emma", "Frank"]

# Rough price bands per category (min, max) so prices look believable
price_band = {
    "Electronics": (25, 250),
    "Furniture":   (40, 400),
    "Clothing":    (10, 90),
    "Groceries":   (5, 45),
    "Toys":        (8, 120),
}

# ---- Build each record ------------------------------------------------------
order_ids, dates, region_col, category_col, product_col = [], [], [], [], []
units_col, price_col, discount_col, rating_col, rep_col = [], [], [], [], []

date_pool = pd.date_range("2023-01-01", "2024-12-31", freq="D")

for i in range(N):
    cat = rng.choice(categories)
    lo, hi = price_band[cat]

    order_ids.append(f"ORD-{10000 + i}")
    dates.append(rng.choice(date_pool))
    region_col.append(rng.choice(regions))
    category_col.append(cat)
    product_col.append(rng.choice(products[cat]))
    units_col.append(int(rng.integers(1, 40)))          # typical units 1..39
    price_col.append(round(float(rng.uniform(lo, hi)), 2))
    discount_col.append(round(float(rng.choice([0, 5, 10, 15, 20, 25])), 2))
    rating_col.append(round(float(rng.uniform(2.5, 5.0)), 1))
    rep_col.append(rng.choice(sales_reps))

df = pd.DataFrame({
    "Order_ID": order_ids,
    "Order_Date": pd.to_datetime(dates),
    "Region": region_col,
    "Product_Category": category_col,
    "Product_Name": product_col,
    "Units_Sold": units_col,
    "Unit_Price": price_col,
    "Discount_Percent": discount_col,
    "Customer_Rating": rating_col,
    "Sales_Rep": rep_col,
})

# ---- Inject OUTLIERS (before computing totals so totals get big too) --------
outlier_idx = rng.choice(df.index, size=8, replace=False)
df.loc[outlier_idx[:4], "Units_Sold"] = rng.integers(400, 650, size=4)   # huge quantities
df.loc[outlier_idx[4:], "Unit_Price"] = rng.uniform(1500, 2500, size=4)  # very high prices

# ---- Derived numeric column: Total_Sales (kept complete) -------------------
df["Total_Sales"] = (
    df["Units_Sold"] * df["Unit_Price"] * (1 - df["Discount_Percent"] / 100)
).round(2)

# Shipping cost roughly scales with units, plus noise
df["Shipping_Cost"] = (df["Units_Sold"] * rng.uniform(0.4, 1.2, size=N) + 5).round(2)

# ---- Inject MISSING VALUES into a few columns ------------------------------
def blank_out(col, frac):
    idx = rng.choice(df.index, size=int(frac * N), replace=False)
    df.loc[idx, col] = np.nan

blank_out("Discount_Percent", 0.08)   # ~8% missing
blank_out("Customer_Rating", 0.10)    # ~10% missing
blank_out("Region", 0.05)             # ~5% missing

# Sort by date for nice line plots and save
df = df.sort_values("Order_Date").reset_index(drop=True)
df.to_csv("sales_data.csv", index=False)

print("Saved sales_data.csv")
print("Shape:", df.shape)
print("\nMissing values per column:")
print(df.isnull().sum())
print("\nHead:")
print(df.head())
