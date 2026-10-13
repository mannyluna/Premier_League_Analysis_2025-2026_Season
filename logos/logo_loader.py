from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import config

class LogoManager:
    """
    A class to manage team logos for the project.
    Loads logos from a specified directory and provides methods to access and display them.

    """

    def __init__(self, logo_dir = config.LOGO_DIR):
        self.logo_dir = Path(logo_dir)
        self.logos = {}


    def load_logos(self):

        # Load all PNG logos from the specified logo directory.
        # Iterate through all files in the logo directory and load PNG images.

        for file in self.logo_dir.glob('*'):
            if file.suffix.lower() != '.png':
                continue

            team = file.stem
            self.logos[team] = plt.imread(file)
            

    def get_logo(self, team: str) -> str | None:
        
        # Convert the team name to uppercase to match the stored logo keys.

        team = team.upper()
        if team not in self.logos:
            raise ValueError(f"Logo for team '{team}' not found.")
        
        return self.logos[team]

    
    def add_logo(self, ax, team: str, xy_cor: tuple, zoom: float =.05):

        # Get the logo image for the specified team
        # Add the logo to the specified axes at the given coordinates.
        
        image = self.get_logo(team)

        im_offset = OffsetImage(image, zoom=zoom)
        im_annotate = AnnotationBbox(im_offset, xy_cor, frameon=False)
        ax.add_artist(im_annotate)

        return im_annotate

   