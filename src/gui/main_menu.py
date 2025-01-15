import pygame
from gui.base_gui import BaseGUI

class MainMenu(BaseGUI):
    """Huvudmeny med navigering."""
    def __init__(self, screen, change_page_callback):
        super().__init__(screen, change_page_callback)
        self.set_title("Lindas Lustfyllda Rederi")
        self.add_option("Simulation", lambda: self.change_page("simulation_menu"))
        self.add_option("Map Editor", lambda: self.change_page("map_editor_menu"))
        self.add_option("Exit", lambda: pygame.quit())
