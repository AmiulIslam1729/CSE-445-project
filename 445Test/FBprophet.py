import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load dataset
file_path = "C:\\Users\\Lenovo\\Downloads\\project445\\project445\\outlier_removed_encoded.xlsx"
df = pd.read_excel(file_path)

# Ensure 'Year' is datetime
df['Year'] = pd.to_datetime(df['Year'], format='%Y')

# Rename columns for Prophet (it requires 'ds' for date & 'y' for target)
df = df.rename(columns={"Year": "ds", "Yield": "y"})

# Splitting data into 80% training and 20% testing
train_size = int(len(df) * 0.8)
train, test = df.iloc[:train_size], df.iloc[train_size:]

# Initialize and train FBProphet model
prophet_model = Prophet()
prophet_model.fit(train)

# Create future dataframe for prediction
future = test[['ds']]  # Prophet requires a dataframe with 'ds' column only
forecast = prophet_model.predict(future)

# Extract predicted values
test_pred = forecast['yhat'].values

# Model Performance Metrics
mae = mean_absolute_error(test['y'], test_pred)
mse = mean_squared_error(test['y'], test_pred)
rmse = np.sqrt(mse)

print(f"📊 Model Performance Metrics:")
print(f"✅ Mean Absolute Error (MAE): {mae:.4f}")
print(f"✅ Mean Squared Error (MSE): {mse:.4f}")
print(f"✅ Root Mean Squared Error (RMSE): {rmse:.4f}")

# Plot Actual vs. Predicted
plt.figure(figsize=(10, 5))
plt.plot(test['ds'], test['y'], label="Actual Yield", marker="o")
plt.plot(test['ds'], test_pred, label="Predicted Yield", linestyle="dashed", marker="x")
plt.xlabel("Year")
plt.ylabel("Yield")
plt.title("FBProphet Model - Actual vs Predicted Yield")
plt.legend()
plt.show()

# Prophet's built-in visualization
prophet_model.plot(forecast)
plt.title("FBProphet Forecast")
plt.show()
