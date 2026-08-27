import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# Load Dataset
data = pd.read_csv("weather.csv")

X = data[['Temperature', 'Humidity', 'Pressure', 'WindSpeed']]
y = data['Rainfall']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model Accuracy (R² Score):", r2)
print("Mean Absolute Error:", mae)

# ----------- USER INPUT -----------

print("\nEnter Weather Details:")
temp = float(input("Temperature: "))
humidity = float(input("Humidity: "))
pressure = float(input("Pressure: "))
wind = float(input("Wind Speed: "))

user_data = pd.DataFrame(
    [[temp, humidity, pressure, wind]],
    columns=['Temperature', 'Humidity', 'Pressure', 'WindSpeed']
)

predicted_rainfall = model.predict(user_data)
print("\nPredicted Rainfall (mm):", round(predicted_rainfall[0], 2))

# ----------- MERGED ACTUAL vs PREDICTED PLOT -----------

plt.figure(figsize=(8, 5))

plt.plot(y_test.values, marker='o', label="Actual Rainfall")
plt.plot(y_pred, marker='s', label="Predicted Rainfall")

plt.xlabel("Test Data Index")
plt.ylabel("Rainfall (mm)")
plt.title("Actual vs Predicted Rainfall Comparison")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("actual_vs_predicted_rainfall.png", dpi=300)
plt.show()
