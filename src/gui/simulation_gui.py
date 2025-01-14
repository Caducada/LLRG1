import pygame
import time
import random
from gui.base_gui import BaseGUI
from simulation.map import Map
from simulation.get_fleet import get_fleet

class SimulationGUI(BaseGUI):
    def handle_events(self):
        super().handle_events()
    """Hantera simuleringens GUI."""
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        """Kör simuleringen."""
        running = True

#        while running:
        self.screen.fill((0, 0, 0))
        # Här lägger du till rendering av simuleringen
        pygame.display.flip()
        sim_map = Map("underground.txt", "simple.txt")

        for sub in sim_map.fleet:
            sub.basic_scan()
            if sub.planned_route[0].split()[0] == "Move":
                sub.move_sub(sub.planned_route[0].split()[1]) 
            elif sub.planned_route[0].split()[0] == "Shoot":
                sub.missile_shoot()
            elif sub.planned_route[0].split()[0] == "Share":
                pass

            action = random.random()
            if action > 0.2:
                sim_map.reduce_rubble(1, 3)

            sim_map.update_map()
            for sub in sim_map.fleet:
                sub.map = sim_map._map
                if sub.endpoint_reached:
                    cleared += 1
                elif not sub.is_alive:
                    cleared += 1
            time.sleep(3)



        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
