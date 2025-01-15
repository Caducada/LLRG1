import pygame
import os
from gui.base_gui import BaseGUI
from gui.graphics import GraphicsLibrary
from simulation.map import Map
from simulation.map import MAP_DIR


class SimulationMenu(BaseGUI):
    def __init__(self, screen, change_page_callback):
        super().__init__(screen, change_page_callback)
        self.set_title("Välj en karta för simulering")
        self.map_dir = MAP_DIR
        self.graphics = GraphicsLibrary()
        self.map_files = self.load_map_files()
        self.map_thumbnails = {}
        self.thumbnail_size = (100, 100)
        self.load_thumbnails()

        # Scroll setup
        self.scroll_offset = 0
        self.scroll_speed = 20
        self.scroll_area_rect = None  # Dynamically set in render
        self.scroll_content_height = 0
        self.load_scroll_content()

    def load_map_files(self):
        """Ladda alla giltiga kartfiler från map_dir."""
        try:
            files = [f for f in os.listdir(self.map_dir) if f.endswith('.txt')]
            valid_files = []
            for file in files:
                temp_map = Map(file_name=os.path.join(self.map_dir, file))
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

            self.map_thumbnails[map_file] = self.generate_map_thumbnail(temp_map._map)

    def generate_map_thumbnail(self, map_data):
        """Generera en miniatyrbild för en karta."""
        if not map_data or not map_data[0]:
            print("Invalid or empty map data provided for thumbnail.")
            return pygame.Surface(self.thumbnail_size)

        cell_width = self.thumbnail_size[0] // len(map_data[0])
        cell_height = self.thumbnail_size[1] // len(map_data)
        cell_size = min(cell_width, cell_height)

        thumbnail = pygame.Surface(self.thumbnail_size)
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                color = self.graphics.get_resource("map", cell)["color"]
                if color:
                    pygame.draw.rect(thumbnail, color, (x * cell_size, y * cell_size, cell_size, cell_size))
        return thumbnail

    def load_scroll_content(self):
        """Generera innehåll för scroll-sektionen."""
        self.scroll_content = []
        y_offset = 0

        for map_file in self.map_files:
            thumbnail = self.map_thumbnails.get(map_file)
            if thumbnail:
                map_path = os.path.join(self.map_dir, map_file)
                temp_map = Map(file_name=map_path)
                map_size_text = f"{len(temp_map._map)}x{len(temp_map._map[0])}"

                rect = pygame.Rect(0, y_offset, 0, 150)  # Width dynamically set in render
                self.scroll_content.append({
                    "file": map_file,
                    "thumbnail": thumbnail,
                    "size_text": map_size_text,
                    "rect": rect
                })
                y_offset += 160  # Spacing between items

        self.scroll_content_height = y_offset

    def handle_scroll_events(self, event):
        """Hantera scrollhändelser."""
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset += event.y * self.scroll_speed
            max_offset = max(0, self.scroll_content_height - self.scroll_area_rect.height)
            self.scroll_offset = max(0, min(self.scroll_offset, max_offset))

    def render(self):
        """Rendera menyn."""
        self.screen.fill(self.graphics.get_resource("gui", "background")["color"])
        self.draw_title()

        # Calculate dynamic scroll area
        self.scroll_area_rect = pygame.Rect(50, 100, self.width - 100, self.height - 200)

        # Scroll area rendering
        self.render_scroll_area()

        # Back button rendering
        self.render_back_button()

    def render_scroll_area(self):
        """Rendera scroll-sektionen."""
        pygame.draw.rect(self.screen, (30, 30, 30), self.scroll_area_rect)
        clip_rect = self.scroll_area_rect.inflate(-10, -10)
        original_clip = self.screen.get_clip()
        self.screen.set_clip(clip_rect)

        for content in self.scroll_content:
            rect = content["rect"].move(self.scroll_area_rect.x, self.scroll_area_rect.y - self.scroll_offset)
            rect.width = self.scroll_area_rect.width  # Update width dynamically
            if clip_rect.colliderect(rect):
                # Rendera rad
                button_color = self.graphics.get_resource("gui", "button")["color"]
                pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
                pygame.draw.rect(self.screen, self.graphics.get_resource("gui", "border")["color"], rect, 3, border_radius=10)

                # Thumbnail centrerad
                thumb_x = rect.x + 20
                thumb_y = rect.y + (rect.height - self.thumbnail_size[1]) // 2
                self.screen.blit(content["thumbnail"], (thumb_x, thumb_y))

                # Storlekstext
                font = pygame.font.Font(None, 36)
                size_surface = font.render(content["size_text"], True, (255, 255, 255))
                self.screen.blit(size_surface, (thumb_x + 120, thumb_y + 30))

        self.screen.set_clip(original_clip)

    def render_back_button(self):
        """Rendera tillbaka-knappen."""
        button_rect = pygame.Rect(50, self.height - 80, self.width - 100, 50)
        button_color = self.graphics.get_resource("gui", "button")["color"]
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.graphics.get_resource("gui", "border")["color"], button_rect, 3, border_radius=10)

        font = pygame.font.Font(None, 36)
        text_surface = font.render("Back", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        self.back_button_rect = button_rect

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
                if self.back_button_rect.collidepoint(mouse_pos):
                    self.change_page("main")
                for content in self.scroll_content:
                    rect = content["rect"].move(self.scroll_area_rect.x, self.scroll_area_rect.y - self.scroll_offset)
                    if rect.collidepoint(mouse_pos):
                        self.start_simulation(content["file"])
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.size)

    def handle_resize(self, new_size):
        """Hanterar storleksändringar och uppdaterar layouten."""
        super().handle_resize(new_size)
        self.scroll_area_rect = pygame.Rect(50, 100, self.width - 100, self.height - 200)
        self.load_scroll_content()  

    def start_simulation(self, map_file):
        """Starta simuleringen med vald karta."""
        print("Started simulating **TEST PRINT**")

