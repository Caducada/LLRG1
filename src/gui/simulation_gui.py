import pygame
from gui.base_gui import BaseGUI
from simulation.simulation import Simulation

class SimulationGUI(BaseGUI):
    def __init__(self, screen, change_page_callback, map_file, fleet_file):
        super().__init__(screen, change_page_callback)
        self.simulation = Simulation(map_file, fleet_file)
        self.cell_size = 20  

        self.button_width = 150
        self.button_height = 40
        self.button_spacing = 10  

        self.buttons = self.create_buttons()
        self.paused = False 

    def create_buttons(self):
        """Skapar knappar på vänstra sidan av skärmen."""
        start_y = 50
        buttons = []

        button_data = [
            ("Fog of War", self.toggle_fog_of_war),
            ("Pause", self.toggle_pause),
            ("Exit", self.exit_simulation)
        ]

        for index, (text, action) in enumerate(button_data):
            button_rect = pygame.Rect(10, start_y + index * (self.button_height + self.button_spacing), self.button_width, self.button_height)
            buttons.append({"rect": button_rect, "text": text, "action": action, "hover": False})

        return buttons

    def toggle_fog_of_war(self):
        """Placeholder-funktion för att aktivera Fog of War."""
        print("Fog of War toggled!")

    def toggle_pause(self):
        """Pausar eller återupptar simuleringen."""
        self.paused = not self.paused
        print("Paused:", self.paused)

    def exit_simulation(self):
        """Avslutar simuleringen och går tillbaka till huvudmenyn."""
        self.running = False
        self.change_page("main")

    def draw_buttons(self):
        """Ritar knapparna på vänstra sidan av skärmen."""
        font = pygame.font.Font(None, 24)
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)

            button_color = (0, 180, 0) if button["hover"] else (0, 150, 0) 
            text_color = (255, 255, 255)

            pygame.draw.rect(self.screen, button_color, button["rect"], border_radius=5)
            pygame.draw.rect(self.screen, (50, 50, 50), button["rect"], 2, border_radius=5)

            text_surface = font.render(button["text"], True, text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

    def resize_map(self):
        """Beräknar dynamisk cellstorlek för att fylla hela fönstret och centrera kartan."""
        map_width = len(self.simulation.get_map()[0])
        map_height = len(self.simulation.get_map())

        cell_width = self.width // map_width
        cell_height = self.height // map_height

        self.cell_size = min(cell_width, cell_height)

        self.map_offset_x = (self.width - (map_width * self.cell_size)) // 2
        self.map_offset_y = (self.height - (map_height * self.cell_size)) // 2

    def draw_cell(self, x, y, cell):
        """Ritar en individuell cell."""
        visual_x, visual_y = self.simulation.translate_visual_coordinates(x, y)
        cell_x = self.map_offset_x + visual_x * self.cell_size
        cell_y = self.map_offset_y + visual_y * self.cell_size

        dead_subs_at_pos = [sub_id for sub_id, pos in self.simulation.map.dead_sub_positions.items() if pos == (x, y)]

        if dead_subs_at_pos:
            pygame.draw.rect(self.screen, (100, 100, 100), (cell_x, cell_y, self.cell_size, self.cell_size))
            skull_image = self.graphics.get_image("skull")
            if skull_image:
                scaled_image = pygame.transform.scale(skull_image, (self.cell_size, self.cell_size))
                self.screen.blit(scaled_image, (cell_x, cell_y))
            else:
                font = pygame.font.Font(None, int(self.cell_size * 0.7))
                text_surface = font.render("☠", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                self.screen.blit(text_surface, text_rect)

            # Visa ID:n på de ubåtar som dog här
            font = pygame.font.Font(None, int(self.cell_size * 0.5))
            id_surface = font.render(f"U{','.join(map(str, dead_subs_at_pos))}", True, (255, 255, 255))
            id_rect = id_surface.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size - 5))
            self.screen.blit(id_surface, id_rect)

            return

        if cell == "B":
            pygame.draw.rect(self.screen, (255, 0, 0), (cell_x, cell_y, self.cell_size, self.cell_size))

            mine_image = self.graphics.get_image("mine")
            if mine_image:
                scaled_image = pygame.transform.scale(mine_image, (self.cell_size, self.cell_size))
                self.screen.blit(scaled_image, (cell_x, cell_y))
            else:
                font = pygame.font.Font(None, int(self.cell_size * 0.7))
                text_surface = font.render("B", True, (255, 255, 255)) 
                text_rect = text_surface.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                self.screen.blit(text_surface, text_rect)
        elif isinstance(cell, int) and cell > 0:
            rubble_image = self.graphics.get_image("rubble")
            if rubble_image:
                scaled_image = pygame.transform.scale(rubble_image, (self.cell_size, self.cell_size))
                self.screen.blit(scaled_image, (cell_x, cell_y))
            else:
                color = self.graphics.get_resource("map", str(cell))["color"]
                pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))

            font = pygame.font.Font(None, int(self.cell_size * 0.7))
            text_surface = font.render(str(cell), True, (255, 255, 255))
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
        """Ritar en ubåt med bild och ID, men ignorerar de som är döda."""
        if not sub.is_alive:
            return  

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
        """Ritar hela kartan och dess innehåll."""
        self.resize_map()

        for y, row in enumerate(self.simulation.get_map()):
            for x, cell in enumerate(row):
                self.draw_cell(x, y, cell)

        for sub in self.simulation.get_fleet():
            if sub.is_alive:
                self.draw_destination(sub)

        for sub in self.simulation.get_active_fleet():
            self.draw_submarine(sub)
    
    def handle_events(self):
        """Hanterar användarinmatningar."""
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        button["action"]()
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.size)

    def simulate_step(self):
        """Utför ett steg i simuleringen."""
        self.simulation.step()

    def run(self):
        """Kör simuleringen."""
        self.running = True
        while self.running:
            self.handle_events()
            if not self.paused:
                self.simulate_step()

            self.screen.fill(self.graphics.get_resource("gui", "background")["color"])
            self.draw_buttons()
            self.draw_map()

            pygame.display.flip()
            pygame.time.delay(200)

            if self.simulation.is_simulation_complete() or (self.simulation.max_cycles and self.simulation.cycle_count >= self.simulation.max_cycles):
                print("Simulation complete or max cycles reached!")
                self.change_page("main")