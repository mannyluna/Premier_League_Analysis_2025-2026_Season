
from matplotlib.patches import RegularPolygon, Rectangle
import numpy as np
from mplsoccer import VerticalPitch
from matplotlib.patches import RegularPolygon,Circle, Rectangle, Wedge
from analysis.player_analyzer import PlayerAnalyzer
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import cmasher as cmr  
from matplotlib.colors import to_hex
import constants.constants as cons
import pandas as pd
import matplotlib.patheffects as path_effects
from mycolorpy import colorlist as mcp


# Constants and mappings for pitch visuals
TEAM_NAME_MAP = cons.TEAM_NAME_MAP
TEXT_EFFECTS = [path_effects.Stroke(linewidth=1.5, foreground='#efe9e6'), path_effects.Normal()]
GREEN_MAP = cmr.get_sub_cmap('Greens', 0, 1)

def draw_field(ax: plt.Axes):
    #Drawing the half pitch
    pitch = VerticalPitch(
        pitch_type='uefa', half=True, goal_type='box', linewidth=1,
        pitch_color="#fefffc", line_color="#00000047",
        stripe=False,
        pad_bottom=0,    # <-- remove padding
        pad_top=25,       # <-- remove padding
        goal_alpha=0.9, line_zorder=2
    )
    pitch.draw(ax=ax)
    
    
    return pitch




def color_from_pct_cached(pct: float) -> str:
    # Get the hex color for a given percentage using the cached green colormap
    # lower percentages will be lighter in color, which will be used for visualizing performance.
    if pct is None:
        return "#ffffff"
    
    t = np.clip(pct, 0, 100)
    norm = Normalize(vmin=0, vmax=100)  
    rgba = GREEN_MAP(norm(t))
    
    return to_hex(rgba)

def get_rank_color(rank: int) -> str:
    # Get the hex color for a given rank based on the team's position in the league table.

    if rank in cons.CHAMPIONS_LEAGUE_POSITIONS:
        return "#36C736A2"
    
    if rank in cons.EUROPA_LEAGUE_POSITIONS:
        return "#3F88DBA0"
    
    if rank in cons.RELEGATION_POSITIONS:
        return "#F11414B3"
    
    return "none"



def create_team_artists(ax: plt.Axes, 
                        primary_x: list[float], 
                        primary: list[str],  
                        top_y: float,  
                        hex_radius: float):

    """
    Initialize the visual elements for a team's representation on the pitch.
    Creates the different visual elements for the team's representation on the pitch.
    Patches on the pitch for the team's representation of shooting performance.
    Returns a dictionary containing all the matplotlib artists for the team visualization.

    """
    
    # Initialize the dictionary to hold all the artists for the team visualization.
    artists = {
        "hex_patches": [],
        "label_texts": [],
        "stat_texts": [],
        "rects": [],
        "title_text": None,
        "score_text": None,
        "top_stat_text": None,
        "rank_circle": None,
        "rank_text": None
    }

    # primary hexes
    for x, label in zip(primary_x, primary):
        
        hp = RegularPolygon((x, top_y), numVertices=6, radius= hex_radius, edgecolor='black', facecolor='#FFFFFF', alpha=0.5, lw=1.25)
        
        ax.add_patch(hp)
        artists["hex_patches"].append(hp)
        artists["label_texts"].append(ax.text(x, top_y + 6, label, ha='center', va='center', weight='bold', size=7))
        st = ax.text(x, top_y, "", ha='center', va='center', weight='bold', size=7)
        st.set_path_effects(TEXT_EFFECTS)
        artists["stat_texts"].append(st)


    # colored patches (main, wedge, left, right)
    # Used for shooting performance visualization
    rect_main = Rectangle((13.7, 88.5), 40.5, 16.5, linestyle = 'None', facecolor='none', alpha=0.6)
    wedge = Wedge(center=(34,88.5), r=34, theta1=180, theta2=360, facecolor='none', edgecolor='none', alpha=0.6)
    rect_l = Rectangle((0, 88.5), 13.5, 16.8, linestyle = 'None', facecolor='none', alpha=0.6)
    rect_r = Rectangle((54, 88.5), 13.5, 16.8, linestyle = 'None', facecolor='none', alpha=0.6)

    for p in (rect_main, wedge, rect_l, rect_r):
        ax.add_patch(p)
        artists["rects"].append(p)

    # title/score/top stat
    artists["title_text"] = None
    artists["score_text"] = None
    artists["top_stat_text"] = None



    # rank circle + text
    # Rank circle and text for the team's ranking 
    rc = Circle((7,112.5), radius=3.5, linewidth=1.5, facecolor='none', alpha=0.6, edgecolor='black')
    ax.add_patch(rc)
    
    artists["rank_circle"] = rc
    artists["rank_text"] = ax.text(7, 112.5, "", ha='center', va='center', weight='bold', size=10)

    return artists



