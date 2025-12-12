# models.py - Module for AI models (forecasting, optimization)

import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Dummy training data: last 4 weeks sales of a product and some related features (e.g., price, promo)
X_train = np.array([
    [100, 10.0, 0],   # Week1: sold 100 units, price $10, no promo
    [120, 10.0, 1],   # Week2: sold 120 units, price $10, promo active
    [90,  12.0, 0],   # Week3: sold 90 units, price $12, no promo
    [130, 12.0, 1],   # Week4: sold 130 units, price $12, promo active
])
y_train = np.array([120, 90, 130, 110])  # Week5 actual sales (for training target)

# Train a simple regression model to forecast Week5 sales from Weeks1-4 features
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Now, simulate current week (Week5) features to predict Week6 sales
current_week_features = np.array([[110, 11.0, 0]])  # Week5: sold 110, price $11, no promo
predicted_sales_week6 = model.predict(current_week_features)
print(f"Predicted sales for next week: {predicted_sales_week6[0]:.0f} units")
