import pandas as pd
import numpy as np

rows = 200

data = {
    "Temperature": np.random.randint(20, 40, rows),
    "Humidity": np.random.randint(50, 95, rows),
    "Pressure": np.random.randint(990, 1020, rows),
    "WindSpeed": np.random.randint(1, 10, rows)
}

df = pd.DataFrame(data)
df["Rainfall"] = (df["Humidity"] * 0.5 + np.random.randint(0, 10, rows)) / 3

df.to_csv("weather.csv", index=False)
print("New Large Dataset Generated!")
