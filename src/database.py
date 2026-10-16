import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///music.db")

query = """
SELECT
    name,
    artists,
    energy,
    CASE
        WHEN energy < 0.4 THEN 'Low'
        WHEN energy <= 0.7 THEN 'Medium'
        ELSE 'High'
    END AS energy_level
FROM songs
LIMIT 20;
"""

df = pd.read_sql(query, engine)

print(df)