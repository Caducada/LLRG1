import sys
import os


# Lägg till 'src' i sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from simulation.simulation import runsim

# Kör GUI
from gui.gui import GuiApp

if __name__ == "__main__":
    # app = GuiApp()
    # app.run()

    runsim(fleet_name="simple.txt", map_name="underground.txt")