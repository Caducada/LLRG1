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
                "E": {"color": (255, 255, 0), "symbol": "E"},     # Exit
                "0": {"color": (255, 255, 255), "symbol": 0},   # Tom cell
                "x": {"color": (100, 100, 100), "symbol": "X"},   # Vägg
                "B": {"color": (255, 0, 0), "symbol": "B"},       # Mina
                "U": {"color": None, "symbol": "U"},     # Ubåt (emoji)
                "y": {"color": (0, 128, 255), "symbol": None},    # Placeholder
                **{str(i): {"color": (0, 128 + i * 14, 0), "symbol": str(i)} for i in range(1, 9)},

            },
        }

    def get_resource(self, category, key):
        """Hämtar grafisk resurs från en specifik kategori."""
        return self.resources.get(category, {}).get(key, {"color": (255, 255, 255), "symbol": None})

