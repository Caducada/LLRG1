import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from simulation.map import Map

def run_test(fleet_name: str, map_name: str):
    sim_map = Map(map_name, fleet_name)
    goal_counter = 0
    death_counter = 0
    while goal_counter <= len(sim_map.fleet) and death_counter <= len(sim_map.fleet):
        for sub in sim_map.fleet:
                time.sleep(3)
                sub.basic_scan()
                sub.get_new_route()
                sub.move_sub(sub.planned_route[0])
                sub.basic_scan()   
        sim_map.update_map()
        for sub in sim_map.fleet:
            sub.map = sim_map._map
            if sub.endpoint_reached:
                print(f"Endpoint reached for sub {sub.id}!")
                goal_counter += 1
            elif not sub.is_alive:
                death_counter += 1
        sim_map.print_map()
            


if __name__ == "__main__":
    run_test(fleet_name="collision.txt", map_name="collision.txt")
    # run_test(fleet_name="simple.txt", map_name="underground.txt")
    
