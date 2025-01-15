import pygame
from gui.main_menu import MainMenu
from gui.simulation_menu import SimulationMenu
from gui.map_editor_menu import MapEditorMenu

class GuiApp:
    """Huvudappen som hanterar sidväxling."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Submarine Simulation")
        self.pages = {}
        self.current_page = None

    def set_page(self, page_name, **kwargs):
        """Byt till en ny sida."""
        self.current_page = self.pages[page_name]
        if kwargs and hasattr(self.current_page, "load_data"):
            self.current_page.load_data(**kwargs)

    def initialize_pages(self):
        """Initialisera alla sidor."""
        self.pages["main"] = MainMenu(self.screen, self.set_page)
        self.pages["simulation_menu"] = SimulationMenu(self.screen, self.set_page, ["map1.txt", "map2.txt"])
        self.pages["map_editor_menu"] = MapEditorMenu(self.screen, self.set_page)

    def run(self):
        """Huvudloopen för applikationen."""
        self.initialize_pages()  # Flytta detta här för att säkerställa att sidor är initialiserade
        self.set_page("main")
        while True:
            self.current_page.run()

if __name__ == "__main__":
    app = GuiApp()
    app.run()
