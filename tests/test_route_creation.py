import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from simulation.map import Map
from simulation.submarine import Submarine


def main():
    my_map = Map()._map
    for line in my_map:
        if not len(line):
            my_map.remove(line)
    my_sub = Submarine(
        id=1, map_width=10, map_height=10, map=my_map, y0=8, x0=1, ye=8, xe=3
    )
    my_sub.get_new_route()
    print(my_sub.planned_route)


if __name__ == "__main__":
    main()
