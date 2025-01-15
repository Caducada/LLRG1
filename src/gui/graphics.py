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
                "0": {"color": (0, 0, 0), "symbol": None},
                "x": {"color": (50, 50, 50), "symbol": "X"},
                "B": {"color": (255, 0, 0), "symbol": "B"},
                "submarine": {"color": None, "symbol": "🚤"},     # Ubåt (emoji)
                "y": {"color": (0, 128, 255), "symbol": None},    # Placeholder
            },
        }

    def get_resource(self, category, key):
            """Hämtar resurs från kategori och nyckel."""
            return self.resources.get(category, {}).get(key, {"color": (255, 255, 255), "symbol": None})
