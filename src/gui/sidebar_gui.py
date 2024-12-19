import pygame

class Sidebar:
    def __init__(self, screen, width):
        self.screen = screen
        self.width = width
        self.buttons = []

    def add_button(self, text, action, color=(150, 150, 150)):
        button_rect = pygame.Rect(10, 10 + len(self.buttons) * 40, self.width - 20, 30)
        self.buttons.append({"rect": button_rect, "text": text, "action": action, "color": color})

    def render(self):
        pygame.draw.rect(self.screen, (220, 220, 220), (0, 0, self.width, self.screen.get_height()))
        font = pygame.font.Font(None, 24)
        for button in self.buttons:
            pygame.draw.rect(self.screen, button["color"], button["rect"])
            text = font.render(button["text"], True, (0, 0, 0))
            self.screen.blit(text, (button["rect"].x + 5, button["rect"].y + 5))

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                button["action"]()
