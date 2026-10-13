from pathlib import Path
from typing import Any
import pandas as pd
import glob

from config import EPL_DATA


class SoccerDataLoader:
    """
    A class to load all soccer-related datasets for the project.
    Including players, teams, transfers, fixtures, and player match statistics.
    
    """

    @staticmethod
    def load_players() -> pd.DataFrame:
        return pd.read_csv(EPL_DATA / "players.csv")

    @staticmethod
    def load_teams() -> pd.DataFrame:
        return pd.read_csv(EPL_DATA / "teams.csv")

    @staticmethod
    def load_transfers() -> pd.DataFrame:
        return pd.read_csv(EPL_DATA / "transfers.csv")

    @staticmethod
    def load_multiple_files(pattern: str) -> pd.DataFrame:
        """
        Example:
        pattern = "fixtures*.csv"
        """

        files = glob.glob(str(EPL_DATA / pattern))

        if not files:
            raise FileNotFoundError(
                f"No files found matching: {pattern}"
            )

        dfs = []

        for file in files:
            df = pd.read_csv(file)

            if "gameweek" not in df.columns:
                try:
                    gameweek = (int(Path(file).stem[-2:]))
                    df["gameweek"] = gameweek
                except ValueError:
                    pass

            dfs.append(df)

        return pd.concat(dfs, ignore_index=True)

    def load_all(self) -> dict[str, pd.DataFrame]:
        return {
            "players": self.load_players(),
            "teams": self.load_teams(),
            "transfers": self.load_transfers(),
            "fixtures": self.load_multiple_files("fixtures*.csv"),
            "player_gameweek": self.load_multiple_files(
                "player_gameweek*.csv"
            ),
            "player_match": self.load_multiple_files(
                "playermatch*.csv"
            ),
        }