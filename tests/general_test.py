import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from simulation.map import Map

def run_test(sim_map:Map) -> None:
    """Funktion för att testa olika kartor"""
    cleared = 0
    while cleared <= len(sim_map.fleet):
        for sub in sim_map.fleet:
                sub.basic_scan()
                if sub.planned_route[0].split()[0] == "Move":
                    sub.move_sub(sub.planned_route[0].split()[1]) 
                elif sub.planned_route[0].split()[0] == "Shoot":
                    sub.missile_shoot()
                elif sub.planned_route[0].split()[0] == "Share":
                    #Har inte skapat klassen som hanterar interaktioner mellan ubåtar än :(
                    pass
        sim_map.update_map()
        for sub in sim_map.fleet:
            sub.map = sim_map._map
            if sub.endpoint_reached:
                cleared += 1
            elif not sub.is_alive:
                cleared += 1
        time.sleep(3)
        sim_map.print_map()
        print("<------------------->")
            


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    run_test(Map(file_name="underground.txt", sub_file_name="collision.txt"))
    # run_test(Map(file_name="underground.txt", sub_file_name="simple.txt"))
    
