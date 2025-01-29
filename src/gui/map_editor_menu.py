from gui.base_gui import BaseGUI
from simulation.map import MAP_DIR
import pygame
import os

class MapEditorMenu(BaseGUI):
    """Meny för att välja kartstorlek."""
    def __init__(self, screen, change_page_callback):
        super().__init__(screen, change_page_callback)
        self.set_title("Map Editor")
        self.map_dir = MAP_DIR
        self.add_option("10x10", lambda: self.start_editor(10, 10))
        self.add_option("20x20", lambda: self.start_editor(20, 20))
        self.add_option("50x50", lambda: self.start_editor(50, 50))
        self.add_option("Ange storlek", self.custom_size_popup)
        self.add_option("Välj befintlig karta", self.open_map_selection)
        self.add_option("Back", lambda: self.change_page("main"))

    def start_editor(self, width, height, map_file=None):
        """Starta karteditorn med angiven storlek eller befintlig karta."""
        self.change_page("map_editor", width=width, height=height, map_file=map_file)

    def open_map_selection(self):
        """Öppnar en popup där användaren kan välja en befintlig karta att redigera."""
        self.run_scroll_popup()

    def run_scroll_popup(self):
        """Visar en scrollbar-popup med alla sparade kartor."""
        running = True
        font = pygame.font.Font(None, 32)
        popup_width = self.width - 100
        popup_height = self.height - 150
        popup_rect = pygame.Rect(50, 75, popup_width, popup_height)

        scroll_area_rect = popup_rect.inflate(-20, -20)
        scroll_speed = 20
        scroll_offset = 0
        map_files = [f for f in os.listdir(self.map_dir) if f.endswith(".txt")]

        scroll_content = []
        y_offset = 0
        for map_file in map_files:
            rect = pygame.Rect(0, y_offset, scroll_area_rect.width, 50)
            scroll_content.append({"file": map_file, "rect": rect})
            y_offset += 60

        scroll_content_height = y_offset

        while running:
            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (50, 50, 50), popup_rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, 3, border_radius=10)

            clip_rect = popup_rect.inflate(-10, -10)
            original_clip = self.screen.get_clip()
            self.screen.set_clip(clip_rect)

            mouse_pos = pygame.mouse.get_pos()
            for content in scroll_content:
                rect = content["rect"].move(clip_rect.x, clip_rect.y - scroll_offset)

                if rect.collidepoint(mouse_pos):
                    row_color = (80, 80, 80)
                else:
                    row_color = (30, 30, 30)

                pygame.draw.rect(self.screen, row_color, rect)
                text_surface = font.render(content["file"], True, (255, 255, 255))
                self.screen.blit(text_surface, (rect.x + 10, rect.y + 10))

            self.screen.set_clip(original_clip)

            close_button_rect = pygame.Rect(popup_rect.right - 60, popup_rect.top + 10, 50, 30)
            pygame.draw.rect(self.screen, (200, 0, 0), close_button_rect, border_radius=5)
            close_text = pygame.font.Font(None, 24).render("Close", True, (255, 255, 255))
            self.screen.blit(close_text, close_button_rect.move(10, 5))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEWHEEL:
                    scroll_offset += event.y * scroll_speed
                    max_offset = max(0, scroll_content_height - scroll_area_rect.height)
                    scroll_offset = max(0, min(scroll_offset, max_offset))
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if close_button_rect.collidepoint(mouse_pos):
                        running = False
                    for content in scroll_content:
                        rect = content["rect"].move(clip_rect.x, clip_rect.y - scroll_offset)
                        if rect.collidepoint(mouse_pos):
                            self.start_editor(None, None, map_file=content["file"])
                            return

    def custom_size_popup(self):
        """Popup för att ange egen kartstorlek."""
        running = True
        input_box_width = pygame.Rect(self.width // 2 - 100, self.height // 2 - 60, 200, 40)
        input_box_height = pygame.Rect(self.width // 2 - 100, self.height // 2 + 10, 200, 40)

        color_inactive = (150, 150, 150)
        color_active = (0, 255, 0)
        color_width = color_inactive
        color_height = color_inactive

        active_width = False
        active_height = False
        width_text = ""
        height_text = ""

        font = pygame.font.Font(None, 32)
        error_message = "" 

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box_width.collidepoint(event.pos):
                        active_width = True
                        active_height = False
                    elif input_box_height.collidepoint(event.pos):
                        active_height = True
                        active_width = False
                    else:
                        active_width = False
                        active_height = False

                    color_width = color_active if active_width else color_inactive
                    color_height = color_active if active_height else color_inactive

                elif event.type == pygame.KEYDOWN:
                    if active_width:
                        if event.key == pygame.K_BACKSPACE:
                            width_text = width_text[:-1]
                        else:
                            width_text += event.unicode

                    elif active_height:
                        if event.key == pygame.K_BACKSPACE:
                            height_text = height_text[:-1]
                        else:
                            height_text += event.unicode

            self.screen.fill((30, 30, 30))
            pygame.draw.rect(self.screen, (50, 50, 50), (self.width // 2 - 150, self.height // 2 - 100, 300, 250))

            title_surface = font.render("Ange storlek (max 200x200):", True, (255, 255, 255))
            self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, self.height // 2 - 140))

            pygame.draw.rect(self.screen, color_width, input_box_width, 2)
            pygame.draw.rect(self.screen, color_height, input_box_height, 2)

            width_surface = font.render(width_text, True, (255, 255, 255))
            height_surface = font.render(height_text, True, (255, 255, 255))
            self.screen.blit(width_surface, (input_box_width.x + 5, input_box_width.y + 5))
            self.screen.blit(height_surface, (input_box_height.x + 5, input_box_height.y + 5))

            save_button = pygame.Rect(self.width // 2 - 50, self.height // 2 + 80, 100, 40)
            pygame.draw.rect(self.screen, (0, 200, 0), save_button)
            save_surface = font.render("Spara", True, (255, 255, 255))
            self.screen.blit(save_surface, (save_button.x + 20, save_button.y + 5))

            if error_message:
                error_surface = font.render(error_message, True, (255, 0, 0))
                self.screen.blit(error_surface, (self.width // 2 - error_surface.get_width() // 2, self.height // 2 + 130))

            pygame.display.flip()

            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and save_button.collidepoint(mouse_pos):
                try:
                    width = int(width_text.strip())
                    height = int(height_text.strip())
                    if 1 <= width <= 200 and 1 <= height <= 200:
                        self.start_editor(width, height)
                        return
                    else:
                        error_message = "Storleken måste vara mellan 1 och 200!"
                except ValueError:
                    error_message = "Ogiltiga värden! Ange siffror."
