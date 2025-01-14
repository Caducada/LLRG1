import pygame
import os
from gui.base_gui import BaseGUI
from simulation.map import Map
from simulation.get_fleet import get_fleet
from gui.graphics import GraphicsLibrary

BASE_DIR = os.path.abspath(".")
MAP_DIR = os.path.join(BASE_DIR, "data", "maps")
FLEET_FILE = "uboat.txt"

class SimulationGUI(BaseGUI):
    """Hantera simuleringens GUI."""
    def __init__(self, screen):
        super().__init__(screen)
        self.graphics = GraphicsLibrary()
        self.sim_map = None
        self.cell_size = 20
    
    def show_map_selection_menu(self):
        """Visar en meny för att välja karta."""
        font = pygame.font.Font(None, 36)
        map_files = [f for f in os.listdir(MAP_DIR) if f.endswith('.txt')]

        thumbnail_size = (100, 100)
        map_thumbnails = {}

        for map_file in map_files:
            map_path = os.path.join(MAP_DIR, map_file)
            temp_map = Map(file_name=map_path, sub_file_name=FLEET_FILE)
            map_data = temp_map._map
            map_thumbnails[map_file] = self.generate_map_thumbnail(map_data, thumbnail_size)

        buttons = []
        for i, map_file in enumerate(map_files):
            rect = pygame.Rect(50, 50 + i * 120, 200, 100)
            buttons.append({"rect": rect, "map_file": map_file})

        while True:
            self.screen.fill((0, 0, 0))

            for button in buttons:
                pygame.draw.rect(self.screen, (150, 150, 150), button["rect"])
                map_thumbnail = map_thumbnails[button["map_file"]]
                self.screen.blit(map_thumbnail, (button["rect"].x + 220, button["rect"].y))
                text = font.render(button["map_file"], True, (255, 255, 255))
                self.screen.blit(text, (button["rect"].x + 10, button["rect"].y + 10))
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            return button["map_file"]  

    def generate_map_thumbnail(self, map_data, size):
        """Genererar en miniatyr för en karta."""
        thumbnail = pygame.Surface(size)
        cell_size = min(size[0] // len(map_data[0]), size[1] // len(map_data))
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                color = self.graphics.get_resource(cell)["color"]
                if color:
                    pygame.draw.rect(thumbnail, color, (x * cell_size, y * cell_size, cell_size, cell_size))
        return thumbnail
    
    def load_simulation_data(self, map_name):
        """Ladda data för simuleringen."""
        map_file = os.path.join(MAP_DIR, map_name)

        if not os.path.isfile(map_file):
            raise FileNotFoundError(f"Map file not found: {map_file}")

        self.sim_map = Map(file_name=map_file, sub_file_name=FLEET_FILE)

    def simulate_step(self):
        """Utför ett steg i simuleringen."""
        for sub in self.sim_map.fleet:
            sub.basic_scan()
            if sub.planned_route:
                action = sub.planned_route.pop(0)
                if "Move" in action:
                    direction = action.split()[1]
                    sub.move_sub(direction)
        self.sim_map.update_map()

    def draw_map_with_submarines(self):
        """Ritar kartan och ubåtarna."""
        font = pygame.font.Font(None, self.cell_size - 4)
        for y, row in enumerate(self.sim_map._map):
            for x, cell in enumerate(row):
                cell_x = x * self.cell_size
                cell_y = y * self.cell_size
                resource = self.graphics.get_resource(cell)
                color = resource["color"]
                symbol = resource["symbol"]
                if color:
                    pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))
                if symbol:
                    text = font.render(symbol, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                    self.screen.blit(text, text_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), (cell_x, cell_y, self.cell_size, self.cell_size), 1)

        for sub in self.sim_map.fleet:
            pygame.draw.rect(
                self.screen,
                (0, 255, 0), 
                (sub.temp_x * self.cell_size, sub.temp_y * self.cell_size, self.cell_size, self.cell_size)
            )
    
    def run_simulation(self):
        """Kör simuleringen."""
        self.running = True
        while self.running:
            self.handle_events()
            self.simulate_step()
            self.draw_map_with_submarines()
            pygame.display.flip()
            pygame.time.delay(500)

    def run(self):
        """Huvudmetod för att köra simuleringen."""
        selected_map = self.show_map_selection_menu()  
        self.load_simulation_data(selected_map)   
        self.run_simulation() 
