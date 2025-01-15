# class PageManager:
#     """Hanterar navigering mellan olika GUI-sidor."""
#     def __init__(self, screen):
#         self.screen = screen
#         self.pages = {}
#         self.current_page = None

#     def add_page(self, name, page):
#         """Lägg till en sida i navigeringshanteraren."""
#         self.pages[name] = page

#     def set_page(self, name):
#         """Byt till en ny sida."""
#         if name in self.pages:
#             self.current_page = self.pages[name]
#             self.current_page.run()

#     def start(self, start_page):
#         """Starta navigering."""
#         self.set_page(start_page)
