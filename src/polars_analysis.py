import polars as pl

df = pl.scan_csv("data/data.csv")

df = df.with_columns(
    ((pl.col("year") // 10) * 10).alias("decade")
)

print(df.head())

avg_duration = (
    df
    .group_by("decade")
    .agg(
        pl.col("duration_ms").mean().alias("avg_duration")
    )
    .sort("decade")
    .collect()
)

print(avg_duration)

avg_loudness = (
    df
    .group_by("decade")
    .agg(
        pl.col("loudness").mean().alias("avg_loudness")
    )
    .sort("decade")
    .collect()
)

print(avg_loudness)

avg_danceability = (
    df
    .group_by("decade")
    .agg(
        pl.col("danceability").mean().alias("avg_danceability")
    )
    .sort("decade")
    .collect()
)

print(avg_danceability)

avg_energy = (
    df
    .group_by("decade")
    .agg(
        pl.col("energy").mean().alias("avg_energy")
    )
    .sort("decade")
    .collect()
)

print(avg_energy)
