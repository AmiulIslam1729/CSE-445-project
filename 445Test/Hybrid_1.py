import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_excel("C:\\Users\\Lenovo\\Downloads\\project445\\project445\\outlier_removed_encoded.xlsx")

# Ensure 'Year' is datetime and set as index
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index('Year', inplace=True)

# Splitting data into training (80%) and testing (20%)
train_size = int(len(df) * 0.8)
train, test = df.iloc[:train_size], df.iloc[train_size:]

# Define target variable and features
y_train, y_test = train['Yield'], test['Yield']
X_train, X_test = train.drop(columns=['Yield']), test.drop(columns=['Yield'])

# Train XGBoost model
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=5)
xgb_model.fit(X_train, y_train)

# XGBoost predictions
xgb_pred = xgb_model.predict(X_test)

# Compute residuals
residuals_train = y_train - xgb_model.predict(X_train)
residuals_test = y_test - xgb_pred

# Train SARIMA model on residuals
sarima_model = SARIMAX(residuals_train, order=(1,1,1), seasonal_order=(1,1,1,12))
sarima_fit = sarima_model.fit()

# Predict residuals for test set
sarima_residual_pred = sarima_fit.predict(start=len(residuals_train), end=len(residuals_train) + len(residuals_test) - 1)

# Final hybrid prediction
final_pred = xgb_pred + sarima_residual_pred

# Model Performance Metrics
mae = mean_absolute_error(y_test, final_pred)
mse = mean_squared_error(y_test, final_pred)
rmse = np.sqrt(mse)

print(f"\n\U0001F4CA Hybrid (XGBoost + SARIMA) Performance:")
print(f"✅ MAE: {mae:.4f}")
print(f"✅ MSE: {mse:.4f}")
print(f"✅ RMSE: {rmse:.4f}\n")

# Plot Actual vs Predicted
tl = len(y_test)
plt.figure(figsize=(10, 5))
plt.plot(y_test.index, y_test, label='Actual Yield', marker='o')
plt.plot(y_test.index, final_pred, label='Hybrid Prediction', linestyle='dashed', marker='x')
plt.xlabel('Year')
plt.ylabel('Yield')
plt.title('Hybrid (XGBoost + SARIMA) Model: Actual vs Predicted Yield')
plt.legend()
plt.show()

# Residuals Plot
plt.figure(figsize=(10, 5))
plt.plot(y_test.index, residuals_test, marker='o', linestyle='dashed')
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Year')
plt.ylabel('Residuals')
plt.title('Residuals Plot')
plt.show()
