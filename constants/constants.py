"""
Soccer Analytics Project Constants
"""

# ==========================================================
# League Information
# ==========================================================

LEAGUE_NAME = "Premier League"

SEASON = "2025-2026"

NUM_TEAMS = 20


# ==========================================================
# Radar Chart Defaults
# ==========================================================

RADAR_NUM_RINGS = 5

RADAR_ALPHA_PRIMARY = 0.60

RADAR_ALPHA_SECONDARY = 0.70

RADAR_LOGO_ZOOM = 0.04

RADAR_TITLE_SIZE = 18

RADAR_PLAYER_SIZE = 10

RADAR_LABEL_SIZE = 8


# ==========================================================
# Animation Defaults
# ==========================================================

ANIMATION_INTERVAL = 700

ANIMATION_FIGSIZE = (20, 10)


# ==========================================================
# Dashboard Defaults
# ==========================================================

TEAM_DASHBOARD_FIGSIZE = (25, 20)

HEX_RADIUS = 4.5

TOP_Y = 66


# ==========================================================
# Team Colors
# ==========================================================

TEAM_COLORS = {
    "ARS": "#EF0107",
    "AVL": "#BDC009",
    "BOU": "#B20023",
    "BRE": "#E30613",
    "BHA": "#0057B8",
    "BUR": "#6C1D45",
    "CHE": "#0768D6",
    "CRY": "#1B458F",
    "EVE": "#234594",
    "FUL": "#000000",
    "LEE": "#CEC21C",
    "LIV": "#C8102E",
    "MCI": "#77BAEC",
    "MUN": "#DA291C",
    "NEW": "#000000",
    "NFO": "#E53233",
    "SUN": "#F9423A",
    "TOT": "#132257",
    "WHU": "#7C2C30",
    "WOL": "#F9A01B",
}

TEAM_NAME_MAP = {
    "ARS": "Arsenal",
    "AVL": "Aston Villa",
    "BUR": "Burnley",
    "BOU": "AFC Bournemouth",
    "BRE": "Brentford",
    "BHA": "Brighton & Hove Albion",
    "WHU": "West Ham United",
    "WOL": "Wolverhampton Wanderers",
    "CHE": "Chelsea",
    "CRY": "Crystal Palace",
    "EVE": "Everton",
    "FUL": "Fulham",
    "LEE": "Leeds United",
    'LIV': 'Liverpool',
    'MCI': 'Manchester City',
    'MUN': 'Manchester United',
    'NEW': 'Newcastle United',
    'NFO': 'Nottingham Forest',
    'SUN': 'Sunderland',
    'TOT': 'Tottenham Hotspur'
}


# ==========================================================
# Goalkeeper Metrics
# ==========================================================

GK_METRICS = {
    "gk_accurate_passes": "Accurate Passes",
    "gk_accurate_long_balls": "Long Balls",
    "saves": "Saves",
    "goals_conceded": "Goals Conceded",
    "xgot_faced": "XGOT Faced",
    "goals_prevented": "Goals Prevented",
    "sweeper_actions": "Sweeper Actions",
    "high_claim": "High Claims",
    "saves_inside_box": "Box Saves",
}


# ==========================================================
# Defender Metrics
# ==========================================================

DEFENDER_METRICS = {
    "tackles_won": "Tackles Won",
    "interceptions": "Interceptions",
    "blocks": "Blocks",
    "clearances": "Clearances",
    'ground_duels_won_percent': "Ground Duels Won %",
    'aerial_duels_won_percent': "Aerial Duels Won %",
    'accurate_passes_percent': "Accurate Passes %",
    'accurate_long_balls_percent': "Accurate Long Balls %",
    'goals': "Goals",
    'assists': "Assists",
}


# ==========================================================
# Midfielder Metrics
# ==========================================================

MIDFIELDER_METRICS = {
    "goals": "Goals",
    "assists": "Assists",
    "xg": "xG",
    "xa": "xA",
    'successful_dribbles': "Successful Dribbles",
    'shots_on_target': "Shots On Target",
    'defensive_contributions': "Defensive Contributions",
    "accurate_passes_percent": "Accurate Passes %",
    'accurate_crosses_percent': "Accurate Crosses %",
    "final_third_passes": "Final Third Passes",
}


# ==========================================================
# Forward Metrics
# ==========================================================

FORWARD_METRICS = {
    "goals": "Goals",
    "assists": "Assists",
    "xg": "xG",
    "xa": "xA",
    "total_shots": "Shots",
    "shots_on_target": "Shots On Target",
    "touches_opposition_box": "Touches In Box",
    "chances_created": "Chances Created",
    "successful_dribbles": "Successful Dribbles",
    "penalties_scored": "Penalties Scored",
}


# ==========================================================
# Team Offensive Metrics
# ==========================================================

OFFENSIVE_METRICS = {
    "total_shots": "Shots",
    "shots_on_target": "SoT",
    "shots_inside_box": "Shots In Box",
    "shots_outside_box": "Shots Outside Box",
    "score": "Goals",
    "expected_goals_xg": "xG",
    "non_penalty_xg": "npxG",
    "xg_on_target_xgot": "xGOT",
}


# ==========================================================
# Defensive Metrics
# ==========================================================

DEFENSIVE_METRICS = {
    "clearances": "Clearances",
    "blocks": "Blocks",
    "interceptions": "Interceptions",
    "tackles_won": "Tackles Won",
}

# ==========================================================
# Pitch Visuals Constants
# ==========================================================

PRIMARY_PITCH_COLS = ['Shots', 'SoT%', 'Goals', 'xG', 'npxG', 'xGOT']
PRIMARY_X_LOC = [62, 50.6, 39.2, 27.8 , 16.4 ,5]

TOP_Y = 66
HEX_RADIUS = 4.5

RANK_CENTER = (7, 112.5)
RANK_RADIUS = 3.5

CHAMPIONS_LEAGUE_POSITIONS = {1, 2, 3, 4}

EUROPA_LEAGUE_POSITIONS = {5}

RELEGATION_POSITIONS = {18, 19, 20}
