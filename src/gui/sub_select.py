import pygame
import os
import random
from gui.base_gui import BaseGUI
from simulation.map import Map
from simulation.map import SUB_DIR, MAP_DIR  # För att spara ubåtsfilen i rätt katalog

class SubmarineSelectionMenu(BaseGUI):
    """Meny för att välja ubåtsdata innan simulering."""
    def __init__(self, screen, change_page_callback, map_file):
        super().__init__(screen, change_page_callback)
        self.set_title("Välj ubåtsalternativ")
        self.map_file = map_file

        # Lägg till knappar
        self.add_option("Standardflotta", self.run_default_sim)
        self.add_option("Slumpmässiga ubåtar", self.open_submarine_popup)
        self.add_option("Tillbaka", lambda: self.change_page("simulation_menu"))

        # Popup-fält
        self.show_popup = False
        self.input_text = ""
        self.error_message = ""

    def run_default_sim(self):
        """Kör simuleringen med standardflottan."""
        self.change_page("simulation", map_file=self.map_file, fleet_file="uboat.txt")

    def open_submarine_popup(self):
        """Öppnar en popup för att ange antal slumpmässiga ubåtar."""
        self.show_popup = True
        self.input_text = ""
        self.error_message = ""

    def handle_events(self):
        """Hantera händelser i menyn och popupen."""
        if self.show_popup:
            self.handle_popup_events()  # Hantera popupen
        else:
            super().handle_events()  # Hantera normala menyknappar

    def handle_popup_events(self):
        """Hantera händelser för popup-fönstret."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.validate_and_start_sim()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.unicode.isdigit():
                    self.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.cancel_button.collidepoint(event.pos):
                    self.show_popup = False
                elif self.start_button.collidepoint(event.pos):
                    self.validate_and_start_sim()

    def validate_and_start_sim(self):
        """Validerar input och startar simuleringen om korrekt."""
        try:
            num_submarines = int(self.input_text.strip())
            if num_submarines < 1 or num_submarines > 100:
                self.error_message = "Antalet måste vara mellan 1 och 100!"
            else:
                self.generate_random_submarines(num_submarines)
                print(f"Genererar {num_submarines} slumpmässiga ubåtar...")
                self.change_page("simulation", map_file=self.map_file, fleet_file="random_dumb.txt")
        except ValueError:
            self.error_message = "Ange ett giltigt heltal!"

    def generate_random_submarines(self, num_submarines):
        """Genererar slumpmässiga ubåtar och sparar i en fil."""
        map_path = os.path.join(MAP_DIR, self.map_file)
        temp_map = Map(file_name=map_path)
        map_data = temp_map._map

        if not map_data:
            self.error_message = "Kartan kunde inte läsas in!"
            return

        submarines = []
        attempts = 0
        max_attempts = num_submarines * 5  

        while len(submarines) < num_submarines and attempts < max_attempts:
            spawn = self.get_random_location(map_data)
            end = self.get_random_location(map_data)

            if spawn and end:
                spawn_x, spawn_y = spawn
                end_x, end_y = end
                missiles = random.randint(5, 20)
                submarines.append(f"{spawn_x},{spawn_y},{end_x},{end_y},{missiles}")
            attempts += 1

        if len(submarines) == 0:
            self.error_message = "Misslyckades att generera ubåtar."
            return

        fleet_file_path = os.path.join(SUB_DIR, "random_dumb.txt")
        os.makedirs(SUB_DIR, exist_ok=True)  

        with open(fleet_file_path, "w") as f:
            f.write("X0,Y0,XE,YE,M\n")
            f.write("\n".join(submarines))

        print(f"Ubåtsdata sparat till {fleet_file_path}")

    def get_random_location(self, map_data):
        """Hitta en slumpmässig giltig plats på kartan."""
        if not map_data:
            return None

        rows, cols = len(map_data), len(map_data[0])
        available_positions = [
            (x, y) for y in range(rows) for x in range(cols) 
            if str(map_data[y][x]) == "0"
        ]
        return random.choice(available_positions) if available_positions else None

    def render(self):
        """Renderar menyn och popupen."""
        super().render()

        if self.show_popup:
            self.draw_popup()

    def draw_popup(self):
        """Ritar popup-fönstret för att ange antal ubåtar."""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        self.popup_rect = pygame.Rect(self.width // 2 - 250, self.height // 2 - 150, 500, 300)
        pygame.draw.rect(self.screen, (50, 50, 50), self.popup_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.popup_rect, 3, border_radius=10)

        font = pygame.font.Font(None, 36)
        title_surface = font.render("Ange antal ubåtar (1-100):", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.popup_rect.x + 50, self.popup_rect.y + 20))

        input_box = pygame.Rect(self.popup_rect.x + 150, self.popup_rect.y + 80, 200, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), input_box)
        input_surface = font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

        self.cancel_button = pygame.Rect(self.popup_rect.x + 50, self.popup_rect.y + 200, 150, 50)
        self.start_button = pygame.Rect(self.popup_rect.x + 300, self.popup_rect.y + 200, 150, 50)

        pygame.draw.rect(self.screen, (200, 0, 0), self.cancel_button, border_radius=10)
        pygame.draw.rect(self.screen, (0, 200, 0), self.start_button, border_radius=10)

        cancel_surface = font.render("Avbryt", True, (255, 255, 255))
        start_surface = font.render("Start", True, (255, 255, 255))

        self.screen.blit(cancel_surface, (self.cancel_button.x + 25, self.cancel_button.y + 10))
        self.screen.blit(start_surface, (self.start_button.x + 40, self.start_button.y + 10))

        if self.error_message:
            error_surface = font.render(self.error_message, True, (255, 0, 0))
            self.screen.blit(error_surface, (self.popup_rect.x + 50, self.popup_rect.y + 260))