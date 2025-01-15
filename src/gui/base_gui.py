import pygame
from gui.graphics import GraphicsLibrary

class BaseGUI:
    """Bas för alla GUI-komponenter."""
    def __init__(self, screen, change_page_callback):
        self.screen = screen
        self.change_page_callback = change_page_callback
        self.graphics = GraphicsLibrary()
        self.title = ""
        self.options = []
        self.selected_index = 0
        self.width, self.height = self.screen.get_size()
        self.title_font = pygame.font.Font(None, 80)
        self.option_font = pygame.font.Font(None, 50)

    def set_title(self, title):
        """Ställ in sidans titel."""
        self.title = title

    def add_option(self, text, action):
        """Lägg till ett alternativ."""
        self.options.append({"text": text, "action": action, "rect": None})

    def change_page(self, page_name, **kwargs):
        """Byt till en annan sida."""
        self.running = False  # Stoppa nuvarande sidans loop
        self.change_page_callback(page_name, **kwargs)

    def render(self):
        """Rendera sidans titel och alternativ."""
        self.screen.fill(self.graphics.get_resource("gui", "background")["color"])
        self.draw_title()
        self.draw_options()
    
    def exit_app(self):
        """Avsluta applikationen."""
        pygame.quit()
        exit()

    def draw_title(self):
        """Ritar sidans titel."""
        text = self.title_font.render(self.title, True, self.graphics.get_resource("gui", "title")["color"])
        text_rect = text.get_rect(center=(self.width // 2, self.height // 6))
        self.screen.blit(text, text_rect)

    def draw_options(self):
        """Ritar alla alternativ."""
        button_width = self.width // 3
        button_height = self.height // 12
        center_x = self.width // 2
        start_y = self.height // 2
        spacing = 20

        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(self.options):
            x = center_x - button_width // 2
            y = start_y + i * (button_height + spacing)
            rect = pygame.Rect(x, y, button_width, button_height)
            option["rect"] = rect 

            if rect.collidepoint(mouse_pos):
                button_color = self.graphics.get_resource("gui", "hover")["color"]
                self.selected_index = i
            else:
                button_color = self.graphics.get_resource("gui", "button")["color"]

            pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
            pygame.draw.rect(self.screen, self.graphics.get_resource("gui", "border")["color"], rect, 3, border_radius=10)

            text_color = (255, 255, 255)
            text = self.option_font.render(option["text"], True, text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def handle_events(self):
        """Hantera input för sidans alternativ."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Avsluta sidans loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    action = self.options[self.selected_index].get("action")
                    if action:
                        action()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for option in self.options:
                    rect = option.get("rect")
                    if rect and rect.collidepoint(mouse_pos):
                        action = option.get("action")
                        if action:
                            action()

    def run(self):
        """Huvudloopen för en sida."""
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.render()
            pygame.display.flip()
            clock.tick(60)
