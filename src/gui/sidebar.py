import pygame
from gui.base_gui import BaseGUI


class Sidebar(BaseGUI):
    def __init__(self, screen, width):
        self.screen = screen
        self.width = width
        self.buttons = []
        self.hovered_button = None  

    def add_button(self, text, action, color=(150, 150, 150)):
        """Add a button to the sidebar."""
        button_rect = pygame.Rect(10, 10 + len(self.buttons) * 40, self.width - 20, 30)
        self.buttons.append({"rect": button_rect, "text": text, "action": action, "color": color})

    def render(self):
        """Render the sidebar and its buttons."""
        pygame.draw.rect(self.screen, (220, 220, 220), (0, 0, self.width, self.screen.get_height()))
        font = pygame.font.Font(None, 24)

        for button in self.buttons:
            # Highlight the hovered button
            if button == self.hovered_button:
                button_color = (255, 255, 150) 
            else:
                button_color = button["color"]

            # Draw button background
            pygame.draw.rect(self.screen, button_color, button["rect"], border_radius=5)

            # Draw button border
            pygame.draw.rect(self.screen, (0, 0, 0), button["rect"], 2, border_radius=5)

            # Draw button text
            text = font.render(button["text"], True, (0, 0, 0))
            self.screen.blit(text, (button["rect"].x + 5, button["rect"].y + 5))

    def handle_hover(self, mouse_pos):
        """Handle hover effects for the buttons."""
        self.hovered_button = None  # Reset hovered button
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                self.hovered_button = button
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Change cursor to hand
                return
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Default cursor

    def handle_click(self, mouse_pos):
        """Handle button clicks."""
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                button["action"]()
