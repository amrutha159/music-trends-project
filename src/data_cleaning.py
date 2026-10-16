import pandas as pd


def load_data():
    df = pd.read_csv("data/data.csv")
    return df


def add_decade(df):
    df["decade"] = (df["year"] // 10) * 10
    return df