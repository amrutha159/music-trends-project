import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/data.csv")

# Create decade
df["decade"] = (df["year"] // 10) * 10

# Average duration
avg_duration = df.groupby("decade")["duration_ms"].mean()

# Convert milliseconds to minutes
avg_duration_minutes = avg_duration / 60000

avg_loudness = df.groupby("decade")["loudness"].mean()

avg_danceability = df.groupby("decade")["danceability"].mean()

avg_energy = df.groupby("decade")["energy"].mean()

print(avg_energy)
plt.plot(avg_energy.index, avg_energy.values)

plt.xlabel("Decade")
plt.ylabel("Average Energy")
plt.title("Average Music Energy by Decade")

plt.show()

