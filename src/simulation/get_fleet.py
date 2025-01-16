import os
from .submarine import Submarine

def get_fleet(fleet_name: str, map: list) -> list[Submarine]:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SUB_DIR = os.path.join(BASE_DIR, "data", "fleets/")
    SUB_FILE = os.path.join(SUB_DIR, fleet_name)

    if not os.path.isfile(SUB_FILE):
        raise FileNotFoundError(f"File {SUB_FILE} not found")
    
    sub_list = []
    map_height = len(map)
    map_width = len(map[0]) if map_height > 0 else 0

    with open(SUB_FILE, "r") as fleet:
        counter = 0
        for line_no, line in enumerate(fleet):
            if line_no == 0 and not line[0].isdigit():
                continue
            parts = [p.strip() for p in line.split(",")]
            try:
                temp_x0 = int(parts[0])
                temp_y0 = int(parts[1])
                temp_xe = int(parts[2])
                temp_ye = int(parts[3])
                temp_missiles = int(parts[4]) if len(parts) > 4 else 0

                if not (0 <= temp_x0 < map_width and 0 <= temp_y0 < map_height):
                    print(f"Ubåtens startposition ({temp_x0}, {temp_y0}) är utanför kartan och hoppas över.")
                    continue
                if not (0 <= temp_xe < map_width and 0 <= temp_ye < map_height):
                    print(f"Ubåtens slutposition ({temp_xe}, {temp_ye}) är utanför kartan och hoppas över.")
                    continue

                sub_list.append(
                    Submarine(
                        id = counter,
                        x0=temp_x0,
                        y0=temp_y0,
                        xe=temp_xe,
                        ye=temp_ye,
                        m_count=temp_missiles,
                        map=map,
                    )
                )
                counter += 1

            except (IndexError, ValueError) as e:
                print(f"Ogiltig rad i {fleet_name}: {line.strip()} (Error: {e})")
                continue

    return sub_list