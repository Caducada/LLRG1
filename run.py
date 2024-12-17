import sys
import os
from scripts.run_vision_test import run_sim

# Lägg till 'src' i sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

# Kör GUI
from gui.gui import GuiApp

if __name__ == "__main__":
    app = GuiApp()
    app.run()