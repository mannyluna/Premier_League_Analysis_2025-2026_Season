import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from analysis.team_seasonranker import TeamAnalyzer


class LeagueTableAnimation:

    def __init__(
        self,
        fixtures_df: pd.DataFrame,
        team_colors: dict[str, str],
    ):
        self.team_colors = team_colors

        self.team_analyzer = TeamAnalyzer(fixtures_df)

        self.season_table = (self.team_analyzer.rank_all_gameweeks())

        self.teams = (self.season_table["team"].tolist())

        self.max_gameweek = len([column for column in self.season_table.columns
                                if column.startswith("gmwk_") and column.endswith("_rank")
                                ])

    def _build_rankings_df(self) -> pd.DataFrame:
        """
        Build a DataFrame that represents the league table rankings for each week.
        The resulting DataFrame has weeks as the index and teams as columns, with the values being the rank of each team in that week.
        """

        rank_cols = [f"gmwk_{week}_rank" for week in range(1, self.max_gameweek + 1)]

        season_update = (self.season_table.set_index("team")[rank_cols])

        season_update = season_update.T.reset_index(level = 0, drop= True)
        season_update.index = pd.RangeIndex(1, self.max_gameweek + 1, name='week')

        return season_update

    def create_animation(self,
                        figsize: tuple = (20, 10),
                        interval: int = 700,):

        # Build the rankings DataFrame for the animation.
        # Animation that will visualize the league table rankings for each week.
        # Build the rankings DataFrame for the animation.
        rankings = self._build_rankings_df()

        weeks = list(range(1, self.max_gameweek + 1))

        fig, ax = plt.subplots(figsize=figsize)

        lines = {}
        labels = {}

        for team in self.teams:
            # Get the color for the team, defaulting to black if not specified.
            color = self.team_colors.get(team,"#000000",)

            # Create the line and label for the team in the plot.
            line, = ax.plot([],[], lw=1, marker="o", color=color,)
            label = ax.text(0, 0, team, fontsize=10, color=color,)

            lines[team] = line
            labels[team] = label

        ax.set_xlim(1, self.max_gameweek)
        ax.set_ylim(0.5, len(self.teams) + 0.5,)

        ax.set_yticks(range(1, len(self.teams) + 1))
        ax.set_xticks(range(2, self.max_gameweek + 1, 2,))

        ax.invert_yaxis()

        ax.set_xlabel("Game Week", fontsize=12, fontfamily = 'serif', labelpad=10)
        ax.set_ylabel("Table Rank", fontsize=12, fontfamily = 'serif', labelpad=10)
        ax.set_title("2025-2026 Season- Premier League Table Rank by Game Week", fontsize=14, fontfamily = 'serif', weight='bold', pad=10)

        plt.subplots_adjust(right=.85)

        def update(frame):

            # Update the plot for the current week.
            current_week = frame + 1

            artists = []

            for team in self.teams:
                # Get the x and y data for the current week.
                x_data = weeks[:current_week]
                y_data = rankings.loc[:current_week, team]

                # Update the line and label for the current week.
                lines[team].set_data(x_data,y_data,)

                latest_rank = y_data.iloc[-1]

                # Get the latest rank for the team in the current week.
                labels[team].set_position((current_week + 0.25, latest_rank,))
                labels[team].set_text(f"{team} ({latest_rank})")

                # Add the line and label to the list of artists for the current frame.
                artists.extend([lines[team], labels[team],])

            return artists

        # Create the animation object using FuncAnimation.
        ani = animation.FuncAnimation(
            fig,
            update,
            frames=self.max_gameweek,
            interval=interval,
            blit=False,
        )

        plt.close(fig)

        return fig, ani