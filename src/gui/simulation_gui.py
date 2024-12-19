import pygame
from gui.base_gui import BaseGUI

class SimulationGUI(BaseGUI):
    def handle_events(self):
        super().handle_events()
    """Hantera simuleringens GUI."""
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        """Kör simuleringen."""
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            # Här lägger du till rendering av simuleringen
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False