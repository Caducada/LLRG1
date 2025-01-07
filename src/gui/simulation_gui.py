import pygame
import time
import random
from simulation.map import Map, get_fleet
from gui.base_gui import BaseGUI

class SimulationGUI:
    """Hantera simuleringens GUI."""
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        """Kör simuleringen."""
        running = True
        sim_map = Map("underground.txt", "simple.txt")

        while running:
            self.screen.fill((0, 0, 0))
            # Här lägger du till rendering av simuleringen
            pygame.display.flip()
            goal_counter = 0
            death_counter = 0
        
            for sub in sim_map.fleet:
                time.sleep(3)
                sub.basic_scan()
                sub.get_new_route()
                sub.move_sub(sub.planned_route[0])
                sim_map.update_map()
                sub.map = sim_map._map
                sub.basic_scan()   
                sub.display_vision()

                action = random.random()
                if action > 0.2:
                    sim_map.reduce_rubble(1, 3)
                    sim_map.update_map()
                    sub.map = sim_map._map
                    
                action = random.random()
                if action > 0.8:
                    sub.missile_shoot()

                if sub.endpoint_reached:
                    goal_counter += 1
                elif not sub.is_alive:
                    death_counter += 1
                sim_map.print_map()

                # handle_events()
                # update()
                # render()
                pygame.display.flip()
        

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False