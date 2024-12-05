import os
import csv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAP_DIR = os.path.join(BASE_DIR, "data", "maps/")
SUB_DIR = os.path.join(BASE_DIR, "data", "fleets/")

class Map:
    def __init__(self, file_name = "underground.txt") -> None:
        self._file_name = file_name
        self._map = self.read_map_file(file_name)
        self.read_sub_coords(file='uboat.txt')

    def print_map(self):
        for row in self._map:
            print(' '.join(map(str, row)))


    def convert_digits(self, value):
        if value.isdigit():
            return int(value)
        return value


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

    def read_sub_coords(self, file: str):
        SUB_FILE = os.path.join(SUB_DIR, file)
        sub_coords = []

        if not os.path.exists(SUB_FILE):
            print(f'File {file} not found')

        if os.path.getsize(SUB_FILE) == 0:
            print(f'File {file} is empty')
            
        try:
            with open(SUB_FILE, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)

                for row in reader:
                    print(f'Uboat: {row[0]}:{row[1]}')
                    if self._map[int(row[0])][int(row[1])] == 0:
                        self._map[int(row[0])][int(row[1])] = 'U'

        except Exception as e:
            print(f'{e}')


new_map = Map(file_name='underground.txt')
new_map.print_map()