from simulation.map import Map
from simulation.get_fleet import get_fleet
from simulation.communication import general_share, normal_share
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
        

    def decide(self):
        """Ubåtar fattar beslut om sina handlingar och hanterar blockeringar."""
        normal_share(self.map)
        for sub in self.active_fleet:
            sub.basic_scan()
            sub.update_path()

        if sub.planned_route[0].split()[0] == "Move":
            sub.move_sub(sub.planned_route[0].split()[1])
        elif sub.planned_route[0].split()[0] == "Shoot":
            sub.missile_shoot()
            self.map.missile_hits(
                sub.id, sub.temp_x, sub.temp_y, sub.planned_route[0].split()[1]
            )
        elif sub.planned_route[0].split()[0] == "Scan":
            sub.general_scan(sub.planned_route[0].split()[1])
        elif sub.planned_route[0].split()[0] == "Share":
            general_share(sub.planned_route[0].split()[1], sub, self.map)

    def execute(self):
        """Utför förändringar efter alla handlingar och uppdaterar status."""
        self.map.update_map()

        for sub in self.fleet:
            sub.map = self.map._map  


    def step(self):
        """Utför en cykel i simuleringen."""
        if self.max_cycles and self.cycle_count >= self.max_cycles:
            print("Simulation stopped: reached maximum cycle count.")
            return
        
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