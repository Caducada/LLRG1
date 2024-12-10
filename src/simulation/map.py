import os
import csv
import itertools

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAP_DIR = os.path.join(BASE_DIR, "data", "maps/")
SUB_DIR = os.path.join(BASE_DIR, "data", "fleets/")

class Map:
    def __init__(self, file_name='', x=10, y=10) -> None:
        '''
            Skapar en karta efter kartfil och lägger till ubåtar, 
            om ingen kartfil anges skapas en tom karta
        '''
        if file_name == '':
            self.create_empty_map(x, y)
            # self.read_sub_coords(file='uboat.txt')
        else:
            self._file_name = file_name
            self._map = self.read_map_file(file_name)
            self._map = self._map[::-1]
            self.read_sub_coords(file='uboat.txt')


    def print_map(self):
        temp_map = self._map[::-1]
        for row in temp_map:
            print(' '.join(map(str, row)))
            # print(f'{row}')


    def valid_map(self, map):
        for row in map:
            for col in row:
                if col not in ['x', 'B', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    print(col)
                    return False
        return True


    def read_map_file(self, file: str):
        '''Läser in en kartfil och kontrollerar att bara giltiga tecken finns med'''
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
                reader = csv.reader(csvfile, delimiter=',')
                map = []
                for row in reader:
                    map.append([int(char) if char.isdigit() else char for char in row])
                    
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
      
    def read_sub_coords(self, file: str):
        '''Läser in ubåtarnas koordinater och lägger in i kartan'''
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
                    # print(f'Uboat: {row[0]}:{row[1]}')
                    # print(f'Cell: {self._map[int(row[0])][int(row[1])]}')
                    if self._map[int(row[0])][int(row[1])] == 0:
                        self.modify_cell(int(row[0]), int(row[1]), 'U')
                    
        except Exception as e:
            print(f'{e}')
            

    def modify_cell(self, x, y, value):
        """Modifierar en cell på kartan."""
        if 0 <= y < len(self._map) and 0 <= x < len(self._map[0]):
            self._map[y][x] = value
        else:
            print("Invalid coordinates")


    def get_scan_info(self, x, y):
        scan_info = {'up': '', 'down': '', 'left': '', 'right': ''}
        if x >= len(self._map[0]) or y >= len(self._map) or x < 0 or y < 0:
            print("Invalid coordinates")
            return
        if x == 0:
            scan_info['left'] = ''
            scan_info['right'] = self._map[y][x+1]
        if x == len(self._map[0])-1:
            scan_info['right'] = ''
            scan_info['left'] = self._map[y][x-1]
        if y == 0:
            scan_info['up'] = ''
            scan_info['down'] = self._map[y+1][x]
        if y == len(self._map)-1:
            scan_info['up'] = self._map[y-1][x]
            scan_info['down'] = ''

        if 0 < y and y < len(self._map[0])-1:
            scan_info['up'] = self._map[y-1][x]
            scan_info['down'] = self._map[y+1][x]

        if 0 < x and x < len(self._map)-1:
            scan_info['left'] = self._map[y][x-1]
            scan_info['right'] = self._map[y][x+1]

        return scan_info


# Exempel

# Läser in kartfil
new_map = Map(file_name='underground.txt')
new_map.print_map()
# print(new_map._map[1][1])
# print(new_map.get_scan_info(1, 1))
# print('----------------------')
# print(new_map._map[6][9])
# print(new_map.get_scan_info(10, 1))
# print('----------------------')
# print(new_map._map[3][1])
# print(new_map.get_scan_info(3, 1))
# print('----------------------')
# print(new_map._map[3][0])
# print(new_map.get_scan_info(3, 0))
# print('----------------------')
# print(new_map._map[9][0])
# print(new_map.get_scan_info(9, 0))

# Skapar tom karta med angiven storlek
# new_map = Map(x=20, y=20)
# new_map.print_map()
