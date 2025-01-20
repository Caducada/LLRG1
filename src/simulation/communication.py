from .map import Map
from .submarine import Submarine

def general_share(share_type, giver_sub:Submarine, map:Map):
    if share_type == "position":
        share_position(giver_sub, map)
    elif share_type == "missile_info":
        share_missile_info(giver_sub, map)
    elif share_type == "endpoint":
        share_endpoint(giver_sub, map)
    elif share_type == "missiles":
        share_missiles(giver_sub, map)
    elif share_type == "vision":
        share_vision(giver_sub, map)
    elif share_type == "secret":
        share_secret(giver_sub, map)
    

def share_position(giver_sub: Submarine, map: Map) -> None:
    """Delar sin position med de övriga ubåtarna"""
    for sub in map.fleet:
        if sub.is_alive:
            if sub.id != giver_sub.id:
                create_sub = True
                for temp_sub in sub.sub_list:
                    if temp_sub:
                        if temp_sub.id == giver_sub.id:
                            create_sub = False
                if not create_sub:
                    for temp_sub in sub.sub_list:
                        if temp_sub.id == giver_sub.id:
                            if (
                                temp_sub.temp_x == giver_sub.temp_x
                                and temp_sub.temp_y == giver_sub.temp_y
                                and not temp_sub.endpoint_reached
                            ):
                                temp_sub.static +=1
                            else:
                                temp_sub.static = 0
                            temp_sub.prev_x = temp_sub.temp_x
                            temp_sub.prev_y = temp_sub.prev_y
                            temp_sub.temp_x = giver_sub.temp_x
                            temp_sub.temp_y = giver_sub.temp_y
                else:
                    sub.sub_list.append(
                        Submarine(
                            id=giver_sub.id,
                            temp_x=giver_sub.temp_x,
                            temp_y=giver_sub.temp_y,
                        )
                    )
        sub.update_vision()


def share_missile_info(giver_sub: Submarine, map: Map) -> None:
    """Delar antalet missiler med de övriga ubåtarna"""
    for sub in map.fleet:
        if sub.is_alive:
            if sub.id != giver_sub.id:
                create_sub = True
                for temp_sub in sub.sub_list:
                    if temp_sub:
                        if temp_sub.id == giver_sub.id:
                            create_sub = False
                if not create_sub:
                    for temp_sub in sub.sub_list:
                        if temp_sub.id == giver_sub.id:
                            temp_sub.m_count = giver_sub.m_count
                else:
                    sub.sub_list.append(
                        Submarine(id=giver_sub.id, m_count=giver_sub.m_count)
                    )


def share_endpoint(giver_sub: Submarine, map: Map) -> None:
    """Delar info om slutpositionen med de övriga ubåtarna"""
    for sub in map.fleet:
        if sub.is_alive:
            if sub.id != giver_sub.id:
                create_sub = True
                for temp_sub in sub.sub_list:
                    if temp_sub:
                        if temp_sub.id == giver_sub.id:
                            create_sub = False
                if not create_sub:
                    for temp_sub in sub.sub_list:
                        if temp_sub.id == giver_sub.id:
                            temp_sub.xe = giver_sub.xe
                            temp_sub.ye = giver_sub.ye
                            temp_sub.endpoint_reached = giver_sub.endpoint_reached
                else:
                    sub.sub_list.append(
                        Submarine(
                            id=giver_sub.id,
                            xe=giver_sub.xe,
                            ye=giver_sub.ye,
                            endpoint_reached=giver_sub.endpoint_reached,
                        )
                    )
                    
def share_missiles(giver_sub: Submarine, map: Map):
    """Ger överblibna missiler till en ubåt"""
    pass
    
def share_vision(giver_sub: Submarine, map: Map):
    """Ger sin uppfattning av världen till en ubåt"""
    pass

def share_secret(giver_sub: Submarine, map: Map):
    """Ger en hemlig nyckel till en annan ubåt"""
    pass