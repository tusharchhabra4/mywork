import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data = pd.read_csv("weather.csv")

data["Rain"] = data["Rainfall"].apply(lambda x: 1 if x > 0 else 0)

X = data[['Temperature', 'Humidity', 'Pressure', 'WindSpeed']]
y = data['Rain']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Weather Prediction Accuracy:", accuracy)

print("\nEnter Weather Details:")
temp = float(input("Temperature: "))
humidity = float(input("Humidity: "))
pressure = float(input("Pressure: "))
wind = float(input("Wind Speed: "))

user_data = pd.DataFrame(
    [[temp, humidity, pressure, wind]],
    columns=['Temperature', 'Humidity', 'Pressure', 'WindSpeed']
)

result = model.predict(user_data)

if result[0] == 1:
    print("\n🌧 Weather Prediction: RAIN")
else:
    print("\n☀ Weather Prediction: NO RAIN")
