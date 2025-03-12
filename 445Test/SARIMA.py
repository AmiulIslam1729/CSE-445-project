import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load dataset
file_path = "C:\\Users\\Lenovo\\Downloads\\project445\\project445\\outlier_removed_encoded.xlsx"
df = pd.read_excel(file_path)

# Ensure 'Year' is datetime and set it as index
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index('Year', inplace=True)

# Splitting data into 80% training and 20% testing
train_size = int(len(df) * 0.8)
train, test = df.iloc[:train_size], df.iloc[train_size:]

# Define target variable (Yield)
y_train, y_test = train['Yield'], test['Yield']

# Train ETS Model
ets_model = ETSModel(y_train, error="add", trend="add", seasonal="add", seasonal_periods=12)
ets_fit = ets_model.fit()

# Predictions
test_pred = ets_fit.predict(start=len(y_train), end=len(y_train) + len(y_test) - 1)

# Model Performance Metrics
mae = mean_absolute_error(y_test, test_pred)
mse = mean_squared_error(y_test, test_pred)
rmse = np.sqrt(mse)

print(f"📊 Model Performance Metrics:")
print(f"✅ Mean Absolute Error (MAE): {mae:.4f}")
print(f"✅ Mean Squared Error (MSE): {mse:.4f}")
print(f"✅ Root Mean Squared Error (RMSE): {rmse:.4f}")

# Plot Actual vs. Predicted
plt.figure(figsize=(10, 5))
plt.plot(test.index, y_test, label="Actual Yield", marker="o")
plt.plot(test.index, test_pred, label="Predicted Yield", linestyle="dashed", marker="x")
plt.xlabel("Year")
plt.ylabel("Yield")
plt.title("ETS Model - Actual vs Predicted Yield")
plt.legend()
plt.show()

# Residuals Plot
residuals = y_test - test_pred
plt.figure(figsize=(10, 5))
plt.plot(test.index, residuals, marker="o", linestyle="dashed")
plt.axhline(y=0, color="r", linestyle="--")
plt.xlabel("Year")
plt.ylabel("Residuals")
plt.title("ETS Model - Residuals Plot")
plt.show()
