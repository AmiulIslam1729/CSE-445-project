import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

# Target variable (Yield)
y_train, y_test = train['Yield'], test['Yield']

# Train the EWMA model (choosing alpha=0.3 for moderate smoothing)
alpha = 0.3
ewma_model = y_train.ewm(span=int(1/alpha), adjust=False).mean()

# Make predictions for the test period
test_pred = ewma_model.iloc[-1]  # Using last trained EWMA value as forecast for all future values
test_pred = np.full(len(y_test), test_pred)  # Repeat the same predicted value for the entire test set

# Model Performance Metrics
mae = mean_absolute_error(y_test, test_pred)
mse = mean_squared_error(y_test, test_pred)
rmse = np.sqrt(mse)

print(f"📊 Model Performance Metrics:")
print(f"✅ Mean Absolute Error (MAE): {mae:.4f}")
print(f"✅ Mean Squared Error (MSE): {mse:.4f}")
print(f"✅ Root Mean Squared Error (RMSE): {rmse:.4f}")

# Plot Actual vs Predicted
plt.figure(figsize=(10, 5))
plt.plot(test.index, y_test, label='Actual Yield', marker='o')
plt.plot(test.index, test_pred, label='Predicted Yield (EWMA)', linestyle='dashed', marker='x')
plt.xlabel('Year')
plt.ylabel('Yield')
plt.title('Actual vs Predicted Yield - EWMA Model')
plt.legend()
plt.show()

# Residuals Plot
residuals = y_test - test_pred
plt.figure(figsize=(10, 5))
plt.plot(test.index, residuals, marker='o', linestyle='dashed')
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Year')
plt.ylabel('Residuals')
plt.title('Residuals Plot - EWMA Model')
plt.show()
