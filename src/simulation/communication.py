from .map import Map

def share_position(sub_id:int, map:Map) -> None:
    for sub in map.fleet:
        if sub_id == sub.id:
            safe_point = str(sub.temp_y) + str(sub.temp_x)
            break
    for sub in map.fleet:
        if sub.id != sub_id:
            sub.remove_duplicate_subs(safe_point=safe_point, sub_index=sub_id)