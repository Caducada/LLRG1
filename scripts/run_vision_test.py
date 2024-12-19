import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from simulation.map import Map
from simulation.get_fleet import get_fleet

def run_sim(fleet_name:str, map_name:str):    
    sim_map = Map(map_name)
    sub_list = get_fleet(fleet_name, sim_map._map)
    has_run = False
    for sub in sub_list:
        while True:
            if not has_run:
                time.sleep(3)
                sub.basic_scan()
                sub.display_planned_route()
                has_run = True
            time.sleep(3)
            sub.basic_scan()
            sub.display_vision()
            sub.display_planned_route()
            sub.move_sub(sub.planned_route[0])
            if sub.endpoint_reached:
                sub.display_vision()
                print(f"Endpoint reached for sub {sub.id}!")
                break

        
if __name__ == "__main__":
    run_sim(fleet_name="simple.txt", map_name="underground.txt")