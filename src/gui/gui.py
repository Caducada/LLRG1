import pygame
from gui.map_editor_gui import MapEditor
from gui.simulation_gui import SimulationGUI
from gui.base_gui import BaseGUI

class GuiApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1600, 1200))
        self.clock = pygame.time.Clock()
        self.running = True

        self.menu = MenuScreen(self.screen, self.handle_menu_selection)
        self.map_editor = MapEditor(self.screen)
        self.simulation = SimulationGUI(self.screen)

    def handle_menu_selection(self, option_index):
        if option_index == 0:
            self.menu = None
            self.map_editor.run()
        elif option_index == 1:
            self.menu = None
            self.simulation.run()
        elif option_index == 2:
            self.running = False

    def run(self):
        while self.running:
            if self.menu:
                self.menu.run()
            self.clock.tick(60)
        pygame.quit()


class MenuScreen(BaseGUI):
    def __init__(self, screen, on_option_selected):
        super().__init__(screen)
        self.options = ["Map Editor", "Simulation", "Quit"]
        self.on_option_selected = on_option_selected

    def render(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        for i, option in enumerate(self.options):
            text = font.render(f"{i + 1}. {option}", True, (255, 255, 255))
            self.screen.blit(text, (100, 100 + i * 50))

    def handle_events(self):
        super().handle_events()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    self.on_option_selected(event.key - pygame.K_1)
                    self.running = False

if __name__ == "__main__":
    app = GuiApp()  # Skapa en instans av huvudklassen
    app.run()    # Kör applikationen
