from gui.base_gui import BaseGUI

class MapEditorMenu(BaseGUI):
    """Meny för att välja kartstorlek."""
    def __init__(self, screen, change_page_callback):
        super().__init__(screen, change_page_callback)
        self.set_title("Skapa en ny karta")
        self.add_option("10x10", lambda: self.start_editor(10, 10))
        self.add_option("20x20", lambda: self.start_editor(20, 20))
        self.add_option("50x50", lambda: self.start_editor(50, 50))
        self.add_option("Back", lambda: self.change_page("main"))

    def start_editor(self, width, height):
        """Starta karteditorn med vald storlek."""
        print(f"Startar editor med storlek {width}x{height}")
        self.change_page("map_editor", width=width, height=height)
