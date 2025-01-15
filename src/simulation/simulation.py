
from simulation.map import Map
from simulation.get_fleet import get_fleet
import random
import time

def runsim(fleet_name:str, map_name:str):
    running = True
    sim_map = Map(map_name, fleet_name)
    print(f'fleet_name: {fleet_name}')
    print(f'map_name  : {map_name}')
    sub_list = get_fleet(fleet_name, sim_map._map)
    sim_map.print_map()
    while running:
        for sub in sub_list:
            sub.is_alive = True
            sub.basic_scan()
            print(f'Sub: {sub.id}')
            print(f'Antal missiler: {sub.m_count}')
            # for pr in sub.planned_route[0]:
            #     print(f'sub_planned_route: {pr}')
            print(f'sub_planned_route: {sub.planned_route[0].split()[0]}')
            print(f'sub_planned_route: {sub.planned_route[0].split()[1]}')
            input("Press any key")
            print(f'sub x:y {sub.x0}:{sub.y0}')
            sim_map.print_map()
            if sub.planned_route[0].split()[0] == "Move":
                sub.move_sub(sub.planned_route[0].split()[1]) 
            elif sub.planned_route[0].split()[0] == "Shoot":
                sim_map.missile_hits(sub.id, sub.x0, sub.y0, sub.planned_route[0].split()[1])
            
        print(f'Missile hits: {sim_map.missile_hits_dict}')

        sim_map.update_map()
        sim_map.print_map()



if __name__ == "__main__":
    runsim(fleet_name="uboat.txt", map_name="collision.txt")

