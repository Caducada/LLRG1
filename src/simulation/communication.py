from .map import Map
from .submarine import Submarine


def share_position(map: Map) -> None:
    for sub in map.fleet:
        for i in range(len(map.fleet)):
            if i != sub.id:
                safe_point = str(map.fleet[i].temp_y) + str(map.fleet[i].temp_x)
                sub.remove_duplicate_subs(safe_point=safe_point, sub_index=sub.id)
    for sub in map.fleet:
        if not len(sub.sub_list):
            for i in range(len(map.fleet)):
                if map.fleet[i-1].id != sub.id:
                    sub.sub_list.append(
                        Submarine(id=map.fleet[i-1].id, temp_x=map.fleet[i-1].temp_x, temp_y=map.fleet[i-1].temp_y )
                    )
        else:
            for i in range(len(map.fleet)):
                if map.fleet[i-1].id != sub.id:
                    sub.sub_list[i-1].temp_x = map.fleet[i-1].temp_x
                    sub.sub_list[i-1].temp_y = map.fleet[i-1].temp_y

def share_missile_info(map: Map) -> None:
    for sub in map.fleet:
        if not len(sub.sub_list):
            for i in range(len(map.fleet)):
                if map.fleet[i-1].id != sub.id:
                    sub.sub_list.append(
                        Submarine(id=map.fleet[i-1].id, m_count=map.fleet[i-1].m_count)
                    )
        else:
            for i in range(len(map.fleet)):
                if map.fleet[i-1].id != sub.id:
                    sub.sub_list[i-1].m_count = map.fleet[i-1].m_count


def share_endpoint(map: Map) -> None:
    for sub in map.fleet:
        if not len(sub.sub_list):
            for i in range(len(map.fleet)):
                if map.fleet[i].id != sub.id:
                    sub.sub_list.append(
                        Submarine(
                            id=map.fleet[i-1].id,
                            xe=map.fleet[i-1].xe,
                            ye=map.fleet[i-1].ye,
                            endpoint_reached=map.fleet[i-1].endpoint_reached,
                        )
                    )
        else:
            for i in range(len(map.fleet)):
                if map.fleet[i-1].id != sub.id:
                    sub.sub_list[i-1].xe = map.fleet[i-1].xe
                    sub.sub_list[i-1].ye = map.fleet[i-1].ye
                    sub.sub_list[i-1].endpoint_reached = map.fleet[i-1].endpoint_reached


def request_missiles(sub_id: int, map: Map) -> None:
    for sub in map.fleet:
        if sub.id == sub_id:
            square = sub.get_adjacent_square(sub.temp_x, sub.temp_y)
            client = sub
            break
    if not square:
        return
    for sub in map.fleet:
        if sub.get_client_route(y_goal=int(square[0]), x_goal=int(square[1])):
            if (
                sub.m_count
                - sub.endpoint_missiles_required
                - sub.client_missiles_required
            ) > 0:
                sub.client_id = client.id
                return


def remove_helper(sub_id: int, map: Map) -> None:
    for sub in map.fleet:
        if sub.client_id != None:
            if sub.client_id == sub_id:
                sub.client = None
