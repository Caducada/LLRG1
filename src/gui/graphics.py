import pygame
import os
class GraphicsLibrary:
    """Hanterar grafiska resurser för GUI och kartobjekt."""
    def __init__(self):
        self.resources = {
            "gui": {
                "background": {"color": (0, 0, 0)},
                "title": {"color": (0, 255, 0)},
                "button": {"color": (50, 150, 50)},
                "hover": {"color": (100, 255, 100)},
                "border": {"color": (0, 255, 0)},
            },
            "map": {
                "D": {"color": (100, 100, 100), "symbol": "D"},
                "E": {"color": (255, 255, 0), "symbol": "E"}, 
                "0": {"color": (255, 255, 255), "symbol": ""}, 
                "x": {"color": (100, 100, 100), "symbol": "X"}, 
                "B": {"color": (255, 0, 0), "symbol": "B"}, 
                **{str(i): {"color": (0, 128 + i * 14, 0), "symbol": str(i)} for i in range(1, 10)}, 
            },
        }
        self.submarine_colors = {} 
        self.images = self._load_images()


    def _load_images(self):
        """Laddar bilder för ubåtar och stenrösen."""
        images = {}
        base_path = os.path.dirname(os.path.abspath(__file__)) 
        try:
            images["submarine"] = pygame.image.load(os.path.join(base_path, "assets/sub.png"))
            images["rubble"] = pygame.image.load(os.path.join(base_path, "assets/rubble.png"))
            images["mine"] = pygame.image.load(os.path.join(base_path, "assets/mine.png"))
            images["skull"] = pygame.image.load(os.path.join(base_path, "assets/skull.png"))
        except FileNotFoundError as e:
            print(f"Några bilder saknas: {e}. Standardrepresentation används.")
        return images


    def assign_submarine_color(self, sub_id):
        """Tilldelar en unik färg till varje ubåt."""
        import random
        if sub_id not in self.submarine_colors:
            self.submarine_colors[sub_id] = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255),
            )
        return self.submarine_colors[sub_id]

    def get_resource(self, category, key):
        """Hämtar grafisk resurs från en specifik kategori."""
        return self.resources.get(category, {}).get(key, {"color": (255, 255, 255), "symbol": None})

    def get_image(self, key):
        """Returnerar en bild om tillgänglig."""
        return self.images.get(key)
