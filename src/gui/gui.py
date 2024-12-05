import pygame
from gui.map_editor_gui import MapEditor
from gui.simulation_gui import SimulationGUI

class GuiApp:
    """Huvudklass som hanterar hela applikationen"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Submarine Simulation")
        self.clock = pygame.time.Clock()
        self.running = True

        self.active_screen = "menu"

        self.map_editor = MapEditor(self.screen)
        self.simulation = SimulationGUI(self.screen)

    def main_menu(self):
        font = pygame.font.Font(None, 36)
        menu_items = ["1. Map editor", "2. Simulation", "3. Quit"]
        selected_option = None

        while selected_option is None:
            self.screen.fill((0, 0, 0))
            for i, text in enumerate(menu_items):
                rendered_text = font.render(text, True, (255, 255, 255))
                self.screen.blit(rendered_text, (200, 100 + i * 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.active_screen = "map_editor"
                        return
                    elif event.key == pygame.K_2:
                        self.active_screen = "simulation"
                        return
                    elif event.key == pygame.K_3:
                        self.running = False
                        return
    def run(self):
        """Huvudkörningen för hela gui-applikationen."""
        while self.running:
            if self.active_screen == "menu":
                self.main_menu()
            elif self.active_screen == "map_editor":
                self.map_editor.run()
                self.active_screen = "menu"
            elif self.active_screen == "simulation":
                self.simulation_gui.run()
                self.active_screen = "menu" 
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    app = GuiApp()  # Skapa en instans av huvudklassen
    app.run()    # Kör applikationen
