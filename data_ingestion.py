# data_ingestion.py - Module for data loading and preprocessing

import pandas as pd

def load_data():
    """Simulate data ingestion from an ERP/POS source (here using CSV or SQL)."""
    # Example: Read from a CSV file or database table
    try:
        inventory_df = pd.read_csv("data/inventory_positions.csv")
    except FileNotFoundError:
        # Fallback: create dummy data if CSV not available
        inventory_data = {
            "SKU": ["SKU1", "SKU2", "SKU3", "SKU4"],
            "Category": ["Beverages", "Beverages", "Snacks", "Snacks"],
            "Shelf_ID": ["Shelf_A1", "Shelf_A2", "Shelf_B1", "Shelf_B2"],
            "Shelf_Capacity": [50, 50, 30, 30],      # max units that can be placed on shelf
            "Current_OnShelf": [20, 5, 30, 10],      # units currently on shelf
            "Backroom_Stock": [30, 20, 10, 5],       # units in back storage
            "Daily_Sales_Rate": [5, 2, 4, 3]         # average daily units sold
        }
        inventory_df = pd.DataFrame(inventory_data)
    return inventory_df

def preprocess_data(df):
    """Clean and enrich the data frame with additional features needed by models."""
    df = df.copy()
    # Ensure correct data types
    df["Daily_Sales_Rate"] = df["Daily_Sales_Rate"].astype(float)
    df["Shelf_Capacity"]   = df["Shelf_Capacity"].astype(int)
    df["Current_OnShelf"]  = df["Current_OnShelf"].astype(int)
    # Compute total current stock (shelf + backroom)
    df["Total_Stock"] = df["Current_OnShelf"] + df.get("Backroom_Stock", 0)
    # Feature: Shelf utilization percentage
    df["Shelf_Utilization"] = (df["Current_OnShelf"] / df["Shelf_Capacity"]) * 100
    # Feature: Days of cover (how many days will stock last at current sales rate)
    df["Days_of_Cover"] = df["Total_Stock"] / df["Daily_Sales_Rate"]
    # Replace infinite or undefined Days_of_Cover (if Daily_Sales_Rate is 0) with a large number
    df["Days_of_Cover"].replace([float("inf"), None, pd.NA], 9999, inplace=True)
    # Categorize risk level based on days of cover (e.g., less than 2 days = high risk)
    df["Stockout_Risk"] = df["Days_of_Cover"].apply(lambda x: "High" if x < 2 else ("Medium" if x < 5 else "Low"))
    return df

# Example usage:
raw_df = load_data()
clean_df = preprocess_data(raw_df)
print(clean_df.head())
