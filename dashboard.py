# dashboard.py - Streamlit app for visualization

import streamlit as st
import pandas as pd

# Load processed data (here we reuse the preprocessing from our module)
from data_ingestion import load_data, preprocess_data
df = preprocess_data(load_data())

# Set page layout
st.set_page_config(page_title="Store Inventory Dashboard", layout="wide")

st.title("🏪 Store Inventory Optimization Dashboard")
st.markdown("This dashboard displays current inventory status, shelf utilization, and AI-driven recommendations for restocking and space optimization.")

# 1. Inventory Levels by Category
st.subheader("Inventory Levels by Category")
inventory_by_cat = df.groupby("Category")["Total_Stock"].sum().reset_index()
# Bar chart of total stock per category
st.bar_chart(data=inventory_by_cat, x="Category", y="Total_Stock", height=300)
st.caption("Total units in stock by category (including on-shelf and backroom).")

# 2. Shelf Space Usage and Suggestions
st.subheader("Shelf Space Utilization by SKU")
# Show a table with SKU, utilization %, and suggestion
shelf_usage = df[["SKU", "Category", "Shelf_Utilization"]].copy()
shelf_usage["Shelf_Utilization"] = shelf_usage["Shelf_Utilization"].apply(lambda x: f"{x:.1f}%")
# Add a suggestion based on utilization
def space_suggestion(util):
    u = float(util.strip('%'))
    if u < 30:
        return "🔻 Underutilized - Consider reducing shelf space or stock"
    elif u > 90:
        return "🔺 Overfilled - Consider adding shelf space or restocking more frequently"
    else:
        return "Optimal"
shelf_usage["Suggestion"] = shelf_usage["Shelf_Utilization"].apply(space_suggestion)
st.dataframe(shelf_usage, width=700)
st.caption("Shelf utilization for each SKU (percentage of allocated shelf filled). Suggestions indicate if shelf space might be reallocated.")

# 3. Stockout Risk Predictions
st.subheader("Stockout Risk Alerts")
high_risk_items = df[df["Stockout_Risk"] == "High"]
if not high_risk_items.empty:
    st.error(f"⚠️ {len(high_risk_items)} SKUs at HIGH risk of stockout soon!")
    # List high-risk items with days of cover
    for _, item in high_risk_items.iterrows():
        st.write(f"- **{item['SKU']}** (Category: {item['Category']}): Only **{item['Days_of_Cover']:.1f} days** of stock left.")
else:
    st.success("No high-risk stockouts expected in the immediate term.")
medium_risk = df[df["Stockout_Risk"] == "Medium"]
if not medium_risk.empty:
    st.warning(f"{len(medium_risk)} SKUs have medium risk (limited stock cover).")

# 4. Replenishment Recommendations
st.subheader("Replenishment Recommendations")
for _, item in high_risk_items.iterrows():
    # Suggest reorder quantity: e.g., enough for 10 days of sales minus current stock
    sku = item["SKU"]
    daily = item["Daily_Sales_Rate"]
    current_total = item["Total_Stock"]
    # For demo, recommend bringing stock to 10 days of cover
    recommended_qty = max(0, int(daily * 10 - current_total))
    if recommended_qty > 0:
        st.write(f"🔄 Reorder **{recommended_qty} units** of **{sku}** (Projected shortfall in {item['Days_of_Cover']:.1f} days)")
# Also consider backroom refill suggestions for items low on shelf but with backroom stock
low_shelf = df[(df["Current_OnShelf"] < df["Shelf_Capacity"] * 0.5) & (df["Backroom_Stock"] > 0)]
for _, item in low_shelf.iterrows():
    st.write(f"🗃️ Move **{item['Backroom_Stock']} units** of **{item['SKU']}** from backroom to shelf (Shelf only {item['Current_OnShelf']}/{item['Shelf_Capacity']} filled)")
