import pandas as pd

def preprocess():
    df = pd.read_csv("athlete_events.csv.zip")
    region_df = pd.read_csv("noc_regions.csv")

    # Filter for Summer Olympics only
    df = df[df['Season'] == "Summer"]

    # Merge region data to get the 'region' column
    df = df.merge(region_df, on='NOC', how='left')

    # Drop exact duplicate rows
    df.drop_duplicates(inplace=True)

    # ❌ Don't add Gold/Silver/Bronze columns here — handled in helper.py
    return df
