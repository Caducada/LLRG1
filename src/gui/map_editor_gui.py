from simulation.map import Map
from .widgets import GraphicsLibrary
import tkinter as tk
from tkinter.simpledialog import askinteger
import pygame

class MapEditor:
    """Hanterar kartredigering i pygame."""
    def __init__(self, screen):
        self.screen = screen
        self.sidebar_width = 200
        self.cell_size = 20
        self.map_obj = None 
        self.running = False
        self.selected_value = '0'
        self.graphics = GraphicsLibrary()  # Instansiera grafikbiblioteket
        self.buttons = []  

    def ask_map_size(self):
        """Visa val för att välja kartstorlek."""
        font = pygame.font.Font(None, 36)
        size_buttons = [
            {"rect": pygame.Rect(250, 200, 200, 50), "text": "10x10", "size": (10, 10)},
            {"rect": pygame.Rect(250, 300, 200, 50), "text": "20x20", "size": (20, 20)},
            {"rect": pygame.Rect(250, 400, 200, 50), "text": "50x50", "size": (50, 50)},
        ]

        while True:
            self.screen.fill((0, 0, 0))
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

    def init_buttons(self):
        """Initiera knappar för sidopanelen."""
        self.buttons = [
            {"rect": pygame.Rect(10, 10, 180, 30), "text": "Wall (x)", "value": "x", "color": self.graphics.get_resource('x')["color"]},
            {"rect": pygame.Rect(10, 50, 180, 30), "text": "Mine (B)", "value": "B", "color": self.graphics.get_resource('B')["color"]},
            {"rect": pygame.Rect(10, 90, 180, 30), "text": "Empty (0)", "value": "0", "color": self.graphics.get_resource('0')["color"]},
            {"rect": pygame.Rect(10, 140, 180, 30), "text": "Save Map", "action": self.save_map, "color": (200, 200, 200)},
            {"rect": pygame.Rect(10, 180, 180, 30), "text": "Main Menu", "action": self.go_to_main_menu, "color": (200, 200, 200)},
        ]

    def save_map(self):
        """Sparar kartan till underground.txt."""
        self.map_obj.save_map_to_file("data/maps/underground.txt")
        print("Map saved to underground.txt.")

    def go_to_main_menu(self):
        """Avslutar redigeraren och går tillbaka till huvudmenyn."""
        self.running = False  # Stäng ner editorn

    def calculate_cell_size(self):
        """Anpassar cellstorleken så att kartan fyller tillgängligt utrymme."""
        map_width = len(self.map_obj._map[0])
        map_height = len(self.map_obj._map)
        available_width = self.screen.get_width() - self.sidebar_width
        available_height = self.screen.get_height()

        # Anpassa cellstorlek baserat på tillgängligt utrymme
        cell_width = available_width // map_width
        cell_height = available_height // map_height
        self.cell_size = min(cell_width, cell_height)

    def draw_sidebar(self):
        """Ritar sidopanelen."""
        font = pygame.font.Font(None, 24)
        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(self.screen, (220, 220, 220), (0, 0, self.sidebar_width, self.screen.get_height()))
        for button in self.buttons:
            rect = button["rect"]
            color = button.get("color", (150, 150, 150))
            text_color = (0, 0, 0)
            if rect.collidepoint(mouse_pos):
                color = (255, 255, 0)  # Hover-effekt

            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            text = font.render(button["text"], True, text_color)
            self.screen.blit(text, (rect.x + 10, rect.y + 5))

    def handle_button_click(self, mouse_pos):
        """Hantera klick på knappar."""
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                if "value" in button:
                    self.selected_value = button["value"]
                elif "action" in button:
                    button["action"]()

    def draw_map(self):
        """Ritar kartan på skärmen med färger och symboler."""
        font = pygame.font.Font(None, self.cell_size - 4)
        for y, row in enumerate(self.map_obj._map):
            for x, cell in enumerate(row):
                cell_x = self.sidebar_width + x * self.cell_size
                cell_y = y * self.cell_size

                # Hämta grafisk resurs
                resource = self.graphics.get_resource(cell)
                color = resource["color"]
                symbol = resource["symbol"]

                # Rita cellens bakgrundsfärg
                if color:
                    pygame.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))

                # Rita symbol om den finns
                if symbol:
                    text = font.render(symbol, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                    self.screen.blit(text, text_rect)

                # Rita cellens gränser
                pygame.draw.rect(self.screen, (0, 0, 0), (cell_x, cell_y, self.cell_size, self.cell_size), 1)

    def get_cell_under_mouse(self):
        """Hämtar kartcellen under muspekaren."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < self.sidebar_width:
            return None  # Musen är över sidopanelen
        cell_x = (mouse_x - self.sidebar_width) // self.cell_size
        cell_y = mouse_y // self.cell_size
        if 0 <= cell_y < len(self.map_obj._map) and 0 <= cell_x < len(self.map_obj._map[0]):
            return cell_x, cell_y
        return None

    def run(self):
        """Kör karteditorn."""
        self.ask_map_size()  
        self.init_buttons() 
        self.running = True
        while self.running:
            self.calculate_cell_size()
            self.screen.fill((0, 0, 0))
            self.draw_sidebar()
            self.draw_map()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Vänsterklick
                        mouse_pos = pygame.mouse.get_pos()
                        if mouse_pos[0] < self.sidebar_width:
                            self.handle_button_click(mouse_pos)
                        else:
                            cell_coords = self.get_cell_under_mouse()
                            if cell_coords:
                                cell_x, cell_y = cell_coords
                                self.map_obj.modify_cell(cell_x, cell_y, self.selected_value)

            pygame.display.flip()