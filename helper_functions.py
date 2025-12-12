# helper_functions.py

def send_alert(message):
    print(f"[ALERT] {message}")  # In production, replace with email, SMS, or GUI push

def recommend_reorder(sku, item):
    recommended_qty = int(item["Daily_Sales_Rate"] * 7)
    print(f"[REORDER] Recommend ordering {recommended_qty} units of {sku}")

def log_suggestion(message):
    print(f"[SUGGESTION] {message}")  # Could also log to file or database

def auto_order(sku, quantity):
    print(f"[AUTO-ORDER] Placed order for {quantity} units of {sku}")
