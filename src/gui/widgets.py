import pygame


class GraphicsLibrary:
    """Hanterar grafiska resurser för kartobjekt."""
    def __init__(self):
        self.resources = {}
        self.load_resources()

    def load_resources(self):
        """Laddar grafiska resurser."""
        self.resources = {
            '0': {"color": (255, 255, 255), "symbol": None},   # Tom cell
            'x': {"color": (100, 100, 100), "symbol": "X"},   # Vägg
            'B': {"color": (255, 0, 0), "symbol": "B"},       # Mina
            'submarine': {"color": None, "symbol": "🚤"},     # Ubåt (emoji)
            'y': {"color": (0, 128, 255), "symbol": None},    # Stenrös (placeholder färg)
        }

    def get_resource(self, key):
        """Hämtar grafisk resurs för ett objekt"""
        return self.resources.get(key, {"color": (0, 0, 0), "symbol": "?"})