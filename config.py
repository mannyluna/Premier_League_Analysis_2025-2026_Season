"""
Application configuration.

Contains:
- Paths
- Output directories
- League settings
- Visualization settings
"""

from pathlib import Path


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"

EPL_DATA = DATA_DIR / "premier_league"

LOGO_DIR = PROJECT_ROOT  / "logos"

OUTPUT_DIR = PROJECT_ROOT / "outputs"

VISUALS_DIR = PROJECT_ROOT  / "visuals"


# ==========================================================
# Source Data Files
# ==========================================================

PLAYERS_FILE = DATA_DIR / "players.csv"

PLAYER_STATS_FILE = DATA_DIR / "playerstats.csv"

PLAYER_MATCH_FILE = DATA_DIR / "playermatch.csv"

PLAYER_GAMEWEEK_FILE = DATA_DIR / "player_gameweek.csv"

TEAMS_FILE = DATA_DIR / "teams.csv"

TRANSFERS_FILE = DATA_DIR / "transfers.csv"

FIXTURES_FILE = DATA_DIR / "fixtures.csv"


# ==========================================================
# League Setup
# ==========================================================

LEAGUE_NAME = "Premier League"

SEASON = "2025-2026"

EXPECTED_TEAMS = 20




