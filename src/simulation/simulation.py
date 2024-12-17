
from simulation.map import Map
from simulation.get_fleet import get_fleet


def runsim(fleet_name:str, map_name:str):
    running = True
    sim_map = Map(map_name)
    sub_list = get_fleet(fleet_name, sim_map._map)
    for sub in sub_list:
        sub.basic_scan()
        while running and len(sub.planned_route) > 0:
            print(sub.planned_route)
            sub.display_vision()
            cur_move = sub.planned_route.pop(0)
            sub.move_sub(cur_move)
            
            input("Press any key")
        
if __name__ == "__main__":
    runsim(fleet_name="simple.txt", map_name="underground.txt")

