
from simulation.map import Map
from simulation.get_fleet import get_fleet
import random


def runsim(fleet_name:str, map_name:str):
    running = True
    sim_map = Map(map_name, fleet_name)
    print(f'fleet_name: {fleet_name}')
    print(f'map_name  : {map_name}')
    sub_list = get_fleet(fleet_name, sim_map._map)
    for sub in sub_list:
        print(f'Antal missiler: {sub.m_count}')
        sub.basic_scan()
        while running and len(sub.planned_route) > 0:
            print(sub.planned_route)
            sub.display_vision()
            cur_move = sub.planned_route.pop(0)
            sub.move_sub(cur_move)

            action = random.random()
            if action > 0.2:
                sim_map.reduce_rubble(1, 3)

            action = random.random()
            if action > 0.8:
                if sub.missile_shoot():
                    print(f'Missil avfyrad')
                    print(f'Antal missiler kvar: {sub.m_count}')
            
            input("Press any key")



if __name__ == "__main__":
    runsim(fleet_name="simple.txt", map_name="underground.txt")