def update_team_artists(ax, artists, offensive_data: dict, team_data: pd.DataFrame, team_shortname: str, season_table: pd.DataFrame, player_match_names: pd.DataFrame):

    """
    Update the visual elements for a team's representation on the pitch based on the provided offensive data, team data, and player match names.
    Sets the text for the stat labels, shooting performance patches, and team ranking.
    """

    # update stat texts (labels were created with text content already)
    labels = [t.get_text() for t in artists["label_texts"]]

    for st, label in zip(artists["stat_texts"], labels):
        raw = offensive_data.get(label, "")
        display = f"{raw}%" if '%' in label else raw
        st.set_text(display)

    # color main patches by shots inside/outside
    shots_in = offensive_data.get('Shots Inside the Box %', 0)
    shots_out = offensive_data.get('Shots Outside the Box %', 0)
    artists["rects"][0].set_facecolor(color_from_pct_cached(shots_in))

    # color the remaining rectangles based on shots outside the box
    for r in artists["rects"][1:]:
        r.set_facecolor(color_from_pct_cached(shots_out))

    text_in = ax.annotate(text=f"{shots_in}%", xy=(46, 75), textcoords='offset points',
                            size=10, ha='center', va='center', weight='bold')
    text_out = ax.annotate(text=f"{shots_out}%", xy=(46, 64), textcoords='offset points',
                            size=10, ha='center', va='center', weight='bold')
    
    text_in.set_path_effects(TEXT_EFFECTS)
    text_out.set_path_effects(TEXT_EFFECTS)

    # title and scores
    home_goals = int(team_data.loc[team_data['is_home'] == True, 'score'].iat[0]) if (team_data['is_home'] == True).any() else 0
    away_goals = int(team_data.loc[team_data['is_home'] == False, 'score'].iat[0]) if (team_data['is_home'] == False).any() else 0
    artists["title_text"] = ax.annotate(text = TEAM_NAME_MAP.get(team_shortname, team_shortname).upper(), xy = (34,118), ha='center', va='center', weight = 'bold', size = 9)
    artists["score_text"] = ax.annotate(text = f"Goals: {home_goals + away_goals} | Home: {home_goals} | Away: {away_goals}", xy = (34,114), ha='center', va='center', size = 8.5)

    max_gw = season_table.columns[-1].split('_')[-2]
    # Get the top scorer for the team
    top_scorer_lookup = PlayerAnalyzer(player_match_names, max_gw).build_top_scorer_lookup()

    # Annotate name and number of goals for the top scorer
    if top_scorer_lookup.get(team_shortname) is not None:
        top = top_scorer_lookup[team_shortname]
        artists["top_stat_text"] = ax.annotate(text = f"{top['Full_Name']} | Goals: {int(top['goals'])}", xy = (34,111), ha='center', va='center', size = 8.5)
    else:
        artists["top_stat_text"].set_text("")

    # rank of the team in the season table
    mask = season_table['team'] == team_shortname
    rank = season_table.loc[mask, f'gmwk_{max_gw}_rank'].values[0].astype(int)

    # Get the color for the rank circle based on the team's rank. Champions League, Europa League, or Relegation.
    face = get_rank_color(rank)

    artists["rank_circle"].set_facecolor(face)
    artists["rank_text"].set_text(str(rank))

    return