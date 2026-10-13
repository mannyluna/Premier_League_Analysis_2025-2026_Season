import pandas as pd
import numpy as np


class TeamStatistics:

    """
    A class to analyze team statistics, including offensive and defensive metrics.
    Expands the fixtures data into a team perspective and provides methods to build offensive and defensive dataframes.
    """
    def __init__(self, fixtures_df: pd.DataFrame):
        self.fixtures_df = fixtures_df.copy()

        self._offensive_df = None
        self._defensive_df = None

    def expand_team_data(self,
                        params: dict,
                    ) -> pd.DataFrame:
        """
        Convert home/away fixture data into
        a team perspective dataframe.
        """

        home_columns = params["home"]
        away_columns = params["away"]

        update_home = {
            col: col.replace("home_", "")
            if col.startswith("home_")
            else col.replace("away_", "opp_")
            for col in home_columns
        }

        update_away = {
            col: col.replace("away_", "")
            if col.startswith("away_")
            else col.replace("home_", "opp_")
            for col in away_columns
        }

        home_df =( self.fixtures_df[home_columns]
                    .rename(columns=update_home)
                    .assign(is_home=True))

        away_df =( self.fixtures_df[away_columns]
                .rename(columns=update_away)
                .assign(is_home=False))
        

        team_df = pd.concat([home_df, away_df], ignore_index=True,)

        return (
            team_df.sort_values(["team_shortname", "gameweek"])
            .reset_index(drop=True))

    def build_offensive_data(self) -> pd.DataFrame:

        params = {
            "home": [
                "home_team_shortname",
                "away_team_shortname",
                "gameweek",
                "home_expected_goals_xg",
                "away_expected_goals_xg",
                "home_total_shots",
                "home_shots_on_target",
                "home_shots_inside_box",
                "home_non_penalty_xg",
                "home_xg_on_target_xgot",
                "home_score",
                "away_score",
            ],
            "away": [
                "home_team_shortname",
                "away_team_shortname",
                "gameweek",
                "away_expected_goals_xg",
                "home_expected_goals_xg",
                "away_total_shots",
                "away_shots_on_target",
                "away_shots_inside_box",
                "away_non_penalty_xg",
                "away_xg_on_target_xgot",
                "away_score",
                "home_score",
            ],
        }

        self._offensive_df = self.expand_team_data(params)

        return self._offensive_df

    def build_defensive_data(self) -> pd.DataFrame:

        params = {
            "home": [
                "home_team_shortname",
                "away_team_shortname",
                "gameweek",
                "home_clearances",
                "home_blocks",
                "home_interceptions",
                "home_tackles_won",
                "home_possession",
            ],
            "away": [
                "home_team_shortname",
                "away_team_shortname",
                "gameweek",
                "away_clearances",
                "away_blocks",
                "away_interceptions",
                "away_tackles_won",
                "away_possession",
            ],
        }

        self._defensive_df = self.expand_team_data(params)

        return self._defensive_df

    def team_scoring_data(self, team: str,) -> dict[str, float]:

        if self._offensive_df is None:
            self.build_offensive_data()

        team_df = self._offensive_df[self._offensive_df["team_shortname"] == team]

        total_matches = len(team_df)

        if total_matches == 0:
            return {}

        shots = team_df["total_shots"].sum()
        goals = team_df["score"].sum()
        sot = team_df["shots_on_target"].sum()

        shots_per_match = round(shots / total_matches,1,)
        goals_per_match = round(goals / total_matches,1,)
        sot_pct = int(round((sot / shots) * 100)) if shots else 0

        xg = round(team_df["expected_goals_xg"].sum()/ total_matches,2,)

        npxg = round(team_df["non_penalty_xg"].sum()/ total_matches, 2,)

        xgot = round(team_df["xg_on_target_xgot"].sum()/ total_matches,2,)

        shots_inside = team_df["shots_inside_box"].sum()

        shots_inside_pct = int(round((shots_inside / shots) * 100)) if shots else 0

        return {
            "Shots": shots_per_match,
            "Goals": goals_per_match,
            "SoT%": sot_pct,
            "xG": xg,
            "npxG": npxg,
            "xGOT": xgot,
            "Shots Inside the Box %": shots_inside_pct,
            "Shots Outside the Box %": round(
                100 - shots_inside_pct,1,)}

    def team_defensive_data(self,
                            team: str,
                            ) -> dict[str, float]:

        if self._defensive_df is None:
            self.build_defensive_data()

        team_df = self._defensive_df[self._defensive_df["team_shortname"] == team]
        matches = len(team_df)

        if matches == 0:
            return {}

        return {
            "Clearances": round(team_df["clearances"].sum()/ matches, 2,),
            "Blocks": round(team_df["blocks"].sum()/ matches, 2,),
            "Interceptions": round(team_df["interceptions"].sum()/ matches, 2,),
            "Tackles": round(team_df["tackles_won"].sum()/ matches, 2,),
            "Possession": round(team_df["possession"].mean(), 2,),
            }


    def get_team_summary(self,
                        team: str,
                        ) -> dict:

        attack = self.team_scoring_data(team)

        defense = self.team_defensive_data(team)

        return {"team": team,
                **attack,
                **defense}
    

    def offensive_rankings(self) -> pd.DataFrame:

        if self._offensive_df is None:
            self.build_offensive_data()

        summary = []

        for team in sorted(self._offensive_df["team_shortname"].unique()):

            attack = self.team_scoring_data(team)

            summary.append({
                    "team": team,
                    "goals_per_match": attack["goals_per_match"],
                    "sot_pct": attack["sot_pct"],
                    "xg_per_match": attack["xg_per_match"],
                    "xgot_per_match": attack["xgot_per_match"],}
            )

        df_rank = pd.DataFrame(summary)

        df_rank["goals_pct"] = (df_rank["goals_per_match"].rank(pct=True).mul(100))
        df_rank["sot_pct_rank"] = (df_rank["sot_pct"].rank(pct=True).mul(100))
        df_rank["xg_pct"] = (df_rank["xg_per_match"].rank(pct=True).mul(100))
        df_rank["xgot_pct"] = (df_rank["xgot_per_match"].rank(pct=True).mul(100))

        df_rank["offensive_rating"] = (df_rank[[
                    "goals_pct",
                    "sot_pct_rank",
                    "xg_pct",
                    "xgot_pct",]].mean(axis=1).round(1))

        df_rank["offensive_rank"] = (df_rank["offensive_rating"]
                                .rank(ascending=False, method="min")
                                .astype(int)
                                )

        return df_rank.sort_values("offensive_rank")
    
    