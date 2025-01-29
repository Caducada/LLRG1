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
        self.selected_value = "x"
        self.graphics = GraphicsLibrary()
        self.sidebar_buttons = [] 
        self.init_sidebar()
        self.calculate_cell_size()

    def init_sidebar(self):
        """Initiera sidopanelens knappar."""
        self.add_sidebar_button("Wall (x)", lambda: self.set_selected_value("x"), self.graphics.get_resource("map", "x")["color"])
        self.add_sidebar_button("Mine (B)", lambda: self.set_selected_value("B"), self.graphics.get_resource("map", "B")["color"])
        self.add_stonepile_buttons(range(1, 9))  
        self.add_sidebar_button("Empty (0)", lambda: self.set_selected_value("0"), self.graphics.get_resource("map", "0")["color"])
        self.add_sidebar_button("Save Map", self.save_map, (200, 200, 200))
        self.add_sidebar_button("Main Menu", lambda: self.change_page("main"), (200, 200, 200))

    def add_sidebar_button(self, text, action, color):
        """Lägg till en vanlig knapp till sidopanelen."""
        if len(self.sidebar_buttons) > 0:
            last_button = self.sidebar_buttons[-1]
            button_y = last_button["rect"].bottom + 10  
        else:
            button_y = 10 

        button_rect = pygame.Rect(10, button_y, 180, 40)
        self.sidebar_buttons.append({"rect": button_rect, "text": text, "action": action, "color": color, "is_stonepile": False})

    def add_stonepile_buttons(self, stone_range):
        """Lägg till stenröseknappar, två och två per rad."""
        buttons_per_row = 2
        button_width = (200 - 30) // buttons_per_row  #
        button_height = 40
        spacing = 10

        if len(self.sidebar_buttons) > 0:
            last_button = self.sidebar_buttons[-1]
            stonepile_start_y = last_button["rect"].bottom + 10
        else:
            stonepile_start_y = 10

        for i, stone_value in enumerate(stone_range):
            color = self.graphics.get_resource("map", str(stone_value))["color"]
            row = i // buttons_per_row
            col = i % buttons_per_row

            button_x = 10 + col * (button_width + spacing)
            button_y = stonepile_start_y + row * (button_height + spacing)

            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.sidebar_buttons.append({"rect": button_rect, "text": str(stone_value), "action": lambda value=str(stone_value): self.set_selected_value(value), "color": color, "is_stonepile": True})

    def set_selected_value(self, value):
        """Ställ in det valda värdet för redigering."""
        self.selected_value = value

    def save_map(self):
        """Spara kartan till en fil."""
        if not self.map_obj:
            print("No map to save.")
            return

        file_name = self.get_file_name_input()
        if file_name:
            if not file_name.endswith(".txt"):
                file_name += ".txt" 
            self.map_obj.save_map_to_file(file_name)
            print(f"Map saved to {file_name}.")
        else:
            print("Save canceled.")

    def get_file_name_input(self):
        """Visa en popup för att låta användaren mata in ett filnamn."""
        running = True
        input_box = pygame.Rect(self.width // 2 - 150, self.height // 2 - 20, 300, 40)
        color_inactive = (150, 150, 150)
        color_active = (0, 255, 0)
        color = color_inactive
        active = False
        text = ""
        font = pygame.font.Font(None, 32)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text.strip()  
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

                    if event.key == pygame.K_ESCAPE:
                        return None  

            self.screen.fill((30, 30, 30))  
            pygame.draw.rect(self.screen, (50, 50, 50), (self.width // 2 - 160, self.height // 2 - 60, 320, 120))
            pygame.draw.rect(self.screen, color, input_box, 2)

            title_surface = font.render("Enter file name to save:", True, (255, 255, 255))
            self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, self.height // 2 - 50))

            text_surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(300, text_surface.get_width() + 10)

            cancel_button = pygame.Rect(self.width // 2 - 60, self.height // 2 + 40, 120, 30)
            pygame.draw.rect(self.screen, (200, 0, 0), cancel_button)
            cancel_text = font.render("Cancel", True, (255, 255, 255))
            self.screen.blit(cancel_text, (cancel_button.x + (cancel_button.w - cancel_text.get_width()) // 2, cancel_button.y + 5))

            pygame.display.flip()

            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and cancel_button.collidepoint(mouse_pos):
                return None  

    def handle_events(self):
        """Hantera events som mus- och tangentbordsinmatning."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_held = pygame.mouse.get_pressed()[0]  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_pos[0] < 200:  
                    for button in self.sidebar_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            button["action"]()
                else: 
                    self.modify_cell_under_mouse()
            elif event.type == pygame.MOUSEMOTION and mouse_held:  
                if mouse_pos[0] >= 200:  
                    self.modify_cell_under_mouse()
            elif event.type == pygame.VIDEORESIZE:
                print("Window resized to", event.size)
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

        pygame.draw.rect(self.screen, sidebar_bg_color, (0, 0, 200, self.screen.get_height()))

        font = pygame.font.Font(None, 24)
        mouse_pos = pygame.mouse.get_pos()

        for button in self.sidebar_buttons:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            current_color = hover_color if is_hovered else button_color

            pygame.draw.rect(self.screen, current_color, button["rect"], border_radius=5)
            pygame.draw.rect(self.screen, border_color, button["rect"], 2, border_radius=5)

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
        """Rita kartan så att den fyller hela tillgängligt utrymme."""
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
                    text = font.render(symbol, True, (0, 0, 0))  
                    text_rect = text.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                    self.screen.blit(text, text_rect)

                pygame.draw.rect(self.screen, (0, 0, 0), (cell_x, cell_y, self.cell_size, self.cell_size), 1)

