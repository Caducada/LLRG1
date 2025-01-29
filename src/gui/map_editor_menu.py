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

        # 🛑 Gör "Close"-knappen större och lättare att klicka
        close_button_rect = pygame.Rect(popup_rect.right - 90, popup_rect.top + 10, 80, 40)

        while running:
            self.screen.fill((0, 0, 0))

            # Rita popup-fönstret
            pygame.draw.rect(self.screen, (50, 50, 50), popup_rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, 3, border_radius=10)

            clip_rect = popup_rect.inflate(-10, -10)
            original_clip = self.screen.get_clip()
            self.screen.set_clip(clip_rect)

            mouse_pos = pygame.mouse.get_pos()

            # Rita listan med kartor
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

            # 🛑 LÄGG TILL HOVER-EFFEKT PÅ "CLOSE"-KNAPPEN 🛑
            if close_button_rect.collidepoint(mouse_pos):
                close_color = (255, 50, 50)  # Ljusare röd vid hover
            else:
                close_color = (200, 0, 0)   # Standardfärg

            # Rita "Close"-knappen **SIST** så att den hamnar överst
            pygame.draw.rect(self.screen, close_color, close_button_rect, border_radius=5)
            close_text = pygame.font.Font(None, 28).render("Close", True, (255, 255, 255))
            self.screen.blit(close_text, (close_button_rect.x + 15, close_button_rect.y + 10))

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
                    # 🛑 Prioritera "Close"-knappen först 🛑
                    if close_button_rect.collidepoint(mouse_pos):
                        running = False
                        break  # Avsluta loopen direkt

                    # Hantera kartval om "Close" **inte** klickades
                    for content in scroll_content:
                        rect = content["rect"].move(clip_rect.x, clip_rect.y - scroll_offset)
                        if rect.collidepoint(mouse_pos):
                            self.start_editor(None, None, map_file=content["file"])
                            return

    def custom_size_popup(self):
        """Popup för att ange egen kartstorlek."""
        running = True
        font = pygame.font.Font(None, 32)

        input_box_width = pygame.Rect(self.width // 2 - 100, self.height // 2 - 50, 200, 40)
        input_box_height = pygame.Rect(self.width // 2 - 100, self.height // 2 + 10, 200, 40)

        color_inactive = (150, 150, 150)
        color_active = (0, 255, 0)
        color_width = color_inactive
        color_height = color_inactive

        active_width = False
        active_height = False
        width_text = ""
        height_text = ""
        error_message = ""
        user_interacted = False 

        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    user_interacted = True  
                    if input_box_width.collidepoint(event.pos):
                        active_width = True
                        active_height = False
                    elif input_box_height.collidepoint(event.pos):
                        active_height = True
                        active_width = False
                    elif back_button.collidepoint(event.pos):
                        self.change_page('main')
                        return
                    else:
                        active_width = False
                        active_height = False

                    color_width = color_active if active_width else color_inactive
                    color_height = color_active if active_height else color_inactive

                elif event.type == pygame.KEYDOWN:
                    user_interacted = True 
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

            popup_rect = pygame.Rect(self.width // 4, self.height // 4, self.width // 2, self.height // 2)
            pygame.draw.rect(self.screen, (50, 50, 50), popup_rect, border_radius=10)

            title_surface = font.render("Ange storlek (max 200x200):", True, (255, 255, 255))
            self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, popup_rect.top + 20))

            box_hover_color = (180, 180, 180)
            current_color_width = color_width if not input_box_width.collidepoint(mouse_pos) else box_hover_color
            current_color_height = color_height if not input_box_height.collidepoint(mouse_pos) else box_hover_color

            pygame.draw.rect(self.screen, current_color_width, input_box_width, 2)
            pygame.draw.rect(self.screen, current_color_height, input_box_height, 2)

            width_display_text = width_text if width_text else "xxx"
            height_display_text = height_text if height_text else "yyy"

            width_surface = font.render(width_display_text, True, (255, 255, 255) if width_text else (100, 100, 100))
            height_surface = font.render(height_display_text, True, (255, 255, 255) if height_text else (100, 100, 100))

            self.screen.blit(width_surface, (input_box_width.x + 5, input_box_width.y + 10))
            self.screen.blit(height_surface, (input_box_height.x + 5, input_box_height.y + 10))

            save_button = pygame.Rect(self.width // 2 - 110, self.height // 2 + 80, 100, 40)
            back_button = pygame.Rect(self.width // 2 + 10, self.height // 2 + 80, 100, 40)

            save_color = (0, 200, 0) if not save_button.collidepoint(mouse_pos) else (0, 255, 0)
            back_color = (200, 0, 0) if not back_button.collidepoint(mouse_pos) else (255, 50, 50)

            pygame.draw.rect(self.screen, save_color, save_button, border_radius=5)
            pygame.draw.rect(self.screen, back_color, back_button, border_radius=5)

            save_surface = font.render("Spara", True, (255, 255, 255))
            back_surface = font.render("Tillbaka", True, (255, 255, 255))
            self.screen.blit(save_surface, (save_button.x + 20, save_button.y + 10))
            self.screen.blit(back_surface, (back_button.x + 10, back_button.y + 10))

            if user_interacted and error_message:
                error_surface = font.render(error_message, True, (255, 0, 0))
                self.screen.blit(error_surface, (self.width // 2 - error_surface.get_width() // 2, self.height // 2 + 130))

            pygame.display.flip()

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


