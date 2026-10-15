"""
CodSoft Task 1: Data Cleaning & Preprocessing
Run from the project root: python task1_data_cleaning/clean_data.py
Install: pip install pandas
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "sales_raw.csv"
OUTPUT = ROOT / "data" / "sales_cleaned.csv"

df = pd.read_csv(INPUT)
print("=== Initial structure ===")
print(df.info())
print("\n=== First 5 rows ===")
print(df.head())
print("\nMissing values before cleaning:\n", df.isna().sum())
print("\nDuplicate rows before cleaning:", df.duplicated().sum())

# Normalize text values
for col in ["Region", "Product", "Payment_Method"]:
    df[col] = df[col].astype("string").str.strip()
df["Region"] = df["Region"].str.title()
df["Product"] = df["Product"].str.title()
df["Payment_Method"] = df["Payment_Method"].str.title()

# Convert columns to appropriate types
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
for col in ["Customer_Age", "Quantity", "Unit_Price", "Sales"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Handle missing / invalid values
df["Customer_Age"] = df["Customer_Age"].fillna(df["Customer_Age"].median())
df["Region"] = df["Region"].fillna("Unknown")
df["Order_Date"] = df["Order_Date"].fillna(df["Order_Date"].mode().iloc[0])
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median()).astype(int)
df["Unit_Price"] = df["Unit_Price"].fillna(df["Unit_Price"].median())
df["Sales"] = df["Quantity"] * df["Unit_Price"]
df = df.drop_duplicates().reset_index(drop=True)

# Export cleaned dataset
df.to_csv(OUTPUT, index=False)
print("\n=== Cleaning summary ===")
print("Rows after cleaning:", len(df))
print("Duplicate rows after cleaning:", df.duplicated().sum())
print("Missing values after cleaning:\n", df.isna().sum())
print(f"\nCleaned dataset saved to: {OUTPUT}")
