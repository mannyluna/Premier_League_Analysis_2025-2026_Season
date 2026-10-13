from dataclasses import dataclass
from unittest import loader

import pandas as pd

from data.data_loader import SoccerDataLoader
import cleaner.player_cleaner as player_cleaner


@dataclass
class SoccerData:
    fixtures: pd.DataFrame
    players: pd.DataFrame
    cleaned_transfers: pd.DataFrame
    teams: pd.DataFrame
    player_match_names: pd.DataFrame
    player_match_data: pd.DataFrame
    team_map: dict
    team_name_map: dict


def build_dataset() -> SoccerData:

    # ---------------------------
    # Load Data
    # ---------------------------

    loader = SoccerDataLoader()

    player_match_data = loader.load_multiple_files("playermatch*.csv")
    fixtures_data = loader.load_multiple_files("fixtures*.csv")

    players_df = loader.load_players()
    transfers_df = loader.load_transfers()
    teams_df = loader.load_teams()

    # ---------------------------
    # Clean Players
    # ---------------------------

    players_df = player_cleaner.clean_players(players_df)

    # ---------------------------
    # Team Mappings
    # ---------------------------

    team_map = dict(
        zip(teams_df["code"], 
            zip(teams_df["fotmob_name"], teams_df["short_name"])
        )
    )

    team_name_map = dict(zip(teams_df["short_name"], teams_df["fotmob_name"]))

    # ---------------------------
    # Enrich Fixture Data
    # ---------------------------

    fixtures_data["home_team_name"] = (
        fixtures_data["home_team"]
        .map(team_map)
        .str[0]
    )

    fixtures_data["away_team_name"] = (
        fixtures_data["away_team"]
        .map(team_map)
        .str[0]
    )

    fixtures_data["home_team_shortname"] = (
        fixtures_data["home_team"]
        .map(team_map)
        .str[1]
    )

    fixtures_data["away_team_shortname"] = (
        fixtures_data["away_team"]
        .map(team_map)
        .str[1]
    )

    # ---------------------------
    # Build Player Match Dataset
    # ---------------------------

    player_match_names = (
        player_match_data
        .merge(players_df, on="player_id")
    )

    player_match_names["team_code"] = (
        player_match_names["team_code"]
        .map(team_map)
        .str[1]
    )

    player_match_names.rename(
        columns={"team_code": "team"},
        inplace=True
    )

    player_match_names["Full_Name"] = (
        player_match_names
        .apply(player_cleaner.get_full_name, axis=1)
    )


    # ---------------------------
    # Clean Transfer Data
    # ---------------------------

    transfers_df = player_cleaner.clean_transfers(transfers_df)

    transfers_df[["First_Name", "Last_Name"]] = (transfers_df["Player"]
                                                 .str.split(" ", n=1, expand=True))

    lst_team = list(team_name_map.values())

    cleaned_transfers = transfers_df.copy()
    cleaned_transfers["Date"] = pd.to_datetime(cleaned_transfers["Date"], errors="coerce")

    mask = (
        cleaned_transfers["Moving to"].isin(lst_team)
        &
        cleaned_transfers["Moving From"].isin(lst_team))

    filtered_transfers = (
        cleaned_transfers.loc[mask, ['Moving From', 'Moving to', 'First_Name', 'Last_Name', 'Date']]
        .dropna(subset=["First_Name"])
        .drop_duplicates()
        .sort_values("Date")
        .reset_index(drop=True)
    )

    reverse_team_map = {
        value: key
        for key, value in team_name_map.items()
    }

    filtered_transfers["Moving From"] = (
        filtered_transfers["Moving From"]
        .map(reverse_team_map)
    )

    filtered_transfers["Moving to"] = (
        filtered_transfers["Moving to"]
        .map(reverse_team_map)
    )

    filtered_transfers['gameweek'] = [20, 22,  23, 24, 24, 25,25]

    player_match_names = player_cleaner.player_transfer(player_match_names, filtered_transfers)

    player_match_names.drop(
            columns=[
                "player_code",
                "first_name",
                "second_name",
                "web_name",
                "alt_name",
                "clean_first_name",
                "clean_last_name",
                "clean_alt_name",
            ],
            errors="ignore",
            inplace=True,
        )
    
    # ---------------------------
    # Return Object
    # ---------------------------

    return SoccerData(
        fixtures=fixtures_data,
        players=players_df,
        cleaned_transfers=filtered_transfers,
        teams=teams_df,
        player_match_names=player_match_names,
        player_match_data=player_match_data,
        team_map=team_map,
        team_name_map=team_name_map,
    )