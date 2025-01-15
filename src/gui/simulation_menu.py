import pygame
from gui.base_gui import BaseGUI

class SimulationMenu(BaseGUI):
    """Simuleringsmenyn."""
    def __init__(self, screen, change_page_callback, map_files):
        super().__init__(screen, change_page_callback)
        self.set_title("Välj en karta")
        for map_file in map_files:
            # Bind map_file som en standardparameter
            self.add_option(map_file, lambda f=map_file: self.start_simulation(f))
        self.add_option("Back", lambda: self.change_page("main"))

    def start_simulation(self, map_file):
        """Starta simuleringen för vald karta."""
        print(f"Startar simulering med kartan {map_file}")
        self.change_page("simulation", map_file=map_file)

