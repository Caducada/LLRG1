import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from simulation.map import Map
from simulation.communication import share_position, share_missile_info, share_endpoint

def prepare(sim_map:Map):
    for sub in sim_map.fleet:
        share_position(sub, sim_map)
        share_missile_info(sub, sim_map)
        share_endpoint(sub, sim_map) 
        sub.basic_scan() 
        
def decide(sim_map:Map):
    for sub in sim_map.fleet:
        if sub.planned_route[0].split()[0] == "Move":
            sub.move_sub(sub.planned_route[0].split()[1])
        elif sub.planned_route[0].split()[0] == "Shoot":
            sub.missile_shoot()
        elif sub.planned_route[0].split()[0] == "Scan":
            if sub.planned_route[0].split()[1] == "basic":
                sub.basic_scan()
            elif sub.planned_route[0].split()[1] == "advanced":
                sub.advanced_scan()
    
def execute(sim_map:Map, cleared: set):
    sim_map.update_map()
    for sub in sim_map.fleet:
        sub.map = sim_map._map
        if sub in cleared and not sub.endpoint_reached and sub.is_alive:
            cleared.remove(sub)
        if sub.endpoint_reached:
            cleared.add(sub)
        elif not sub.is_alive:
            cleared.add(sub)
    return cleared
    

def run_test(sim_map: Map) -> None:
    """Funktion för att testa olika kartor"""
    cleared = set()
    sim_map.update_map()
    sim_map.print_map()
    while len(cleared) != len(sim_map.fleet):
        prepare(sim_map)
        decide(sim_map)
        cleared = execute(sim_map, cleared)
        time.sleep(3)
        sim_map.print_map()
        print("<------------------->")


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    run_test(Map(file_name="help.txt", sub_file_name="help.txt"))
    # run_test(Map(file_name="underground.txt", sub_file_name="collision.txt"))
    # run_test(Map(file_name="underground.txt", sub_file_name="simple.txt"))
