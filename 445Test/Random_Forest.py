import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import seaborn as sns

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

# Initialize and train the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
rf_model.fit(X_train, y_train)

# Predictions on test data
test_pred = rf_model.predict(X_test)

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
plt.plot(test.index, y_test, label='Actual Yield', marker='o')
plt.plot(test.index, test_pred, label='Predicted Yield', linestyle='dashed', marker='x')
plt.xlabel('Year')
plt.ylabel('Yield')
plt.title('Actual vs Predicted Yield - Random Forest Model')
plt.legend()
plt.show()

# Feature Importance Plot
plt.figure(figsize=(10, 5))
feature_importances = pd.Series(rf_model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
sns.barplot(x=feature_importances[:10], y=feature_importances.index[:10], palette="viridis")
plt.xlabel('Importance Score')
plt.ylabel('Feature')
plt.title('Top 10 Feature Importance - Random Forest')
plt.show()
