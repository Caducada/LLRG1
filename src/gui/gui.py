import pygame
from gui.main_menu import MainMenu
from gui.map_editor_gui import MapEditor
from gui.simulation_gui import SimulationGUI

class GuiApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Submarine Simulation")
        self.clock = pygame.time.Clock()
        self.running = True

        # Skapa menyer och andra delar
        self.menu = MainMenu(self.screen, self.handle_menu_selection)
        self.map_editor = MapEditor(self.screen)
        self.simulation = SimulationGUI(self.screen)

    def handle_menu_selection(self, index):
        """Hantera val från huvudmenyn."""
        if index == 0:  # Simulation
            self.simulation.run()
        elif index == 1:  # Map Editor
            self.map_editor.run()
        elif index == 2:  # Exit
            print("Exiting application...")  # Debug
            pygame.quit()
            exit()

    def run(self):
        """Huvudloopen för hela GUI-applikationen."""
        while True:
            self.menu.run()  # Kör menyn tills något annat startas eller Exit väljs
            self.clock.tick(60)

if __name__ == "__main__":
    app = GuiApp()
    app.run()
