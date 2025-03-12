import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

# Load dataset
file_path = "C:\\Users\\Lenovo\\Downloads\\project445\\project445\\outlier_removed_encoded.xlsx"
df = pd.read_excel(file_path)

# Ensure 'Year' is in datetime format and set it as the index
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index('Year', inplace=True)

# Splitting data into 80% training and 20% testing
train_size = int(len(df) * 0.8)
train, test = df.iloc[:train_size], df.iloc[train_size:]

# Define target variable (Yield) and features (other columns)
y_train, y_test = train['Yield'], test['Yield']
X_train, X_test = train.drop(columns=['Yield']), test.drop(columns=['Yield'])

# Initialize and train the CatBoost model
cat_model = CatBoostRegressor(iterations=1000, learning_rate=0.1, depth=6, loss_function='RMSE', verbose=200)
cat_model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=100)

# Predictions on test data
test_pred = cat_model.predict(X_test)

# Model Performance Metrics
mae = mean_absolute_error(y_test, test_pred)
mse = mean_squared_error(y_test, test_pred)
rmse = np.sqrt(mse)

print(f"\U0001F4CA Model Performance Metrics:")
print(f"✅ Mean Absolute Error (MAE): {mae:.4f}")
print(f"✅ Mean Squared Error (MSE): {mse:.4f}")
print(f"✅ Root Mean Squared Error (RMSE): {rmse:.4f}")

# Plot Actual vs. Predicted
plt.figure(figsize=(10, 5))
plt.plot(test.index, y_test, label='Actual Yield', marker='o')
plt.plot(test.index, test_pred, label='Predicted Yield', linestyle='dashed', marker='x')
plt.xlabel('Year')
plt.ylabel('Yield')
plt.title('Actual vs Predicted Yield - CatBoost Model')
plt.legend()
plt.show()

# Feature Importance Plot
plt.figure(figsize=(10, 5))
feature_importance = cat_model.get_feature_importance()
feature_names = X_train.columns
plt.barh(feature_names, feature_importance)
plt.xlabel("Feature Importance Score")
plt.title("Feature Importance in CatBoost Model")
plt.show()