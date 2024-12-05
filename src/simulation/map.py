import os
import csv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAP_DIR = os.path.join(BASE_DIR, "data", "maps/")

class Map:
    def __init__(self, file_name = "underground.txt") -> None:
        self._file_name = file_name
        self._map = self.read_map_file(file_name)


    def print_map(self):
        for row in self._map:
            print(f'{row}')


    def convert_digits(self, value):
        if value.isdigit():  # Check if the value is a digit
            return int(value)  # Convert to integer
        return value  # Return the original value if it's not a digit


    def valid_map(self, map):
        for row in map:
            for col in row:
                if col not in ['x', 'B', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    print(col)
                    return False
        return True


    def read_map_file(self, file: str):
        MAP_FILE = os.path.join(MAP_DIR, file)
        map = [[]]

        if not os.path.exists(MAP_FILE):
            print("File not found")
            return map
        if os.path.getsize(MAP_FILE) == 0:
            print("File is empty")
            return map
        
        try:
            with open(MAP_FILE, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    converted_row = [self.convert_digits(item) for item in row]
                    map.append(converted_row)
            if self.valid_map(map):
                return map
            else:
                return []

        except Exception as e:
            print(f'{e}')
            return []
        
    def create_empty_map(self, width, height, default_value='0'):
        """Skapar en tom karta med angiven storlek."""
        self._map = [[default_value for _ in range(width)] for _ in range(height)]

    def generate_random_map(self):
        """Genererar en slumpmässig karta."""
        pass

    def modify_cell(self, x, y, value):
        """Modifierar en cell på kartan."""
        if 0 <= y < len(self._map) and 0 <= x < len(self._map[0]):
            self._map[y][x] = value
        else:
            print("Invalid coordinates")

new_map = Map(file_name='undergroundempty.txt')
new_map.print_map()