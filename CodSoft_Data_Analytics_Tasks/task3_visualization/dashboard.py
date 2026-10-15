"""
CodSoft Task 3: Data Visualization
Run from the project root: python task3_visualization/dashboard.py
Install: pip install pandas matplotlib seaborn
Creates PNG charts in output/charts/.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "sales_cleaned.csv"
OUT = ROOT / "output" / "charts"
OUT.mkdir(parents=True, exist_ok=True)
if not INPUT.exists():
    raise FileNotFoundError("Run Task 1 first to create data/sales_cleaned.csv")

df = pd.read_csv(INPUT, parse_dates=["Order_Date"])
sns.set_theme(style="whitegrid")

# 1. Bar chart: sales by product
sales_product = df.groupby("Product", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
plt.figure(figsize=(9, 5))
sns.barplot(data=sales_product, x="Product", y="Sales", color="steelblue")
plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales (INR)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(OUT / "sales_by_product.png", dpi=160)
plt.close()

# 2. Line chart: monthly sales
monthly = df.assign(Month=df["Order_Date"].dt.to_period("M").dt.to_timestamp()).groupby("Month", as_index=False)["Sales"].sum()
plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly, x="Month", y="Sales", marker="o", color="steelblue")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales (INR)")
plt.tight_layout()
plt.savefig(OUT / "monthly_sales_trend.png", dpi=160)
plt.close()

# 3. Pie chart: orders by payment method
payments = df["Payment_Method"].value_counts()
plt.figure(figsize=(7, 7))
plt.pie(payments.values, labels=payments.index, autopct="%1.1f%%", startangle=90)
plt.title("Orders by Payment Method")
plt.tight_layout()
plt.savefig(OUT / "payment_method_distribution.png", dpi=160)
plt.close()

# 4. Histogram: customer age distribution
plt.figure(figsize=(9, 5))
sns.histplot(data=df, x="Customer_Age", bins=12, kde=True, color="steelblue")
plt.title("Customer Age Distribution")
plt.xlabel("Customer Age")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig(OUT / "customer_age_distribution.png", dpi=160)
plt.close()

# 5. Scatter plot: quantity vs sales
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Quantity", y="Sales", hue="Product", palette="deep")
plt.title("Quantity vs Sales")
plt.xlabel("Quantity")
plt.ylabel("Sales (INR)")
plt.tight_layout()
plt.savefig(OUT / "quantity_vs_sales.png", dpi=160)
plt.close()

print("Charts saved to:", OUT)
for p in sorted(OUT.glob("*.png")):
    print("-", p.name)
