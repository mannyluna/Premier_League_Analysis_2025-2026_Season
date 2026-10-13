

import numpy as np
import pandas as pd


class PlayerAnalyzer:

    def __init__(self, player_match_names: pd.DataFrame, max_gameweek: int):

        self.player_match_df = player_match_names.copy()
        self.max_gameweek = max_gameweek
        
        self.player_team_map = (
            self.player_match_df.sort_values("gameweek")
            .groupby("Full_Name")["team"]
            .last().to_dict()
            )

    def get_team(
            self,
            full_name: str) -> str:
        """
        Get player's latest team.
        """
        try:
            return self.player_team_map[full_name]
        
        except KeyError:
            raise ValueError(f"Player not found: {full_name}")

    
    def players_with_multiple_teams(self) -> list[str]:

        grouped = (self.player_match_df.groupby("Full_Name", observed=True)["team"].nunique())

        return (grouped[grouped > 1].index.tolist())


    def get_season_perc(self,
                        percent_cols: list[str]) -> pd.DataFrame:

        """
        Get the season percentage for the specified columns.
        This method calculates the season percentage based on specificed percentages for each match. 
        Converts daily match percentages into season-long percentages.

        """

        # Base columns are the columns without the "_percent" suffix. 
        # (ie: "goals" is a base column, "goals_percent" is the corresponding percentage column and is based on the match value)

        base_cols = [col.replace("_percent", "") for col in percent_cols]
        total_labels = []

        df_temp = self.player_match_df[["Full_Name"] + base_cols + percent_cols].copy()

        for col, percent_col in zip(base_cols, percent_cols):

            # Calculate the total label for the current base column and its corresponding percentage column.
            # Returns the total number of occurrences for the current base column. (ie: total_goals, total_passes, etc.)
        
            total_label = ("total_" 
                           + col.replace("_won", "")
                            .replace("accurate_", "")
                            .replace("successful_", "")
                            )

            total_labels.append(total_label)
            pct = df_temp[percent_col].replace(0, np.nan)
            df_temp[total_label] = (df_temp[col].div(pct.div(100)).fillna(0))

        # Group the data by player and sum the base columns and their corresponding total columns.
        df_percent = (df_temp.groupby("Full_Name")[base_cols + total_labels].sum())

        season_cols = []

        for base_col, tot_col in zip(base_cols, total_labels):

            # Calculate the season percentage for the current base column and its corresponding total column.
            season_lab = f"{base_col}_season_percent"

            df_percent[season_lab] = (
                df_percent[base_col]
                .div(df_percent[tot_col].replace(0, np.nan))
                .mul(100).fillna(0))

            season_cols.append(season_lab)

        return (df_percent.reset_index()
                [["Full_Name"] + season_cols])


    def prepare_position_data(
                            self,
                            position: str,
                            metrics: dict[str, str],) -> pd.DataFrame:

        """
        
        Prepare position-specific data for a given player position.
        Metrics to be included in the position-specific data.

        Returns a DataFrame containing the prepared position-specific data.
        """

        metric_cols = list(metrics.keys())

        cols = [
            "gameweek",
            "Full_Name",
            "team",
            "minutes_played",
        ] + metric_cols

        position_df = self.player_match_df.loc[
            (self.player_match_df["position"] == position)
            & (self.player_match_df["minutes_played"] > 0),
            cols,].copy()


        perc_col = [col for col in metric_cols if col.endswith('_percent')]
        non_perc_col = [col for col in metric_cols if col not in perc_col]


        # Group the position-specific data by player and team, summing the non-percentage columns and calculating per-90 values.
        grouped = (position_df.groupby(["Full_Name", "team"])[['minutes_played'] + non_perc_col]).sum()
        grouped["per90"] = grouped["minutes_played"].div(90).replace(0, np.nan)
        grouped[non_perc_col] = grouped[non_perc_col].div(grouped["per90"], axis=0)

        grouped = grouped.reset_index()

        # Finds any percentage columns in the metrics and calculates their season percentages.
        if perc_col:
            season_perct = self.get_season_perc(perc_col)

            pos_summary = grouped.merge(
                season_perct,
                on="Full_Name",
                how="left"
            )

        else:
            pos_summary = grouped

        pos_summary.drop(
            columns=["minutes_played", "per90"],
            inplace=True)
        
        dupes = (
            pos_summary[
            pos_summary["Full_Name"].duplicated(keep=False)]
            ["Full_Name"]
            .unique()
                )
        
        # Remove duplicate entries for players who have played for multiple teams, keeping only the most recent team.
        for dup in dupes:
            # map each player's team at gameweek 1 (if present)
                old_team = self.player_match_df.loc[
                    (self.player_match_df["Full_Name"] == dup)
                    & (self.player_match_df["gameweek"] == 1),
                    "team",].iloc[0]
                
                pos_summary = pos_summary.loc[
                    ~((pos_summary["Full_Name"] == dup)
                    & (pos_summary["team"] == old_team))] 
        
        return pos_summary

    
    @staticmethod
    def normalize_metrics(metrics: dict[str, str])-> tuple[dict[str, str], list[int]]:
        """
        Normalize the metrics dictionary by renaming percentage columns to indicate they are season percentages.
        Renames any columns ending with "_percent" to "_season_percent"
        This is to update the labels in the position-specific data.
        """

        new_metrics = {}
        ind = []
        for i, (key, value) in enumerate(metrics.items()):
            if key.endswith("_percent"):
                new_key = key.replace(
                    "_percent",
                    "_season_percent"
                )

                ind.append(i)

            else:
                new_key = key

            new_metrics[new_key] = value

        return new_metrics, ind 

    @staticmethod
    def calculate_ranges( 
                        p1_vals: list[float], 
                        p2_vals: list[float]) -> tuple[list[float], list[float]]:
        
        min_ranges = []
        max_ranges = []

        for value_1, value_2 in zip(p1_vals, p2_vals):
            low = min(value_1, value_2)
            high = max(value_1, value_2)

            if low == high:
                padding = max(abs(low) * 0.2, 0.1)
                min_ranges.append(low - padding)                
                max_ranges.append(high + padding)
                continue
            
            lower_bound = low - abs(low) * 0.20
            upper_bound = high + abs(high) * 0.20

            if lower_bound == upper_bound:
                upper_bound = lower_bound + 0.1
                
            min_ranges.append(lower_bound)
            max_ranges.append(upper_bound)

        return min_ranges, max_ranges
    

  
    def build_comparison(self,
                        player_1: str,
                        player_2: str,
                        position: str,
                        metrics: dict[str, str]
                        ) -> tuple[list[list[float]], list[list[float]]]:
        """
        Compute per-90 aggregated values for two players and plot radar.
        Compares the two players based on the specified position and metrics.

        Returns a dictionary containing the player names, team names, metric labels, player values, and the calculated min and max ranges for plotting.
       
        """
        # Prepare data and denominators
        
        pos_df = self.prepare_position_data(position=position, metrics=metrics)

        metrics_normalized, ind_perc = self.normalize_metrics(metrics)
        metric_cols = list(metrics_normalized.keys())
       
        if player_1 not in pos_df['Full_Name'].values:
            raise ValueError(f"No minutes found for player: {player_1}")
        
        if player_2 not in pos_df['Full_Name'].values:
            raise ValueError(f"No minutes found for player: {player_2}")

        curr_team_1 = self.get_team(player_1)
        curr_team_2 = self.get_team(player_2)

        p1_vals: list[float] = pos_df.loc[
                    (pos_df['Full_Name'] == player_1) 
                     & (pos_df['team'] == curr_team_1)][metric_cols].values.tolist()[0]
        
        p2_vals: list[float] = pos_df.loc[
                    (pos_df['Full_Name'] == player_2) 
                     & (pos_df['team'] == curr_team_2)][metric_cols].values.tolist()[0]

        min_ranges, max_ranges = (self.calculate_ranges(p1_vals, p2_vals,))

        for i in ind_perc:
            min_ranges[i] = 0
            max_ranges[i] = 100

                
        return {
                "player_1": player_1,
                "player_2": player_2,
                "team_1": curr_team_1,
                "team_2": curr_team_2,
                "metric_labels": list(metrics_normalized.values()),
                "values_1": p1_vals,
                "values_2": p2_vals,
                "min_ranges": min_ranges,
                "max_ranges": max_ranges,
                }


    def build_comparison_set(self,
                        pairs: list[tuple[str, str]],
                        position: str,
                        metrics: dict[str, str],
                        ) -> list[dict]:
        """
        Build all radar comparisons for the given pairs of players, position, and metrics.
        Returns a list of dictionaries, each containing the player names, team names, metric labels, player values, and the calculated min and max ranges for plotting.
        """

        position_df = self.prepare_position_data(position=position,metrics=metrics,)

        metrics_normalized, ind_perc = self.normalize_metrics(metrics)
        metric_columns = list(metrics_normalized.keys())

        comparisons = []

        for player_1, player_2 in pairs:
            team_1 = self.get_team(player_1)
            team_2 = self.get_team(player_2)

            values_1 = (position_df.loc[(position_df["Full_Name"]== player_1)
                                        & (position_df["team"]== team_1),metric_columns,]
                                        .iloc[0]
                                        .tolist()
                                        )

            values_2 = (position_df.loc[(position_df["Full_Name"] == player_2)
                                        & (position_df["team"] == team_2),metric_columns,]
                                        .iloc[0]
                                        .tolist()
                                        )

            min_ranges, max_ranges = (self.calculate_ranges(values_1,values_2,))

            for i in ind_perc:
                    min_ranges[i] = 0
                    max_ranges[i] = 100

            comparisons.append({
                            "player_1": player_1,
                            "player_2": player_2,
                            "team_1": team_1,
                            "team_2": team_2,
                            "metric_labels": list(metrics_normalized.values()),
                            "values_1": values_1,
                            "values_2": values_2,
                            "min_ranges": min_ranges,
                            "max_ranges": max_ranges,})

        return comparisons

    
    def get_top_player(
                        self,
                        team: str,
                        position: str,
                        metrics: dict,
                    ) -> tuple[str, pd.DataFrame]:
        """
        Return the top player for a team and position along
        with the summary dataframe used in the evaluation.
        """

        position_df = self.prepare_position_data(
            position=position,
            metrics=metrics,
        )

        # Filter the position-specific data for the given team.
        team_position_df = position_df[
            position_df["team"] == team
        ]

        # Get the appearances data for the given team.
        appearances_df = (self.player_match_df.groupby(["Full_Name", "team"])["minutes_played"]
            .value_counts()
            .reset_index()
            .sort_values(by=["minutes_played", "count"],
                        ascending=[False, False],))

        team_appearances = appearances_df[
            (appearances_df["team"] == team)
            &(appearances_df["minutes_played"] > 0)]

        # Build the summary dataframe for the team's players.
        # This includes the number of games played, total minutes played, and average minutes per appearance.
        summary = pd.concat([
            team_appearances.groupby("Full_Name")["count"].sum(),
            team_appearances.groupby("Full_Name").apply(lambda x:(x["minutes_played"]*x["count"]).sum()),],
            axis=1,)

        summary = (summary.reset_index().rename(columns={0: "minutes_played"}))

        summary["ave_min_per_app"] = (summary["minutes_played"]/summary["count"])

        summary = (summary.merge(
                team_position_df, on="Full_Name",).rename(
                columns={"count": "gms_played"}))

        summary.drop(
            columns=["team", "minutes_played"],
            inplace=True,)

        multi_team_players = (self.players_with_multiple_teams())

        # Identify players who have played for multiple teams.
        # Adjust the number of games played for these players based on their appearances for the current team.

        for player in summary["Full_Name"]:
            player_mask = (summary["Full_Name"]== player)

            if player in multi_team_players:
                team_games = team_appearances[team_appearances["Full_Name"]== player]["count"].sum()
                summary.loc[player_mask,"gms_played"] = (summary['gms_played']/team_games).round(2)


            else:
                summary.loc[player_mask,"gms_played"] = (summary['gms_played']/float(self.max_gameweek)).round(2)

        # Calculate weighted player score
        score_columns = [col for col in position_df.columns.tolist() if col not in ["Full_Name", 'team', 'gms_played', 'ave_min_per_app']]

        # Calculate the weighted player score based on the position-specific metrics.
        # If there are fewer than 3 players, select the one with the most games played.
        # Otherwise, calculate the weighted score for each player and select the one with the highest score.
        
        if len(summary) < 3: 
            max_sum_index = summary['gms_played'].idxmax()
            player_name = summary.loc[max_sum_index, 'Full_Name']


        if len(summary)>=3:
            summary = summary[(summary['ave_min_per_app'] > 50) & (summary['gms_played'] > .50)].sort_values(by='gms_played', ascending=False)
            summary['score'] = (summary[score_columns].rank(pct=True, ascending=True).sum(axis=1))
            maxind = summary['score'].idxmax()

            player_name = summary.loc[maxind, 'Full_Name']

        return player_name, summary

    def build_top_scorer_lookup(self):

        df = self.player_match_df.copy()

        scorers = (df.groupby(["team", "Full_Name"])["goals"]
                .sum().reset_index()
                .sort_values(["team", "goals"],ascending=[True, False])
        )

        scorers = (scorers.groupby("team")
                    .first().reset_index())

        return scorers.set_index("team").to_dict("index")