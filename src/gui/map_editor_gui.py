from simulation.map import Map
import pygame

class MapEditor:
    """Hanterar kartredigering i pygame"""
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = 20
        self.map_obj = Map()
        self.map_obj.create_empty_map(30,20)
        self.selected_value = 'x'

    def draw_map(self):
        """Ritar Kartan på skärmen"""
        for y, row in enumerate(self.map_obj._map):
            for x, cell in enumerate(row):
                color = {
                    '0': (255, 255, 255),
                    'x': (100,100,100),
                    'B': (255,0,0)
                }.get(cell, (0,0,0))
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size), 1)

    def get_cell_under_mouse(self):
        """Hämtar kartcellen under muspekaren"""
        x, y = pygame.mouse.get_pos()
        return x // self.cell_size, y // self.cell_size

    def run(self):
        """Kör karteditorn."""
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.draw_map()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    cell_x, cell_y = self.get_cell_under_mouse()
                    self.map_obj.modify_cell(cell_x, cell_y, self.selected_value)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        self.selected_value = 'x'
                    elif event.key == pygame.K_b:
                        self.selected_value = 'B'
                    elif event.key == pygame.K_0:
                        self.selected_value = '0'
                    elif event.key == pygame.K_s:
                        self.map_obj.save_map_to_file("edited_map.txt")
                        print("Map saved.")

            pygame.display.flip()