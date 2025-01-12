from .map import Map
from .submarine import Submarine

def share_position(sub_id:int, map:Map) -> None:
    seek_help = True
    for sub in map.fleet:
        if sub_id == sub.id:
            safe_point = str(sub.temp_y) + str(sub.temp_x)
            if sub.endpoint_reached:
                seek_help = False
            break
    for sub in map.fleet:
        if sub.id != sub_id:
            sub.remove_duplicate_subs(safe_point=safe_point, sub_index=sub_id)
    if seek_help:
        assign_helper(sub_id, map)
           
def assign_helper(sub_id:int, map:Map):
    for sub in map.fleet:
        if sub.id == sub_id:
            square = sub.get_adjacent_square()
            client = sub
            break
    if not square:
        return
    for sub in map.fleet:
        if sub.get_client_route(y_goal=int(square[0]), x_goal=int(square[1])):
            if (sub.m_count - sub.endpoint_missiles_required - sub.client_missiles_required) > 0:
                sub.client = client
                return
    