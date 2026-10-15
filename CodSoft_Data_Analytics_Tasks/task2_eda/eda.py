"""
CodSoft Task 2: Exploratory Data Analysis (EDA)
Run from the project root: python task2_eda/eda.py
Install: pip install pandas
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "sales_cleaned.csv"
if not INPUT.exists():
    raise FileNotFoundError("Run Task 1 first to create data/sales_cleaned.csv")

df = pd.read_csv(INPUT, parse_dates=["Order_Date"])
print("=== Dataset overview ===")
print(df.shape)
print(df.dtypes)
print("\n=== Descriptive statistics ===")
print(df[["Customer_Age", "Quantity", "Unit_Price", "Sales"]].describe().round(2))
print("\n=== Total sales by product ===")
print(df.groupby("Product")["Sales"].sum().sort_values(ascending=False))
print("\n=== Total sales by region ===")
print(df.groupby("Region")["Sales"].sum().sort_values(ascending=False))
print("\n=== Sales by payment method ===")
print(df.groupby("Payment_Method")["Sales"].sum().sort_values(ascending=False))
print("\n=== Correlation matrix ===")
print(df[["Customer_Age", "Quantity", "Unit_Price", "Sales"]].corr(numeric_only=True).round(2))

monthly = df.assign(Month=df["Order_Date"].dt.to_period("M").astype(str))
print("\n=== Monthly sales ===")
print(monthly.groupby("Month")["Sales"].sum().sort_index())
print("\n=== Potential outliers (IQR rule, Sales) ===")
q1, q3 = df["Sales"].quantile([0.25, 0.75])
iqr = q3 - q1
outliers = df[(df["Sales"] < q1 - 1.5 * iqr) | (df["Sales"] > q3 + 1.5 * iqr)]
print("Outlier rows:", len(outliers))
print(outliers[["Order_ID", "Product", "Sales"]].head(10).to_string(index=False))
