import pygame
from gui.base_gui import BaseGUI
from gui.sidebar import Sidebar
from simulation.map import Map
from gui.graphics import GraphicsLibrary


class MapEditor(BaseGUI):
    """Karteditor med stöd för att skapa och redigera kartor."""
    def __init__(self, screen, change_page_callback):
        super().__init__(screen, change_page_callback)
        self.set_title("Map Editor")
        self.sidebar_width = 200
        self.cell_size = 20
        self.map_obj = None
        self.selected_value = "0"
        self.graphics = GraphicsLibrary()

        # Sidopanel
        self.sidebar = Sidebar(self.screen, self.sidebar_width)
        self.init_sidebar()

    def init_sidebar(self):
        """Initiera sidopanelens knappar."""
        self.sidebar.add_button("Wall (x)", lambda: self.set_selected_value("x"), self.graphics.get_resource("x")["color"])
        self.sidebar.add_button("Mine (B)", lambda: self.set_selected_value("B"), self.graphics.get_resource("B")["color"])
        self.sidebar.add_button("Empty (0)", lambda: self.set_selected_value("0"), self.graphics.get_resource("0")["color"])
        self.sidebar.add_button("Save Map", self.save_map, (200, 200, 200))
        self.sidebar.add_button("Main Menu", lambda: self.change_page("main"), (200, 200, 200))

    def set_selected_value(self, value):
        """Ställ in det valda värdet för redigering."""
        self.selected_value = value

    def save_map(self):
        """Spara kartan till en fil."""
        if self.map_obj:
            self.map_obj.save_map_to_file("underground.txt")
            print("Map saved to underground.txt.")
        else:
            print("No map to save.")

    def ask_map_size(self):
        """Visa en meny för att välja kartans storlek."""
        font = pygame.font.Font(None, 36)
        size_buttons = [
            {"rect": pygame.Rect(250, 200, 200, 50), "text": "10x10", "size": (10, 10)},
            {"rect": pygame.Rect(250, 300, 200, 50), "text": "20x20", "size": (20, 20)},
            {"rect": pygame.Rect(250, 400, 200, 50), "text": "50x50", "size": (50, 50)},
        ]

        while not self.map_obj:
            self.screen.fill(self.background_color)

            for button in size_buttons:
                pygame.draw.rect(self.screen, (150, 150, 150), button["rect"])
                pygame.draw.rect(self.screen, (0, 0, 0), button["rect"], 2)
                text = font.render(button["text"], True, (255, 255, 255))
                self.screen.blit(text, (button["rect"].x + 50, button["rect"].y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in size_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            self.map_obj = Map()
                            self.map_obj.create_empty_map(*button["size"])
                            return

    def handle_events(self):
        """Hantera events som mus- och tangentbordsinmatning."""
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                self.sidebar.handle_hover(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_pos[0] < self.sidebar_width:  # Klick på sidopanel
                    self.sidebar.handle_click(mouse_pos)
                else:  # Klick på kartan
                    cell_coords = self.get_cell_under_mouse()
                    if cell_coords:
                        cell_x, cell_y = cell_coords
                        self.map_obj.modify_cell(cell_x, cell_y, self.selected_value)

    def update(self):
        """Uppdatera tillstånd."""
        pass  # Placeholder för framtida uppdateringar

    def render(self):
        """Rendera kartan och sidopanelen."""
        if not self.map_obj:
            self.ask_map_size()
        self.calculate_cell_size()
        self.screen.fill(self.background_color)
        self.sidebar.render()
        self.draw_map()

    def calculate_cell_size(self):
        """Beräkna cellstorlek för att kartan ska fylla utrymmet."""
        if not self.map_obj or not self.map_obj._map:
            return
        map_width = len(self.map_obj._map[0])
        map_height = len(self.map_obj._map)
        available_width = self.screen.get_width() - self.sidebar_width
        available_height = self.screen.get_height()
        self.cell_size = min(available_width // map_width, available_height // map_height)

    def draw_map(self):
        """Rita kartan på skärmen."""
        font = pygame.font.Font(None, self.cell_size - 4)
        for y, row in enumerate(self.map_obj._map):
            for x, cell in enumerate(row):
                cell_x = self.sidebar_width + x * self.cell_size
                cell_y = y * self.cell_size
                resource = self.graphics.get_resource("map", cell)
                color = resource["color"]
                symbol = resource["symbol"]
                if color:
                    pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))
                if symbol:
                    text = font.render(symbol, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                    self.screen.blit(text, text_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), (cell_x, cell_y, self.cell_size, self.cell_size), 1)

    def get_cell_under_mouse(self):
        """Hämta vilken cell musen pekar på."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < self.sidebar_width:
            return None
        cell_x = (mouse_x - self.sidebar_width) // self.cell_size
        cell_y = mouse_y // self.cell_size
        if 0 <= cell_y < len(self.map_obj._map) and 0 <= cell_x < len(self.map_obj._map[0]):
            return cell_x, cell_y
        return None
