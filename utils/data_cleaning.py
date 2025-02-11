import pandas as pd


def row_nans_clean(df):
    if df.isna().values.any():
        print(df.isnull().sum())
        df = df.dropna()
    return df
#
def rating_check(df):
    invalid_ratings = df[(df["rating"] < 1) | (df["rating"] > 5)]
    df = df.drop(index=invalid_ratings.index)
    return df

def review_check(df):
    empty_reviews = df[df["review"].str.strip() == ""]
    df = df.drop(index=empty_reviews.index)
    return df

def data_cleaning(df):
     df = row_nans_clean(df)
     df = rating_check(df)
     df = review_check(df)
     return df


