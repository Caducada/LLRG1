import pygame
from gui.base_gui import BaseGUI
from simulation.simulation import Simulation


class SimulationGUI(BaseGUI):
    def __init__(self, screen, change_page_callback, map_file, fleet_file):
        super().__init__(screen, change_page_callback)
        self.simulation = Simulation(map_file, fleet_file)
        self.cell_size = 20  # Standardvärde, uppdateras dynamiskt i `resize_map`

    def resize_map(self):
        """Beräknar dynamisk cellstorlek för att fylla fönstret."""
        map_width = len(self.simulation.get_map()[0])
        map_height = len(self.simulation.get_map())

        available_width = self.width - 200  # Lämnar marginal för sidofält
        available_height = self.height

        cell_width = available_width // map_width
        cell_height = available_height // map_height

        self.cell_size = min(cell_width, cell_height)

    def draw_cell(self, x, y, cell):
        """Ritar en individuell cell."""
        cell_x = x * self.cell_size + 200
        cell_y = y * self.cell_size

        resource = self.graphics.get_resource("map", cell)
        color = resource["color"]
        symbol = resource.get("symbol")

        if color:
            pygame.draw.rect(
                self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size)
            )
        if symbol:
            font = pygame.font.Font(None, int(self.cell_size * 0.7))
            text_surface = font.render(str(symbol), True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2)
            )
            self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(
            self.screen, (0, 0, 0), (cell_x, cell_y, self.cell_size, self.cell_size), 1
        )

    def draw_submarine(self, sub):
        """Ritar en ubåt."""
        submarine_resource = self.graphics.get_resource("map", "U")
        cell_x = sub.temp_x * self.cell_size + 200
        cell_y = sub.temp_y * self.cell_size

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),  # Bakgrundsfärg för ubåten
            (cell_x, cell_y, self.cell_size, self.cell_size),
        )

        if submarine_resource["symbol"]:
            font = pygame.font.Font(None, int(self.cell_size * 0.7))
            text_surface = font.render(submarine_resource["symbol"], True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2)
            )
            self.screen.blit(text_surface, text_rect)

    def draw_destination(self, sub):
        """Ritar en ubåts slutdestination."""
        destination_color = self.graphics.get_resource("map", "E")["color"]
        cell_x = sub.xe * self.cell_size + 200
        cell_y = sub.ye * self.cell_size

        pygame.draw.rect(
            self.screen,
            destination_color,
            (cell_x, cell_y, self.cell_size, self.cell_size),
        )

        font = pygame.font.Font(None, int(self.cell_size * 0.6))
        id_surface = font.render(f"{sub.id}", True, (0, 0, 0))
        id_rect = id_surface.get_rect(
            center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2)
        )
        self.screen.blit(id_surface, id_rect)

    def draw_map(self):
        """Ritar hela kartan."""
        self.resize_map()  # Uppdatera cellstorlek dynamiskt

        # Ritar kartans celler
        for y, row in enumerate(self.simulation.get_map()):
            for x, cell in enumerate(row):
                self.draw_cell(x, y, cell)

        # Ritar ubåtar och slutdestinationer
        for sub in self.simulation.get_active_fleet():
            if not self.simulation.is_valid_destination(sub.xe, sub.ye):
                print(f"Ubåtens slutdestination ({sub.xe}, {sub.ye}) är ogiltig.")
                sub.is_alive = False

            if sub.is_alive:
                self.draw_submarine(sub)
            self.draw_destination(sub)

    def simulate_step(self):
        """Utför ett steg i simuleringen."""
        self.simulation.step()

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

            if self.simulation.is_simulation_complete():
                print("Simulation complete!")
                self.change_page("main")
