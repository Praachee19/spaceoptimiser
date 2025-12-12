# agent.py - Pseudo-code for AI agent monitoring

import time
from data_ingestion import load_data, preprocess_data
from models import model  # our trained forecasting model (for demo purposes)
from helper_functions import send_alert, recommend_reorder, log_suggestion, auto_order

def monitor_and_act():
    while True:
        # Step 1: Data update - fetch latest inventory status
        df = preprocess_data(load_data())
        # Step 2: Check for low stocks / stockouts
        low_stock_items = df[df["Stockout_Risk"] == "High"]
        for _, item in low_stock_items.iterrows():
            sku = item["SKU"]; stock = item["Total_Stock"]; days = item["Days_of_Cover"]
            alert_msg = f"ALERT: {sku} stock is low (current={stock}, ~{days:.1f} days cover left)."
            send_alert(alert_msg)  # function to notify via email/GUI
            recommend_reorder(sku, item)  # function to create a reorder suggestion

        # Step 3: Check for underutilized shelves
        underutilized = df[df["Shelf_Utilization"] < 30]  # e.g., less than 30% filled
        for _, item in underutilized.iterrows():
            sku = item["SKU"]; util = item["Shelf_Utilization"]
            suggestion = f"Note: Shelf holding {sku} is only {util:.0f}% utilized. Consider optimizing this space."
            log_suggestion(suggestion)  # could display on dashboard or log for review

        # Step 4: (Optional) Use predictive model to forecast and auto-order
        # For each item, predict next week's demand
        # If predicted demand > current total stock, trigger advance reorder
        for _, item in df.iterrows():
            sku = item["SKU"]
            # Example: simple threshold on Days_of_Cover used instead of actual model here:
            if item["Days_of_Cover"] < 3:
                auto_order(sku, quantity= item["Daily_Sales_Rate"] * 7)  # order one week of supply
                print(f"Auto-reorder placed for {sku}")

        # Sleep until next check (e.g., run every hour or as needed)
        time.sleep(3600)

# The functions send_alert, recommend_reorder, log_suggestion, auto_order 
# would be part of backend services to handle those actions (not shown in this snippet).
