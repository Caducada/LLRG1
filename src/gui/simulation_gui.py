import pygame
from gui.base_gui import BaseGUI
from simulation.simulation import Simulation


class SimulationGUI(BaseGUI):
    def __init__(self, screen, change_page_callback, map_file, fleet_file):
        super().__init__(screen, change_page_callback)
        self.simulation = Simulation(map_file, fleet_file)
        self.cell_size = 20  

    def resize_map(self):
        """Beräknar dynamisk cellstorlek för att fylla hela fönstret."""
        map_width = len(self.simulation.get_map()[0])
        map_height = len(self.simulation.get_map())

        # Använd hela fönstrets bredd och höjd
        available_width = self.width
        available_height = self.height

        # Beräkna cellstorlek baserat på fönstrets storlek och kartans dimensioner
        cell_width = available_width // map_width
        cell_height = available_height // map_height

        # Använd minsta cellstorlek så att kartan får plats
        self.cell_size = min(cell_width, cell_height)

        # Centrera kartan om det finns extra utrymme
        self.map_offset_x = (available_width - (map_width * self.cell_size)) // 2
        self.map_offset_y = (available_height - (map_height * self.cell_size)) // 2

    # def draw_cell(self, x, y, cell):
    #     """Ritar en individuell cell."""
    #     # Översätt interna koordinater till visuella koordinater
    #     visual_x, visual_y = self.simulation.translate_visual_coordinates(x, y)
    #     cell_x = self.map_offset_x + visual_x * self.cell_size
    #     cell_y = self.map_offset_y + visual_y * self.cell_size

    #     resource = self.graphics.get_resource("map", str(cell) if isinstance(cell, int) else cell)
    #     color = resource["color"]
    #     symbol = resource.get("symbol")

    #     # Rita cellens bakgrund
    #     pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))

    #     if symbol:
    #         font = pygame.font.Font(None, int(self.cell_size * 0.7))
    #         text_surface = font.render(str(symbol), True, (0, 0, 0))
    #         text_rect = text_surface.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
    #         self.screen.blit(text_surface, text_rect)

    #     # Rita cellens kant
    #     pygame.draw.rect(self.screen, (0, 0, 0), (cell_x, cell_y, self.cell_size, self.cell_size), 1)

    def draw_cell(self, x, y, cell):
        """Ritar en individuell cell."""
        visual_x, visual_y = self.simulation.translate_visual_coordinates(x, y)
        cell_x = self.map_offset_x + visual_x * self.cell_size
        cell_y = self.map_offset_y + visual_y * self.cell_size

        # Hantering av stenrösen (1-9)
        if isinstance(cell, int) and cell > 0:
            rubble_image = self.graphics.get_image("rubble")
            if rubble_image:
                scaled_image = pygame.transform.scale(rubble_image, (self.cell_size, self.cell_size))
                self.screen.blit(scaled_image, (cell_x, cell_y))
            else:
                color = self.graphics.get_resource("map", str(cell))["color"]
                pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))

            font = pygame.font.Font(None, int(self.cell_size * 0.7))
            text_surface = font.render(str(cell), True, (255,255,255))
            text_rect = text_surface.get_rect(
                center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2)
            )
            self.screen.blit(text_surface, text_rect)
        else:
            resource = self.graphics.get_resource("map", str(cell) if isinstance(cell, int) else cell)
            color = resource["color"]
            symbol = resource.get("symbol")

            pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))

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
        """Ritar en ubåt med bild och ID, där ID visas längst ner i cellen."""
        visual_x, visual_y = self.simulation.translate_visual_coordinates(sub.temp_x, sub.temp_y)
        cell_x = self.map_offset_x + visual_x * self.cell_size
        cell_y = self.map_offset_y + visual_y * self.cell_size

        color = self.graphics.assign_submarine_color(sub.id)

        pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))

        submarine_image = self.graphics.get_image("submarine")
        if submarine_image:
            scaled_image = pygame.transform.scale(submarine_image, (self.cell_size, self.cell_size))
            self.screen.blit(scaled_image, (cell_x, cell_y))

        font = pygame.font.Font(None, int(self.cell_size * 0.4)) 
        id_surface = font.render(f"U{sub.id}", True, (0, 0, 0))  
        id_rect = id_surface.get_rect(midbottom=(cell_x + self.cell_size // 2, cell_y + self.cell_size)) 
        self.screen.blit(id_surface, id_rect)

    def draw_destination(self, sub):
        """Ritar ubåtens slutdestination."""
        visual_x, visual_y = self.simulation.translate_visual_coordinates(sub.xe, sub.ye)
        cell_x = self.map_offset_x + visual_x * self.cell_size
        cell_y = self.map_offset_y + visual_y * self.cell_size

        color = self.graphics.assign_submarine_color(sub.id)
        pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))

        font = pygame.font.Font(None, int(self.cell_size * 0.6))
        id_surface = font.render(f"E U{sub.id}", True, (0, 0, 0))
        id_rect = id_surface.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
        self.screen.blit(id_surface, id_rect)

    def draw_map(self):
        """Ritar hela kartan."""
        self.resize_map()  

        for y, row in enumerate(self.simulation.get_map()):
            for x, cell in enumerate(row):
                self.draw_cell(x, y, cell)

        for sub in self.simulation.get_fleet():
            self.draw_destination(sub)

        for sub in self.simulation.get_active_fleet():
            self.draw_submarine(sub)

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
