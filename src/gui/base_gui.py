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
        self.title_font = pygame.font.Font(None, self.get_dynamic_font_size(10))
        self.option_font = pygame.font.Font(None, self.get_dynamic_font_size(14))
        self.min_width = 640
        self.min_height = 450
        self.scroll_offset = 0 
        self.scroll_speed = 30 

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

    def get_dynamic_font_size(self, percentage):
        """Beräkna dynamisk teckenstorlek baserat på fönsterhöjd."""
        return max(20, int(self.height * percentage / 100))

    def render(self):
        """Rendera sidans titel och alternativ."""
        self.screen.fill(self.graphics.get_resource("gui", "background")["color"])
        self.draw_title()
        self.draw_options()

    def draw_title(self):
        """Ritar sidans titel."""
        self.title_font = pygame.font.Font(None, self.get_dynamic_font_size(10))
        text = self.title_font.render(self.title, True, self.graphics.get_resource("gui", "title")["color"])
        text_rect = text.get_rect(center=(self.width // 2, self.height // 8))
        self.screen.blit(text, text_rect)

    def draw_options(self):
        """Ritar alla alternativ dynamiskt och justerar storlek om det finns för många."""
        max_buttons = 4  
        total_buttons = len(self.options)

        if total_buttons > max_buttons:
            button_height = self.height // (total_buttons + 4) 
        else:
            button_height = self.height // 8 

        button_width = self.width // 2
        center_x = self.width // 2
        start_y = self.height // 4  
        spacing = 10  

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

            text_size = max(20, int(button_height * 0.5))  
            text_font = pygame.font.Font(None, text_size)

            text_color = (255, 255, 255)
            text = text_font.render(option["text"], True, text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def handle_resize(self, new_size):
        """Hanterar fönsterstorleksändring med minimistorlekskontroll."""
        new_width, new_height = new_size
        if new_width < self.min_width:
            new_width = self.min_width
        if new_height < self.min_height:
            new_height = self.min_height

        self.width, self.height = new_width, new_height
        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        self.title_font = pygame.font.Font(None, self.get_dynamic_font_size(10))
        self.option_font = pygame.font.Font(None, self.get_dynamic_font_size(14))

    def handle_events(self):
        """Hantera input och scroll."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    action = self.options[self.selected_index].get("action")
                    if action:
                        action()
            elif event.type == pygame.MOUSEWHEEL:  
                self.scroll_offset += event.y * self.scroll_speed
                max_scroll = max(0, len(self.options) * (self.height // 4 + 10) - self.height // 2)
                self.scroll_offset = max(-max_scroll, min(0, self.scroll_offset))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for option in self.options:
                    rect = option.get("rect")
                    if rect and rect.collidepoint(mouse_pos):
                        action = option.get("action")
                        if action:
                            action()

    def exit_app(self):
        """Avsluta applikationen."""
        pygame.quit()
        exit()

    def run(self):
        """Huvudloopen för en sida."""
        self.handle_resize(self.screen.get_size())
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.render()
            pygame.display.flip()
            clock.tick(60)
