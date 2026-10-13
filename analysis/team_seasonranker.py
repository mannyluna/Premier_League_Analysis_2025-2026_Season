import pandas as pd
import numpy as np


class TeamAnalyzer:

    """
    A class to analyze team performance across a season, including cumulative statistics and rankings.
    Expands the fixtures data into a format suitable for cumulative analysis and provides methods to build season tables and rank teams by gameweek.
    """
    def __init__(self, fixtures_df: pd.DataFrame):

        self.fixtures_df = fixtures_df.copy()
        self._team_rows = None
        self._season_table = None
    
    def expand_fixtures(self) -> pd.DataFrame:

        if self._team_rows is not None:
            return self._team_rows
        
        home = self.fixtures_df.rename(columns={
            "home_team_shortname": "team",
            "away_team_shortname": "opponent",
            "home_score": "gf",
            "away_score": "ga",})
        [["team", "opponent", "gf", "ga", "gameweek"]].copy()

        home["is_home"] = True

        away = self.fixtures_df.rename(columns={
            "away_team_shortname": "team",
            "home_team_shortname": "opponent",
            "away_score": "gf",
            "home_score": "ga",})
        [["team", "opponent", "gf", "ga", "gameweek"]].copy()
        
        away["is_home"] = False

        team_rows = pd.concat([home, away],ignore_index=True)

        team_rows["goal_diff"] = (team_rows["gf"]- team_rows["ga"])

        team_rows["points"] = np.select([
            team_rows["goal_diff"] > 0,
            team_rows["goal_diff"] < 0,
            ], [3,0,], default=1,)

        team_rows["result"] = np.select([
            team_rows["goal_diff"] > 0,
            team_rows["goal_diff"] < 0,
            ], ["W","L",], default="D",)

        team_rows = team_rows.sort_values(["team", "gameweek"]).reset_index(drop=True)
        
        self._team_rows = team_rows

        return team_rows

    def _pivot_metric(self,
                    team_rows: pd.DataFrame,
                    column: str,
                    prefix: str,
                    ) -> pd.DataFrame:
        
        pivot = team_rows.pivot(index="team", 
                                columns="match_number",
                                values=column,)
            
        
        pivot.columns = [f"{prefix}_gmwk_{i}" for i in pivot.columns]
        
        return pivot
    
    def build_season_table(self) -> pd.DataFrame:
        
        """
        Produce a DataFrame indexed by team with columns:
        cum_goal_dif_gmwk_1, ..., goals_for_gmwk_1, ..., points_gmwk_1, ...
        """
        # compute cumulative columns per team ordered by gameweek
        if self._season_table is not None:
            return self._season_table

        team_rows = self.expand_fixtures()


        team_groups = team_rows.groupby("team")
        
        team_rows["cum_goal_diff"] = (team_groups["goal_diff"].cumsum())

        team_rows["cum_goals_for"] = (team_groups["gf"].cumsum())

        team_rows["cum_goals_against"] = (team_groups["ga"].cumsum())

        team_rows["cum_points"] = (team_groups["points"].cumsum())

        # create a helper column for gameweek position (1-based)
        # If there are missing gameweeks for a team, this will reflect the actual match order.
        team_rows["match_number"] = team_rows.groupby("team").cumcount() + 1

        season_table = pd.concat(
            [self._pivot_metric(team_rows,
                            "cum_goal_diff",
                            "cum_goal_diff",
                            ),
            self._pivot_metric(team_rows,
                            "cum_goals_for",
                            "goals_for",
                            ),
            self._pivot_metric(team_rows,
                            "cum_goals_against",
                            "goals_against",
                            ),
            self._pivot_metric(team_rows,
                            "cum_points",
                            "points",
                            ),], axis=1,)
        
        season_table = (season_table.fillna(0).astype(int).reset_index())
        
        self._season_table = season_table
        
        return season_table

    

    def _rank_for_gameweek(self, 
                          season_table: pd.DataFrame, 
                          week: int) -> pd.DataFrame:
        """
        Add a column 'gmwk_{week}_rank' to season_df ranking teams by:
        points_gmwk_{week}, cum_goal_dif_gmwk_{week}, goals_for_gmwk_{week}
        Ties broken alphabetically by team name.
        """
        pts_col = f"points_gmwk_{week}"
        gd_col = f"cum_goal_diff_gmwk_{week}"
        gf_col = f"goals_for_gmwk_{week}"
        rank_col = f"gmwk_{week}_rank"

        # If some teams don't have that gameweek (NaN), treat as 0
        df_season = season_table.copy()
        for col in (pts_col, gd_col, gf_col):
            if col not in df_season.columns:
                df_season[col] = 0

        # sort by keys (descending for numeric metrics, ascending for team name)
        df_season = df_season.sort_values([pts_col, gd_col, gf_col, "team"], ascending=[False, False, False, True])

        # assign dense ranks based on the sorted order
        df_season[rank_col] = pd.Series(range(1, len(df_season) + 1), index=df_season.index)

        # return to original index order (optional)
        df_season = df_season.sort_index()

        return df_season        
    
    def rank_all_gameweeks(self)-> pd.DataFrame:

        season_table = self.build_season_table()

        weeks = len([c for c in season_table.columns if c.startswith("points_gmwk_")])

        for week in range(1, weeks + 1):
            season_table = self._rank_for_gameweek(season_table, week)

        return season_table
