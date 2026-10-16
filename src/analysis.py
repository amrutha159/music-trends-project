import matplotlib.pyplot as plt

from data_cleaning import load_data, add_decade


df = load_data()
df = add_decade(df)


def calculate_average_duration(df):
    avg_duration = df.groupby("decade")["duration_ms"].mean()
    avg_duration_minutes = avg_duration / 60000
    return avg_duration_minutes


def calculate_average_loudness(df):
    return df.groupby("decade")["loudness"].mean()


def calculate_average_danceability(df):
    return df.groupby("decade")["danceability"].mean()


def calculate_average_energy(df):
    return df.groupby("decade")["energy"].mean()


avg_duration = calculate_average_duration(df)
avg_loudness = calculate_average_loudness(df)
avg_danceability = calculate_average_danceability(df)
avg_energy = calculate_average_energy(df)


print("Average song duration:")
print(avg_duration)

print("Average loudness:")
print(avg_loudness)

print("Average danceability:")
print(avg_danceability)

print("Average energy:")
print(avg_energy)


