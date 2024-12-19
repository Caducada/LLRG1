import pygame

class BaseGUI:
    """Bas för alla GUI-komponenter."""
    def __init__(self, screen):
        self.screen = screen
        self.running = False

    def run(self):
        """Kör huvudloopen för GUI."""
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()

    def handle_events(self):
        """Hantera händelser (kan överskrivas i subklasser)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Uppdatera tillstånd (överskrid i subklasser)."""
        pass

    def render(self):
        """Rendera grafik (överskrid i subklasser)."""
        pass