import pygame
from gui.base_gui import BaseGUI
from simulation.map import Map
from simulation.get_fleet import get_fleet
from gui.graphics import GraphicsLibrary

class SimulationGUI(BaseGUI):
    """GUI för att köra simuleringen."""
    def __init__(self, screen, change_page_callback, map_file):
        super().__init__(screen, change_page_callback)
        self.set_title("Simulering")
        self.map_file = map_file
        self.graphics = GraphicsLibrary()
        self.sim_map = Map(file_name=self.map_file)
        self.sub_list = get_fleet("uboat.txt", self.sim_map._map)
        self.cell_size = 20

    def draw_map(self):
        """Rita kartan och u-båtarna."""
        font = pygame.font.Font(None, self.cell_size - 4)
        for y, row in enumerate(self.sim_map._map):
            for x, cell in enumerate(row):
                cell_x = x * self.cell_size + 200
                cell_y = y * self.cell_size
                resource = self.graphics.get_resource("map", cell)
                color = resource["color"]
                if color:
                    pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), (cell_x, cell_y, self.cell_size, self.cell_size), 1)

        for sub in self.sub_list:
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                (sub.temp_x * self.cell_size + 200, sub.temp_y * self.cell_size, self.cell_size, self.cell_size),
            )

    def simulate_step(self):
        """Utför ett steg i simuleringen."""
        for sub in self.sub_list:
            sub.basic_scan()
            if sub.planned_route:
                action = sub.planned_route.pop(0)
                if "Move" in action:
                    direction = action.split()[1]
                    sub.move_sub(direction)

    def handle_events(self):
        """Hantera användarens input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        """Kör simuleringen."""
        self.running = True
        while self.running:
            self.handle_events()
            self.simulate_step()
            self.screen.fill(self.graphics.get_resource("gui", "background")["color"])
            self.draw_map()
            pygame.display.flip()
            pygame.time.delay(500)
