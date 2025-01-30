from simulation.map import Map
from simulation.get_fleet import get_fleet
from simulation.communication import general_share
import time
import os

class Simulation:
    def __init__(self, map_file, fleet_file, max_cycles=None):
        """Initierar simuleringen med en karta och en lista av ubåtar."""
        self.map = Map(file_name=map_file, sub_file_name=fleet_file)
        self.fleet = self.map.fleet
        self.active_fleet = [sub for sub in self.fleet if sub.is_alive]
        self.cleared = set()
        self.cycle_count = 0
        self.max_cycles = max_cycles
        
    def prepare(self):
        """Utför förberedelser för en ny cykel och optimerar datadelning."""
        for sub in self.active_fleet:
            if sub.is_alive:
                sub.basic_scan()
                
                if sub.position_changed:
                    general_share("position", sub, self.map)
                    sub.position_changed = False 

                if sub.missile_count_changed:
                    general_share("missile_info", sub, self.map)
                    sub.missile_count_changed = False 

                if sub.endpoint_changed:
                    general_share("endpoint", sub, self.map)
                    sub.endpoint_changed = False  
        self.map.update_paths()

    def decide(self):
        """Ubåtar fattar beslut om sina handlingar och hanterar blockeringar."""
        for sub in self.active_fleet:
            if not sub.is_alive:
                sub.planned_route.clear() 
                continue

            if sub.endpoint_reached:
                if sub.planned_route:  
                    action = sub.planned_route[0]
                    action_type = action.split()[0]
                    if action_type == "Scan":
                        sub.general_scan(action.split()[1])
                    elif action_type == "Share":
                        general_share(action.split()[1], sub, self.map)
                continue 

            if sub.planned_route:
                action = sub.planned_route[0]
                action_type = action.split()[0]

                if action_type == "Move":
                    next_x, next_y = sub.get_next_position(action.split()[1])
                    blocking_sub = sub.find_sub_at(next_x, next_y)

                    if blocking_sub:
                        if blocking_sub.is_alive:

                            general_share("position", blocking_sub, self.map)
                            
                            if sub.m_count > 0:
                                sub.planned_route.appendleft(f"Shoot {action.split()[1]}")
                            else:
                                sub.planned_route.appendleft(f"Move {action.split()[1]}")
                        continue  

                    sub.move_sub(action.split()[1])

                elif action_type == "Shoot":
                    sub.missile_shoot()
                    self.map.missile_hits(sub.id, sub.temp_x, sub.temp_y, action.split()[1])

                elif action_type == "Scan":
                    sub.general_scan(action.split()[1])

                elif action_type == "Share":
                    general_share(action.split()[1], sub, self.map)

    def execute(self):
        """Utför förändringar efter alla handlingar och uppdaterar status."""
        self.map.update_map()

        for sub in self.fleet:
            sub.map = self.map._map  

            if sub not in self.cleared:
                if sub.endpoint_reached or not sub.is_alive:
                    if not sub.is_alive:  # 🚨 UBÅTEN DÖR
                        pos = (sub.temp_x, sub.temp_y)

                        if pos not in self.map.dead_sub_positions.values():
                            self.map.dead_sub_positions[sub.id] = pos
                        else:
                            self.map.dead_sub_positions[sub.id] = pos 

                        if (sub.xe, sub.ye) in self.map.endpoint_positions:
                            self.map.endpoint_positions.remove((sub.xe, sub.ye))

                    self.cleared.add(sub)

                    if (sub.xe, sub.ye) in self.map.endpoint_positions:
                        self.map.endpoint_positions.remove((sub.xe, sub.ye))
                        self.map.modify_cell(sub.xe, sub.ye, "0")
    def step(self):
        """Utför en cykel i simuleringen."""
        if self.max_cycles and self.cycle_count >= self.max_cycles:
            print("Simulation stopped: reached maximum cycle count.")
            return
        
        
        self.prepare()
        self.decide()
        self.execute()
        
        self.cycle_count += 1
        
        if self.max_cycles and self.cycle_count >= self.max_cycles:
            print("Simulation stopped due to reaching max cycles.")

    def run(self, display=True):
        os.system("cls" if os.name == "nt" else "clear")
        self.map.update_map()
        if display:
            self.map.print_map()
            print("<------------------->")

        while len(self.cleared) < len(self.fleet):
            if self.max_cycles and self.cycle_count >= self.max_cycles:
                print("Simulation stopped: reached maximum cycle count.")
                break

            self.step()
            time.sleep(0.1)  # SNABBARE SIMULERING
            if display:
                os.system("cls" if os.name == "nt" else "clear")
                self.map.print_map()
                print("<------------------->")

        print("Simulation complete!")

    def translate_visual_coordinates(self, x, y):
        """Översätter interna koordinater (indexering) till visuella koordinater."""
        map_height = len(self.map._map)
        translated_y = map_height - 1 - y
        return x, translated_y

    def is_simulation_complete(self):
        """Kontrollerar om alla ubåtar har nått sitt mål eller dött."""
        return len(self.cleared) == len(self.fleet)

    def get_map(self):
        """Returnerar den aktuella kartan."""
        return self.map._map

    def get_fleet(self):
        """Returnerar alla ubåtar."""
        return self.fleet

    def get_active_fleet(self):
        """Returnerar endast aktiva ubåtar."""
        return self.active_fleet