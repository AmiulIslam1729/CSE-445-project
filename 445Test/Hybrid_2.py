import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load dataset
df = pd.read_excel("C:\\Users\\Lenovo\\Downloads\\project445\\project445\\outlier_removed_encoded.xlsx")

# Convert 'Year' to datetime
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index('Year', inplace=True)

# Define features and target
target = 'Yield'
features = df.columns[df.columns != target]

# Train-test split (80-20)
train_size = int(len(df) * 0.8)
train, test = df.iloc[:train_size], df.iloc[train_size:]

X_train, X_test = train[features], test[features]
y_train, y_test = train[target], test[target]

# Scaling Data
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

y_train = y_train.values.reshape(-1, 1)
y_test = y_test.values.reshape(-1, 1)
y_scaler = MinMaxScaler()
y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled = y_scaler.transform(y_test)

# Reshape input for LSTM (samples, time steps, features)
X_train_lstm = X_train_scaled.reshape((X_train_scaled.shape[0], 1, X_train_scaled.shape[1]))
X_test_lstm = X_test_scaled.reshape((X_test_scaled.shape[0], 1, X_test_scaled.shape[1]))

# Build LSTM Model
lstm_model = Sequential([
    LSTM(50, activation='relu', return_sequences=True, input_shape=(1, X_train.shape[1])),
    Dropout(0.2),
    LSTM(50, activation='relu'),
    Dense(1)
])

lstm_model.compile(optimizer='adam', loss='mse')
lstm_model.fit(X_train_lstm, y_train_scaled, epochs=50, batch_size=16, verbose=1)

# Predict with LSTM
lstm_pred_scaled = lstm_model.predict(X_test_lstm)
lstm_pred = y_scaler.inverse_transform(lstm_pred_scaled)

# Train XGBoost Model
xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
xgb_model.fit(X_train, y_train.ravel())

# Predict with XGBoost
xgb_pred = xgb_model.predict(X_test)

# Combine Predictions (Averaging)
hybrid_pred = (lstm_pred.flatten() + xgb_pred) / 2

# Model Performance Metrics
mae = mean_absolute_error(y_test, hybrid_pred)
mse = mean_squared_error(y_test, hybrid_pred)
rmse = np.sqrt(mse)

print(f"Hybrid (LSTM + XGBoost) Performance:")
print(f"✅ MAE: {mae:.4f}")
print(f"✅ MSE: {mse:.4f}")
print(f"✅ RMSE: {rmse:.4f}")

# Plot Predictions
plt.figure(figsize=(10, 5))
plt.plot(test.index, y_test, label='Actual Yield', marker='o')
plt.plot(test.index, hybrid_pred, label='Hybrid Predicted Yield', linestyle='dashed', marker='x')
plt.xlabel('Year')
plt.ylabel('Yield')
plt.title('Actual vs Hybrid Predicted Yield')
plt.legend()
plt.show()
