import pygame
from gui.main_menu import MainMenu
from gui.simulation_menu import SimulationMenu
from gui.map_editor_menu import MapEditorMenu
from gui.map_editor_gui import MapEditor
from gui.simulation_gui import SimulationGUI
from gui.sub_select import SubmarineSelectionMenu
import os
from simulation.map import MAP_DIR

class GuiApp:
    """Huvudappen som hanterar sidväxling."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        pygame.display.set_caption("Submarine Simulation")
        self.pages = {}
        self.current_page = None
        self.running = True

    # def change_page(self, page_name, **kwargs):
    #     """Byt till en annan sida."""
    #     self.running = False  # Stoppa nuvarande sidans loop
    #     self.change_page_callback(page_name, **kwargs)

    def set_page(self, page_name, **kwargs):
        """Byt till en ny sida och säkerställ att relevanta sidor uppdateras."""
        if page_name == "map_editor":
            map_file = kwargs.get("map_file", None)
            if map_file:
                # Ladda kartan från filen och få dess storlek
                from simulation.map import Map  # Importera Map-klassen
                map_obj = Map(file_name=os.path.join(MAP_DIR, map_file))
                width = len(map_obj._map[0])
                height = len(map_obj._map)
                self.pages["map_editor"] = MapEditor(self.screen, self.set_page, width, height, map_file=map_file)
            elif "width" in kwargs and "height" in kwargs:
                # Skapa en ny karta med angiven storlek
                self.pages["map_editor"] = MapEditor(self.screen, self.set_page, kwargs["width"], kwargs["height"])

        elif page_name == "simulation":
            map_file = kwargs.get("map_file", "default_map.txt")
            fleet_file = kwargs.get("fleet_file", "uboat.txt")
            self.pages["simulation"] = SimulationGUI(self.screen, self.set_page, map_file, fleet_file)

        elif page_name == "submarine_selection" and "map_file" in kwargs:
            self.pages["submarine_selection"] = SubmarineSelectionMenu(self.screen, self.set_page, kwargs["map_file"])
        
        elif page_name == "simulation_menu":
            self.pages["simulation_menu"] = SimulationMenu(self.screen, self.set_page)

        self.current_page = self.pages[page_name]

    def initialize_pages(self):
        """Initialisera alla sidor."""
        self.pages["main"] = MainMenu(self.screen, self.set_page)
        self.pages["simulation_menu"] = SimulationMenu(self.screen, self.set_page)
        self.pages["map_editor_menu"] = MapEditorMenu(self.screen, self.set_page)

    def run(self):
        """Huvudloopen för applikationen."""
        self.initialize_pages() 
        self.set_page("main")
        while self.running:
            self.current_page.run()
            if not self.running:
                break

        pygame.quit()

if __name__ == "__main__":
    app = GuiApp()
    app.run()
