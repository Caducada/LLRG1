import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from simulation.map import Map

def run_sim(fleet_name:str, map_name:str):    
    sim_map = Map(map_name, fleet_name)
    has_run = False
    for sub in sim_map.fleet:
        while True:
            if not has_run:
                time.sleep(3)
                sub.basic_scan()
                sub.display_vision()
                print(sub.planned_route)
                has_run = True
            time.sleep(3)
            sub.move_sub(sub.planned_route[0])
            sub.basic_scan()
            sub.display_vision()
            print(sub.planned_route)
            if sub.endpoint_reached:
                print(f"Endpoint reached for sub {sub.id}!")
                break

        
if __name__ == "__main__":
    run_sim(fleet_name="simple.txt", map_name="underground.txt")