import pygame

class BaseGUI:
    """Bas för alla GUI-komponenter."""
    def __init__(self, screen):
        self.screen = screen
        self.running = False

    def run(self, fps=60):
        """Kör huvudloopen med angiven FPS."""
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            clock.tick(fps)  # Begränsa FPS

    def handle_events(self):
        """Hantera händelser."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Uppdatera tillstånd."""
        pass

    def render(self):
        """Rendera grafik."""
        pass


