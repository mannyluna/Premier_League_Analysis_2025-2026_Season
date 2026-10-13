import re
import unicodedata
import pandas as pd
import numpy as np

"""
Utility functions to clean player and transfer data.
Removes special characters and normalizes player names.
"""

def clean_name(name: str | None) -> str:

    if pd.isna(name):
        return "Unknown"

    normalized = unicodedata.normalize(
        "NFKD",
        str(name),
    )

    cleaned = (
        normalized
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    cleaned = re.sub(r"[^A-Za-z\s]", "", cleaned)

    return cleaned.strip()


def clean_players(players_df: pd.DataFrame) -> pd.DataFrame:

    df = players_df.copy()

    df["clean_first_name"] = (df["first_name"].apply(clean_name))

    df["clean_last_name"] = (df["second_name"].apply(clean_name))

    df["clean_web_name"] = (df["web_name"].apply(clean_name))

    df["clean_alt_name"] = (df["alt_name"].apply(clean_name))
   

    return df


def clean_transfers(transfers_df: pd.DataFrame) -> pd.DataFrame:

    df = transfers_df.copy()

    df["Player"] = (df["Player"].apply(clean_name))
    df["Moving From"] = (df["Moving From"].apply(clean_name))
    df["Moving to"] = (df["Moving to"].apply(clean_name))

    return df


def player_transfer(player_match_df: pd.DataFrame, transfers_df: pd.DataFrame):

    for i, row in transfers_df.iterrows():
        first_name = row['First_Name']
        last_name = row['Last_Name']
        team_before = row['Moving From']
        trade_deadline = row['gameweek']

        player_match_df['team'] = np.where((player_match_df['clean_first_name'] == first_name) & (player_match_df['clean_last_name'] == last_name) & (player_match_df['gameweek']  < trade_deadline), team_before, player_match_df['team'])

    return player_match_df


def get_full_name(row: pd.Series) -> str:

    first = (row.get('clean_first_name') or '').strip()
    last  = (row.get('clean_last_name') or '').strip()
    short_lst_name = (row.get('clean_alt_name') or '').strip()

    
    parts = [p for p in (first, last) if p]

    name = ' '.join(parts) if parts else 'Unknown Player'

    if len(name) > 20: 
        parts = [p for p in (first, short_lst_name) if p]
        name = ' '.join(parts) if parts else 'Unknown Player'

    return name