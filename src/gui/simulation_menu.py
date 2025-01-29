import pygame
import os
from gui.base_gui import BaseGUI
from gui.graphics import GraphicsLibrary
from simulation.map import Map
from simulation.map import MAP_DIR, SUB_DIR
import random

class SimulationMenu(BaseGUI):
    def __init__(self, screen, change_page_callback):
        super().__init__(screen, change_page_callback)
        self.set_title("Välj en karta för simulering")
        self.map_dir = MAP_DIR
        self.sub_dir = SUB_DIR
        self.graphics = GraphicsLibrary()
        self.map_files = self.load_map_files()
        self.map_thumbnails = {}
        self.thumbnail_size = (100, 100)
        self.load_thumbnails()

        # Lägg till menyalternativ
        self.add_option("Run default sim", self.run_default_sim)
        self.add_option("List maps", self.show_map_list)
        self.add_option("Choose file", self.choose_file)
        self.add_option("Back", lambda: self.change_page("main"))

        # Scroll-sektion (för list maps)
        self.scroll_offset = 0
        self.scroll_speed = 20
        self.scroll_area_rect = None
        self.scroll_content_height = 0
        self.scroll_content = []

    def load_map_files(self):
        """Ladda alla giltiga kartfiler från map_dir."""
        try:
            files = [f for f in os.listdir(self.map_dir) if f.endswith('.txt')]
            valid_files = []
            for file in files:
                map_path = os.path.join(self.map_dir, file)
                temp_map = Map(file_name=map_path)
                if temp_map._map and temp_map._map[0]:
                    valid_files.append(file)
                else:
                    print(f"Skipping invalid or empty map: {file}")
            return valid_files
        except FileNotFoundError:
            print(f"Kartmappen '{self.map_dir}' hittades inte.")
            return []

    def load_thumbnails(self):
        """Ladda miniatyrbilder för varje karta."""
        for map_file in self.map_files:
            map_path = os.path.join(self.map_dir, map_file)
            temp_map = Map(file_name=map_path)

            if not temp_map._map or not temp_map._map[0]:
                print(f"Skipping empty or invalid map: {map_file}")
                continue

            thumbnail = self.generate_map_thumbnail(temp_map._map)
            self.map_thumbnails[map_file] = thumbnail

    def generate_map_thumbnail(self, map_data):
        """Generera en miniatyrbild för en karta."""
        if not map_data or not map_data[0]:
            print("Invalid or empty map data provided for thumbnail.")
            return pygame.Surface(self.thumbnail_size)

        # Beräkna cellstorlekar baserat på kartans dimensioner
        rows, cols = len(map_data), len(map_data[0])
        cell_width = self.thumbnail_size[0] // cols
        cell_height = self.thumbnail_size[1] // rows
        cell_size = min(cell_width, cell_height)

        thumbnail = pygame.Surface(self.thumbnail_size)
        thumbnail.fill((0, 0, 0))  # Bakgrundsfärg

        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                resource = self.graphics.get_resource("map", cell)
                color = resource["color"]

                if cell in range(1, 10):
                    color = (0, 255, 0)  

                if color:
                    pygame.draw.rect(
                        thumbnail,
                        color,
                        (x * cell_size, y * cell_size, cell_size, cell_size)
                    )
        return thumbnail
    
    def run_default_sim(self):
        """Kör simuleringen med underground.txt."""
        default_map = "underground.txt"
        print(self.map_files)
        if default_map in self.map_files:
            self.start_simulation(default_map)
        else:
            print(f"Default map '{default_map}' not found.")

    def show_map_list(self):
        """Visa en lista med alla kartor i scrollområdet."""
        self.load_scroll_content()
        self.run_scroll_popup()

    # TODO: IMPLEMENTERA FILVÄLJARE
    def choose_file(self):
        """Låt användaren välja en fil manuellt."""
        print("Opening file chooser...")
        # Här kan vi implementera en filväljare eller liknande funktionalitet.
        # För nuvarande simulerar vi ett val:
        # chosen_file = "custom_map.txt"
        # self.start_simulation(chosen_file)

    def load_scroll_content(self):
        """Generera innehåll för scroll-sektionen."""
        self.scroll_content = []
        y_offset = 0

        for map_file in self.map_files:
            thumbnail = self.map_thumbnails.get(map_file)
            if thumbnail:
                map_path = os.path.join(self.map_dir, map_file)
                temp_map = Map(file_name=map_path)

                # Beräkna storlek baserat på kartans dimensioner
                map_rows = len(temp_map._map)
                map_cols = len(temp_map._map[0])
                map_size_text = f"{map_rows}x{map_cols}"

                rect = pygame.Rect(0, y_offset, 0, 150)  
                self.scroll_content.append({
                    "file": map_file,
                    "thumbnail": thumbnail,
                    "size_text": map_size_text,
                    "rect": rect
                })
                y_offset += 160  

        self.scroll_content_height = y_offset

    def handle_scroll_events(self, event):
        """Hantera scrollhändelser."""
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset += event.y * self.scroll_speed
            max_offset = max(0, self.scroll_content_height - self.scroll_area_rect.height)
            self.scroll_offset = max(0, min(self.scroll_offset, max_offset))

    def run_scroll_popup(self):
        """Kör popup-loopen med kartlistan och låt användaren välja ubåtsdata."""
        running = True

        # Definiera popupens område
        popup_width = self.width - 100
        popup_height = self.height - 150
        popup_rect = pygame.Rect(50, 75, popup_width, popup_height)

        # Sätt scroll_area_rect för att hantera scroll
        self.scroll_area_rect = popup_rect.inflate(-10, -10)

        # Sätt korrekt bredd på rektanglarna
        for content in self.scroll_content:
            content["rect"].width = self.scroll_area_rect.width

        while running:
            self.screen.fill((0, 0, 0))  # Svart bakgrund

            # Rendera popup-bakgrund
            pygame.draw.rect(self.screen, (50, 50, 50), popup_rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, 3, border_radius=10)

            clip_rect = popup_rect.inflate(-10, -10)
            original_clip = self.screen.get_clip()
            self.screen.set_clip(clip_rect)

            mouse_pos = pygame.mouse.get_pos()
            for content in self.scroll_content:
                rect = content["rect"].move(clip_rect.x, clip_rect.y - self.scroll_offset)
                rect.width = clip_rect.width

                if rect.collidepoint(mouse_pos):
                    row_color = (80, 80, 80)
                else:
                    row_color = (30, 30, 30)

                pygame.draw.rect(self.screen, row_color, rect)

                self.screen.blit(content["thumbnail"], (rect.x + 20, rect.y + 20))

                font = pygame.font.Font(None, 36)
                name_surface = font.render(content["file"], True, (255, 255, 255))
                size_surface = font.render(content["size_text"], True, (255, 255, 255))
                self.screen.blit(name_surface, (rect.x + 150, rect.y + 10))
                self.screen.blit(size_surface, (rect.x + 150, rect.y + 50))

            self.screen.set_clip(original_clip)

            # Rendera "Stäng"-knappen
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
                    self.handle_scroll_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    for content in self.scroll_content:
                        rect = content["rect"].move(clip_rect.x, clip_rect.y - self.scroll_offset)
                        rect.width = clip_rect.width
                        if rect.collidepoint(mouse_pos):
                            self.change_page("submarine_selection", map_file=content["file"])
                            return

                    # Klick på stäng-knappen
                    if close_button_rect.collidepoint(mouse_pos):
                        running = False

    # def choose_fleet_popup(self, map_file):
    #     """Popup för att välja ubåtsdata."""
    #     running = True
    #     font = pygame.font.Font(None, 32)

    #     input_box = pygame.Rect(self.width // 2 - 100, self.height // 2 + 40, 200, 40)
    #     color_inactive = (150, 150, 150)
    #     color_active = (0, 255, 0)
    #     input_color = color_inactive
    #     active_input = False
    #     num_submarines_text = ""
    #     error_message = ""

    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 exit()
    #             elif event.type == pygame.MOUSEBUTTONDOWN:
    #                 if input_box.collidepoint(event.pos):
    #                     active_input = True
    #                 else:
    #                     active_input = False
    #                 input_color = color_active if active_input else color_inactive

    #                 # Kolla knappar
    #                 if default_button.collidepoint(event.pos):
    #                     self.change_page("simulation", map_file=map_file, fleet_file="uboat.txt")
    #                     return
    #                 elif random_button.collidepoint(event.pos):
    #                     error_message = ""
    #                     active_input = True

    #             elif event.type == pygame.KEYDOWN and active_input:
    #                 if event.key == pygame.K_RETURN:
    #                     try:
    #                         num_submarines = int(num_submarines_text.strip())
    #                         if num_submarines <= 0:
    #                             error_message = "Antalet måste vara större än 0."
    #                         else:
    #                             self.generate_random_submarines(map_file, num_submarines)
    #                             self.change_page("simulation", map_file=map_file, fleet_file="random_dumb.txt")
    #                             return
    #                     except ValueError:
    #                         error_message = "Ogiltigt värde. Ange ett heltal."
    #                 elif event.key == pygame.K_BACKSPACE:
    #                     num_submarines_text = num_submarines_text[:-1]
    #                 else:
    #                     num_submarines_text += event.unicode

    #         # Rendera popup
    #         self.screen.fill((30, 30, 30))
    #         popup_rect = pygame.Rect(self.width // 2 - 150, self.height // 2 - 100, 300, 250)
    #         pygame.draw.rect(self.screen, (50, 50, 50), popup_rect)
    #         pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, 2)

    #         title_surface = font.render("Välj ubåtsdata", True, (255, 255, 255))
    #         self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, self.height // 2 - 90))

    #         default_button = pygame.Rect(self.width // 2 - 140, self.height // 2 - 40, 120, 40)
    #         random_button = pygame.Rect(self.width // 2 + 20, self.height // 2 - 40, 120, 40)
    #         pygame.draw.rect(self.screen, (0, 200, 0), default_button)
    #         pygame.draw.rect(self.screen, (0, 200, 0), random_button)

    #         default_surface = font.render("Default", True, (255, 255, 255))
    #         random_surface = font.render("Random", True, (255, 255, 255))
    #         self.screen.blit(default_surface, (default_button.x + 10, default_button.y + 5))
    #         self.screen.blit(random_surface, (random_button.x + 10, random_button.y + 5))

    #         # Input-fält
    #         pygame.draw.rect(self.screen, input_color, input_box, 2)
    #         input_text_surface = font.render(num_submarines_text, True, (255, 255, 255))
    #         self.screen.blit(input_text_surface, (input_box.x + 5, input_box.y + 5))

    #         # Felmeddelande
    #         if error_message:
    #             error_surface = font.render(error_message, True, (255, 0, 0))
    #             self.screen.blit(error_surface, (self.width // 2 - error_surface.get_width() // 2, self.height // 2 + 90))

    #         pygame.display.flip()

    def handle_events(self):
        """Hanterar event i menyn."""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEWHEEL:
                self.handle_scroll_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Klick på alternativ
                for option in self.options:
                    rect = option["rect"]
                    if rect and rect.collidepoint(mouse_pos):
                        action = option.get("action")
                        if action:
                            action()
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.size)


    def start_simulation(self, map_file):
        """Starta simuleringen med vald karta."""
        fleet_file = "uboat.txt" 
        self.change_page("simulation", map_file=map_file, fleet_file=fleet_file)
