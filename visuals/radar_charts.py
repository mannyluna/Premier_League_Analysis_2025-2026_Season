import matplotlib.pyplot as plt
from mplsoccer import Radar
from mplsoccer import FontManager
from logos.logo_loader import LogoManager as lm
from constants.constants import TEAM_NAME_MAP as team_map

# --------------------------------------------------------
# Fonts
# --------------------------------------------------------

ROBOTO_BOLD = FontManager(
    "https://raw.githubusercontent.com/google/fonts/main/"
    "apache/robotoslab/"
    "RobotoSlab%5Bwght%5D.ttf"
)

"""
Radar chart visualization for player comparisons.
Takes a list of player comparisons and visualizes them using radar charts.
"""

def _add_labels(ax,
                comparison: dict,
                colors: tuple[str, str],) -> None:

    # Add labels for the players and their respective teams to the radar chart.

    ax.text(
        0,
        1.10,
        comparison["player_1"],
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        horizontalalignment="left",
        fontproperties=ROBOTO_BOLD.prop,)

    ax.text(
        0, 1.05,
        team_map.get(comparison["team_1"], "Unknown"),
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        horizontalalignment="left",
        color=colors[0],)

    ax.text(
        .98, 1.10,
        comparison["player_2"],
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        horizontalalignment="right",
        fontproperties=ROBOTO_BOLD.prop,)

    ax.text(
        .98, 1.05,
        team_map.get(comparison["team_2"], "Unknown"),
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        horizontalalignment="right",
        color=colors[1],)


def _add_logos(ax,
            comparison: dict,
            logo_manager: lm,
            ) -> None:
    """
    Add team logos to radar chart.
    """
    logo_manager = lm()  
    logo_manager.load_logos()
    
    logo_manager.add_logo(
        ax=ax,
        team=comparison["team_1"],
        xy_cor=(-6.75, 6.75),
        zoom=0.04,
    )

    logo_manager.add_logo(
        ax=ax,
        team=comparison["team_2"],
        xy_cor=(6.75, 6.75),
        zoom=0.04,
    )


def plot_radar(ax,
            comparison: dict,
            colors: tuple[str, str],
            logo_manager: lm,) -> None:
    """
    Plot a single radar comparison for players of the same position
    The comparison dictionary should contain the necessary metrics, values, and team information for the radar chart.
    """

    radar = Radar(
        params=comparison["metric_labels"],
        min_range=comparison["min_ranges"],
        max_range=comparison["max_ranges"],
        num_rings=5,
    )

    radar.setup_axis(ax=ax)

    radar.draw_circles(
        ax=ax,
        facecolor="#D3D3D3",
        edgecolor="#D3D3D3",
    )

    radar.draw_radar_compare(
        comparison["values_1"],
        comparison["values_2"],
        ax=ax,
        kwargs_radar={
            "facecolor": colors[0],
            "alpha": 0.60,},
        kwargs_compare={
            "facecolor": colors[1],
            "alpha": 0.70,},)

    radar.draw_range_labels(
        ax=ax,fontsize=8,
        fontproperties="Times New Roman",)

    radar.draw_param_labels(
        ax=ax,fontsize=8,
        fontproperties="Times New Roman",)

    _add_labels(
        ax=ax,
        comparison=comparison,
        colors=colors,
    )

    _add_logos(
        ax=ax,
        comparison=comparison,
        logo_manager=logo_manager,)



def radar_visualization(comparisons: list[dict],
                        color_pairs: list[tuple[str, str]],
                        position: str,
                        nrows: int = 5,
                        ncols: int = 2,
                        figsize: tuple = (25, 25),):

    """
    Visualize player comparisons using radar charts.

    Parameters:
    - comparisons: List of player comparison dictionaries.
    - color_pairs: List of color tuples for the radar charts.
    - position: Position of the players (e.g., "Forward", "Midfielder").
    - nrows: Number of rows in the grid layout.
    - ncols: Number of columns in the grid layout.
    - figsize: Figure size for the plot.
    
    """
    # Limit the number of comparisons to fit within the grid layout.
    max_plots = nrows * ncols

    comparisons = comparisons[:max_plots]
    color_pairs = color_pairs[:max_plots]

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize,
    )

    axes = axes.flatten()

    for ax in axes[len(comparisons):]:
        ax.axis("off")

    for ax, comparison, colors in zip(axes, comparisons, color_pairs,):

        plot_radar(ax=ax,
            comparison=comparison,
            colors=colors,
            logo_manager= lm,)

    fig.suptitle(
        f"2025-2026 Season Player Comparisons: {position}s",
        fontsize=18,
        fontweight="bold",
        y=1.01, 
        fontfamily='serif',
    )

    fig.tight_layout(h_pad=4, w_pad=2)

    return 