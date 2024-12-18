import os
from .submarine import Submarine


def get_fleet(fleet_name: str, map: list) -> list[Submarine]:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SUB_DIR = os.path.join(BASE_DIR, "data", "fleets/")
    SUB_FILE = os.path.join(SUB_DIR, fleet_name)
    sub_list = []
    with open(SUB_FILE, "r") as fleet:
        counter = 0
        for line in fleet.readlines():
            if line.split(",")[2].replace(" ", "").isnumeric():
                try:
                    temp_x0 = int(line.split(",")[0].replace(" ", ""))
                except IndexError:
                    temp_x0 = 1
                try:
                    temp_y0 = int(line.split(",")[1].replace(" ", ""))
                except IndexError:
                    temp_y0 = 1
                try:
                    temp_xe = int(line.split(",")[2].replace(" ", ""))
                except IndexError:
                    temp_xe = 1
                try:
                    temp_ye = int(line.split(",")[3].replace(" ", ""))
                except IndexError:
                    temp_ye = 1
                try:
                    temp_missiles = int(line.split(",")[4].replace(" ", ""))
                except IndexError:
                    temp_missiles = 1
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
    return sub_list