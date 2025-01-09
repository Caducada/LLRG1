import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from simulation.map import Map

def run_test(fleet_name: str, map_name: str):
    sim_map = Map(map_name, fleet_name)
    cleared = 0
    while cleared <= len(sim_map.fleet):
        for sub in sim_map.fleet:
                sub.basic_scan()
                sub.move_sub(sub.planned_route[0])  
        sim_map.update_map()
        for sub in sim_map.fleet:
            sub.map = sim_map._map
            if sub.endpoint_reached:
                print(f"Endpoint reached for sub {sub.id}!")
                cleared += 1
            elif not sub.is_alive:
                print(f"Sub {sub.id} has been terminated.")
                cleared += 1
        time.sleep(3)
        sim_map.print_map()
        print("<------------------->")
            


if __name__ == "__main__":
    run_test(fleet_name="collision.txt", map_name="collision.txt")
    # run_test(fleet_name="simple.txt", map_name="underground.txt")
    
