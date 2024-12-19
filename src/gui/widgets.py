import pygame


class GraphicsLibrary:
    def __init__(self):
        self.resources = {}

    def load_resources(self, resources):
        """Ladda resurser från en konfiguration."""
        for key, value in resources.items():
            self.resources[key] = value

    def get_resource(self, key):
        """Hämtar en resurs, eller standard."""
        return self.resources.get(key, {"color": (0, 0, 0), "symbol": "?"})