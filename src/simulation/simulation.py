from simulation.map import Map
from simulation.get_fleet import get_fleet

class Simulation:
    def __init__(self, map_file, fleet_file):
        """Initierar simuleringen med en karta och en lista av ubåtar."""
        self.map = Map(file_name=map_file)
        self.fleet = get_fleet(fleet_file, self.map._map)
        self.active_fleet = [sub for sub in self.fleet if sub.is_alive]
        self.cycle_count = 0

        
    def step(self):
        """Utför en simulering av ett steg."""
        for submarine in self.active_fleet[:]:  # Skapa en kopia av listan för säker iteration
            submarine.basic_scan()
            if submarine.planned_route:
                action = submarine.planned_route.pop(0)
                if "Move" in action:
                    direction = action.split()[1]
                    submarine.move_sub(direction)

            if submarine.endpoint_reached:
                if submarine in self.active_fleet:
                    print(f"Ubåt {submarine.id} har nått sitt mål")
                    self.active_fleet.remove(submarine)
            elif not submarine.is_alive:
                if submarine in self.active_fleet:
                    print(f"Ubåt {submarine.id} har dött")
                    self.active_fleet.remove(submarine)
                    
        self._update_map()

    def _update_map(self):
        """Uppdaterar kartan baserat på ubåtarnas positioner och andra förändringar."""
        self.map.update_map()
        for submarine in self.fleet:
            submarine.map = self.map._map 

    def _handle_share_action(self, submarine, action):
        """Hanterar 'Share' kommandon för ubåtar."""
        if action == "Share position":
            for other_sub in self.fleet:
                if other_sub != submarine:
                    other_sub.get_vision_from_sub(submarine.id, submarine.vision)
        elif action == "Share vision":
            for other_sub in self.fleet:
                if other_sub != submarine:
                    other_sub.get_vision_from_sub(submarine.id, submarine.vision)

    def is_valid_destination(self, x, y):
        """Kontrollerar om slutdestinationen är giltig."""
        invalid_cells = {"x", "B", range(1, 9)}
        cell_value = self.map.get_cell_value(x, y)
        return cell_value not in invalid_cells and cell_value is not None

    def get_map(self):
        """Returnerar den aktuella kartan."""
        return self.map._map

    def get_fleet(self):
        """Returnerar ubåtarnas status."""
        return self.fleet

    def get_active_fleet(self):
        return self.active_fleet

    def is_simulation_complete(self):
        """Kontrollerar om alla ubåtar har nått sitt mål eller dött."""
        return all(sub.endpoint_reached or not sub.is_alive for sub in self.fleet)
