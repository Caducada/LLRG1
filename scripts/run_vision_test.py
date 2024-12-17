import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from simulation.map import Map
from simulation.get_fleet import get_fleet


def run_sim(fleet_name:str, map_name:str):
    sim_map = Map(map_name)
    sub_list = get_fleet(fleet_name, sim_map._map)
    for sub in sub_list:
        sub.get_new_route()
        print(sub.planned_route)
        sub.display_vision()
    
if __name__ == "__main__":
    run_sim(fleet_name="simple.txt", map_name="underground.txt")