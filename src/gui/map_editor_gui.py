import pygame
from gui.base_gui import BaseGUI
from gui.sidebar import Sidebar
from simulation.map import Map
from gui.graphics import GraphicsLibrary


class MapEditor(BaseGUI):
    """Karteditor med stöd för att skapa och redigera kartor."""
    def __init__(self, screen, change_page_callback, width=10, height=10):
        super().__init__(screen, change_page_callback)
        self.set_title("Map Editor")
        self.cell_size = 20
        self.map_obj = Map()
        self.map_obj.create_empty_map(width, height)
        self.selected_value = "0"
        self.graphics = GraphicsLibrary()
        self.sidebar_buttons = [] 
        self.init_sidebar()
        self.calculate_cell_size()

    def init_sidebar(self):
        """Initiera sidopanelens knappar."""
        self.add_sidebar_button("Wall (x)", lambda: self.set_selected_value("x"), self.graphics.get_resource("map", "x")["color"])
        self.add_sidebar_button("Mine (B)", lambda: self.set_selected_value("B"), self.graphics.get_resource("map", "B")["color"])
        self.add_sidebar_button("Empty (0)", lambda: self.set_selected_value("0"), self.graphics.get_resource("map", "0")["color"])
        self.add_sidebar_button("Save Map", self.save_map, (200, 200, 200))
        self.add_sidebar_button("Main Menu", lambda: self.change_page("main"), (200, 200, 200))

    def add_sidebar_button(self, text, action, color):
        """Lägg till en knapp till sidopanelen."""
        button_y = 10 + len(self.sidebar_buttons) * 50
        button_rect = pygame.Rect(10, button_y, 180, 40)
        self.sidebar_buttons.append({"rect": button_rect, "text": text, "action": action, "color": color})

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

    def handle_events(self):
        """Hantera events som mus- och tangentbordsinmatning."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_held = pygame.mouse.get_pressed()[0]  # Kontrollera om vänster musknapp hålls nere

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_pos[0] < 200:  # Klick på sidopanel
                    for button in self.sidebar_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            button["action"]()
                else:  # Klick på kartan
                    self.modify_cell_under_mouse()
            elif event.type == pygame.MOUSEMOTION:
                # Hantera hover för sidopanelen
                for button in self.sidebar_buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        break
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            elif event.type == pygame.MOUSEMOTION and mouse_held:
                if mouse_pos[0] >= 200:
                    self.modify_cell_under_mouse()
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                self.width, self.height = self.screen.get_size()
                self.calculate_cell_size()
    
    def get_cell_under_mouse(self):
        """Hämta vilken cell musen pekar på."""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if not (self.map_offset_x <= mouse_x < self.map_offset_x + self.cell_size * len(self.map_obj._map[0]) and
                self.map_offset_y <= mouse_y < self.map_offset_y + self.cell_size * len(self.map_obj._map)):
            return None

        cell_x = (mouse_x - self.map_offset_x) // self.cell_size
        cell_y = (mouse_y - self.map_offset_y) // self.cell_size

        if 0 <= cell_y < len(self.map_obj._map) and 0 <= cell_x < len(self.map_obj._map[0]):
            return cell_x, cell_y
        return None

    
    def modify_cell_under_mouse(self):
        """Modifiera cellen under muspekaren."""
        cell_coords = self.get_cell_under_mouse()
        if cell_coords:
            cell_x, cell_y = cell_coords
            self.map_obj.modify_cell(cell_x, cell_y, self.selected_value)

    def render(self):
        """Rendera kartan och sidopanelen."""
        self.calculate_cell_size()
        self.screen.fill(self.graphics.get_resource("gui", "background")["color"])
        self.draw_sidebar()
        self.draw_map()

    def draw_sidebar(self):
        """Rita sidopanelen och dess knappar med hover-effekter."""
        sidebar_bg_color = self.graphics.get_resource("gui", "background")["color"]
        hover_color = self.graphics.get_resource("gui", "hover")["color"]
        button_color = self.graphics.get_resource("gui", "button")["color"]
        border_color = self.graphics.get_resource("gui", "border")["color"]

        # Rita sidopanelens bakgrund
        pygame.draw.rect(self.screen, sidebar_bg_color, (0, 0, 200, self.screen.get_height()))

        font = pygame.font.Font(None, 24)
        mouse_pos = pygame.mouse.get_pos()

        for button in self.sidebar_buttons:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            current_color = hover_color if is_hovered else button_color

            # Rita knappens bakgrund och kant
            pygame.draw.rect(self.screen, current_color, button["rect"], border_radius=5)
            pygame.draw.rect(self.screen, border_color, button["rect"], 2, border_radius=5)

            # Rita knappens text
            text = font.render(button["text"], True, (0, 0, 0))
            self.screen.blit(text, (button["rect"].x + 10, button["rect"].y + 10))

    def calculate_cell_size(self):
        """Beräkna cellstorlek för att kartan ska fylla utrymmet proportionellt och centreras."""
        if not self.map_obj or not self.map_obj._map:
            return

        map_width = len(self.map_obj._map[0])  
        map_height = len(self.map_obj._map)  

        available_width = self.width - 200 
        available_height = self.height

        self.cell_size = min(available_width // map_width, available_height // map_height)

        self.map_offset_x = (available_width - map_width * self.cell_size) // 2 + 200
        self.map_offset_y = (available_height - map_height * self.cell_size) // 2

    def draw_map(self):
        """Rita kartan på skärmen."""
        font = pygame.font.Font(None, self.cell_size - 4)
        for y, row in enumerate(self.map_obj._map):
            for x, cell in enumerate(row):
                cell_x = self.map_offset_x + x * self.cell_size
                cell_y = self.map_offset_y + y * self.cell_size
                resource = self.graphics.get_resource("map", cell)
                color = resource["color"]
                symbol = resource["symbol"]

                if color:
                    pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))

                if symbol:
                    text = font.render(symbol, True, (0, 255, 0))  # Matrix-grönt för symboler
                    text_rect = text.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                    self.screen.blit(text, text_rect)

                border_color = self.graphics.get_resource("gui", "border")["color"]
                pygame.draw.rect(self.screen, border_color, (cell_x, cell_y, self.cell_size, self.cell_size), 1)
