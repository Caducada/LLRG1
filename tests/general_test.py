import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from simulation.map import Map
from simulation.communication import share_position

def run_test(sim_map:Map) -> None:
    """Funktion för att testa olika kartor"""
    cleared = set()
    while len(cleared) != len(sim_map.fleet):
        for sub in sim_map.fleet:
            if sub.bool_scan:
                sub.advanced_scan()
                sub.bool_scan = False
            else:
                sub.basic_scan()
                if sub.planned_route[0].split()[0] == "Move":
                    sub.move_sub(sub.planned_route[0].split()[1]) 
                elif sub.planned_route[0].split()[0] == "Shoot":
                    sub.missile_shoot()
                elif sub.planned_route[0].split()[0] == "Share":
                    if sub.planned_route[0].split()[1] == "position":
                        share_position(sub.id, sim_map)
                sub.bool_scan = True
            # sub.display_vision()
            # print(sub.planned_route)
            # print("<------------------->")
        sim_map.update_map()
        for sub in sim_map.fleet:
            sub.map = sim_map._map
            if sub.endpoint_reached:
                cleared.add(sub)
            elif not sub.is_alive:
                cleared.add(sub)
        time.sleep(3)
        sim_map.print_map()
        print("<------------------->")
            


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    run_test(Map(file_name="underground.txt", sub_file_name="collision.txt"))
    # run_test(Map(file_name="underground.txt", sub_file_name="simple.txt"))
    
