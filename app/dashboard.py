
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.title("The Evolution of Music")
st.write("Explore how musical characteristics have changed across different decades.")

# Load the music dataset
engine = create_engine("sqlite:///music.db")
df = pd.read_sql("SELECT * FROM songs", engine)

# Choose a year range
year_range = st.slider(
    "Choose a year range:",
    min_value=int(df["year"].min()),
    max_value=int(df["year"].max()),
    value=(1921, 2020)
)

df_filtered = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
].copy()

df_filtered["decade"] = (df_filtered["year"] // 10) * 10

# Count songs in the selected year range using SQL
count_query = """
SELECT COUNT(*) AS song_count
FROM songs
WHERE year >= ? AND year <= ?;
"""

song_count = pd.read_sql(
    count_query,
    engine,
    params=(year_range[0], year_range[1])
)

st.write("Songs in selected range:", song_count["song_count"].iloc[0])

# Chart 1: Number of songs by decade
count_by_decade_query = """
SELECT
    (year / 10) * 10 AS decade,
    COUNT(*) AS song_count
FROM songs
WHERE year >= ? AND year <= ?
GROUP BY decade
ORDER BY decade;
"""

song_counts = pd.read_sql(
    count_by_decade_query,
    engine,
    params=(year_range[0], year_range[1])
)

fig_counts = px.bar(
    song_counts,
    x="decade",
    y="song_count",
    title="Number of Songs by Decade",
    labels={
        "decade": "Decade",
        "song_count": "Number of Songs"
    },
    hover_data={
        "decade": True,
        "song_count": True
    }
)

st.plotly_chart(fig_counts)

# Choose a music feature to explore
metric_options = {
    "Danceability": "danceability",
    "Energy": "energy",
    "Loudness": "loudness",
    "Song Duration": "duration_ms / 60000"
}

metric_units = {
    "Danceability": "",
    "Energy": "",
    "Loudness": "dB",
    "Song Duration": "minutes"
}

selected_metric = st.selectbox(
    "Choose a music feature:",
    list(metric_options.keys()),
    key="main_music_feature"
)

metric = metric_options[selected_metric]

if metric_units[selected_metric]:
    y_label = f"Average {selected_metric} ({metric_units[selected_metric]})"
else:
    y_label = f"Average {selected_metric}"

# Calculate the selected feature's average by decade using SQL
query = f"""
SELECT
    (year / 10) * 10 AS decade,
    AVG({metric}) AS avg_value
FROM songs
WHERE year >= ? AND year <= ?
GROUP BY decade
ORDER BY decade;
"""

trend = pd.read_sql(
    query,
    engine,
    params=(year_range[0], year_range[1])
)

# Summary cards: highest and lowest averages
highest = trend.loc[trend["avg_value"].idxmax()]
lowest = trend.loc[trend["avg_value"].idxmin()]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Highest Average",
        f"{highest['avg_value']:.2f} {metric_units[selected_metric]}"
    )
    st.write(f"Decade: {int(highest['decade'])}s")

with col2:
    st.metric(
        "Lowest Average",
        f"{lowest['avg_value']:.2f} {metric_units[selected_metric]}"
    )
    st.write(f"Decade: {int(lowest['decade'])}s")

# Chart 2: Average selected feature by decade
fig = px.line(
    trend,
    x="decade",
    y="avg_value",
    markers=True,
    title=f"Average {selected_metric} by Decade",
    labels={
        "decade": "Decade",
        "avg_value": y_label
    },
    hover_data={
        "decade": True,
        "avg_value": ":.2f"
    }
)

st.plotly_chart(fig)

# Choose features for the scatter plot
x_metric_name = st.selectbox(
    "Choose the X-axis feature:",
    list(metric_options.keys()),
    index=1
)

y_metric_name = st.selectbox(
    "Choose the Y-axis feature:",
    list(metric_options.keys()),
    index=0
)

# Map dropdown labels to dataframe columns
column_options = {
    "Danceability": "danceability",
    "Energy": "energy",
    "Loudness": "loudness",
    "Song Duration": "duration_minutes"
}

df_filtered["duration_minutes"] = df_filtered["duration_ms"] / 60000

x_metric = column_options[x_metric_name]
y_metric = column_options[y_metric_name]

# Calculate average selected features by decade
relationship = (
    df_filtered.groupby("decade")[[x_metric, y_metric]]
    .mean()
    .reset_index()
)

# Calculate correlation
if x_metric == y_metric:
    correlation = 1.0
else:
    correlation = relationship[x_metric].corr(relationship[y_metric])

st.write(f"Correlation between selected features: {correlation:.2f}")

# Chart 3: Scatter plot comparing two features
fig_relationship = px.scatter(
    relationship,
    x=x_metric,
    y=y_metric,
    hover_data=["decade"],
    title=f"Average {x_metric_name} vs. {y_metric_name} by Decade",
    labels={
        x_metric: f"Average {x_metric_name}",
        y_metric: f"Average {y_metric_name}"
    }
)

st.plotly_chart(fig_relationship)
