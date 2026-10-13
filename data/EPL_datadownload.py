from pathlib import Path
import pandas as pd


BASE_URL = (
    "https://raw.githubusercontent.com/"
    "olbauday/FPL-Core-Insights/main/"
    "data/2025-2026/By%20Tournament/"
    "Premier%20League"
)

"""
Utility functions to download Premier League match data for a given season.
Downloads player match statistics and fixture data for each gameweek.
"""

def download_match_data(save_dir: Path) -> None:

    save_dir.mkdir(parents=True, exist_ok=True)

    for gw in range(1, 39):

        try:

            player_url = (
                f"{BASE_URL}/GW{gw}/playermatchstats.csv"
            )

            fixture_url = (
                f"{BASE_URL}/GW{gw}/fixtures.csv"
            )

            player_df = pd.read_csv(player_url)
            fixture_df = pd.read_csv(fixture_url)

            gw_str = f"{gw:02d}"

            player_df.to_csv(
                save_dir / f"playermatchstats_gw{gw_str}.csv",
                index=False
            )

            fixture_df.to_csv(
                save_dir / f"fixtures_gw{gw_str}.csv",
                index=False
            )

            print(f"Downloaded GW{gw_str}")

        except Exception as e:

            print(
                f"Failed GW{gw}: {e}"
            )