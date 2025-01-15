import pygame
import random
from gui.base_gui import BaseGUI

class MainMenu(BaseGUI):
    """Huvudmeny med navigering för Simulation, Map Editor och Exit."""
    def __init__(self, screen, on_option_selected):
        super().__init__(screen)
        self.options = ["Simulation", "Map Editor", "Exit"]
        self.selected_index = 0
        self.on_option_selected = on_option_selected

        self.title_font = pygame.font.Font(None, 80)  
        self.title_text = "Lindas Lustfyllda Rederi"

        self.width, self.height = screen.get_size()

    def render(self):
        """Ritar huvudmenyn med Matrix-effekt och text."""
        self.screen.fill((0, 0, 0)) 
        self.draw_title()
        self.draw_menu_buttons()

    def draw_title(self):
        """Ritar rubriken 'Lindas Lustfyllda Rederi'."""
        text = self.title_font.render(self.title_text, True, (0, 255, 0))  
        text_rect = text.get_rect(center=(self.width // 2, self.height // 6)) 
        self.screen.blit(text, text_rect)

    def draw_menu_buttons(self):
        """Ritar menyknappar med gröna färger och highlight-effekter."""
        font = pygame.font.Font(None, 50)
        button_width = self.width // 3
        button_height = self.height // 12
        center_x = self.width // 2
        start_y = self.height // 2

        mouse_x, mouse_y = pygame.mouse.get_pos() 

        for i, option in enumerate(self.options):
            x = center_x - button_width // 2
            y = start_y + i * (button_height + 20)
            rect = pygame.Rect(x, y, button_width, button_height)

            # Kontrollera om musen är över knappen
            if rect.collidepoint(mouse_x, mouse_y):
                button_color = (100, 255, 100)  
                self.selected_index = i  
            elif i == self.selected_index:
                button_color = (50, 255, 50) 
            else:
                button_color = (0, 100 + i * 30, 0) 

            pygame.draw.rect(self.screen, button_color, rect, border_radius=10)

            pygame.draw.rect(self.screen, (0, 255, 0), rect, 3, border_radius=10)

            text_color = (255, 255, 255) if i == self.selected_index else (200, 255, 200)
            text = font.render(option, True, text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def handle_events(self):
        """Hantera input för menyval."""
        mouse_x, mouse_y = pygame.mouse.get_pos()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:  
                self.width, self.height = event.size
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                self.matrix_columns = [0] * (self.width // 10)  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:  
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN: 
                    if self.options[self.selected_index] == "Exit":
                        pygame.quit()
                        exit()
                    self.on_option_selected(self.selected_index)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    button_width = self.width // 3
                    button_height = self.height // 12
                    center_x = self.width // 2
                    start_y = self.height // 2

                    for i, option in enumerate(self.options):
                        x = center_x - button_width // 2
                        y = start_y + i * (button_height + 20)
                        rect = pygame.Rect(x, y, button_width, button_height)
                        if rect.collidepoint(mouse_x, mouse_y):
                            if option == "Exit":
                                pygame.quit()
                                exit()
                            self.on_option_selected(i)
