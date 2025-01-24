import random
import string
from .map import Map
from .submarine import Submarine


def general_share(share_type, giver_sub: Submarine, map: Map):
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
                                temp_sub.static += 1
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


def share_missiles(giver_sub: Submarine, map: Map) -> None:
    """Ger överblibna missiler till en ubåt"""

    if giver_sub.client_id == None:
        print("Error! Can't share missiles with no asigned client")
        return

    adjacent_subs = []

    for i in range(len(giver_sub.vision)):
        for j in range(len(giver_sub.vision[i])):
            if (
                str(giver_sub.vision[i][j])[0] == "U"
                and map._map[i][j] == giver_sub.vision[i][j]
            ):
                if i == giver_sub.temp_y + 1 and j == giver_sub.temp_x:
                    adjacent_subs.append(giver_sub.vision[i][j][1])
                if i == giver_sub.temp_y - 1 and j == giver_sub.temp_x:
                    adjacent_subs.append(giver_sub.vision[i][j][1])
                if i == giver_sub.temp_y and j == giver_sub.temp_x + 1:
                    adjacent_subs.append(giver_sub.vision[i][j][1])
                if i == giver_sub.temp_y and j == giver_sub.temp_x + 1:
                    adjacent_subs.append(giver_sub.vision[i][j][1])

    if not len(adjacent_subs):
        for sub in giver_sub.sub_list:
            if sub.id == giver_sub.client_id:
                sub.static = 0
        return

    missiles_shared = giver_sub.m_count - giver_sub.endpoint_missiles_required
    giver_sub.m_count -= missiles_shared

    for adjacent_id in adjacent_subs:
        for sub in giver_sub.sub_list:
            if sub.id == int(adjacent_id):
                client = sub

    for sub in map.fleet:
        if sub.id == client.id:
            sub.m_count += missiles_shared
    
    print(f"Sub {giver_sub.id} gave {missiles_shared} missiles to sub {adjacent_id}")


def share_vision(giver_sub: Submarine, map: Map) -> None:
    """Ger sin uppfattning av världen till en ubåt"""

    if giver_sub.client_id == None:
        print("Error! Can't share vision with no asigned client")
        return

    adjacent_subs = []

    for i in range(len(giver_sub.vision)):
        for j in range(len(giver_sub.vision[i])):
            if (
                str(giver_sub.vision[i][j])[0] == "U"
                and map._map[i][j] == giver_sub.vision[i][j]
            ):
                if i == giver_sub.temp_y + 1 and j == giver_sub.temp_x:
                    adjacent_subs.append(giver_sub.vision[i][j][1])
                if i == giver_sub.temp_y - 1 and j == giver_sub.temp_x:
                    adjacent_subs.append(giver_sub.vision[i][j][1])
                if i == giver_sub.temp_y and j == giver_sub.temp_x + 1:
                    adjacent_subs.append(giver_sub.vision[i][j][1])
                if i == giver_sub.temp_y and j == giver_sub.temp_x + 1:
                    adjacent_subs.append(giver_sub.vision[i][j][1])

    if not len(adjacent_subs):
        for sub in giver_sub.sub_list:
            if sub.id == giver_sub.client_id:
                sub.static = 0
        return


    for adjacent_id in adjacent_subs:
        for sub in map.fleet:
            if sub.id == int(adjacent_id):
                client = sub
                
    for sub in map.fleet:
        if sub.id == client.id:
            for temp_sub in sub.sub_list:
                if temp_sub.id == giver_sub.id:
                    temp_sub.vision = giver_sub.vision
                    
    for sub in map.fleet:
        if sub.id == giver_sub.id:
            for temp_sub in sub.sub_list:
                if temp_sub.id == client.id:
                    temp_sub.vision = client.vision
    print(f"Sub {giver_sub.id} and  sub {adjacent_id} shared map info with eachother")


def share_secret(giver_sub: Submarine, map: Map) -> None:
    """Ger en hemlig nyckel till en annan ubåt"""
    if giver_sub.client_id == None:
        print("Error! Can't share secret with no asigned client")
        return
    secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    adjacent_subs = []

    for i in range(len(giver_sub.vision)):
        for j in range(len(giver_sub.vision[i])):
            if (
                str(giver_sub.vision[i][j])[0] == "U"
                and map._map[i][j] == giver_sub.vision[i][j]
            ):
                if i == giver_sub.temp_y + 1 and j == giver_sub.temp_x:
                    adjacent_subs.append(giver_sub.vision[i][j][1])
                if i == giver_sub.temp_y - 1 and j == giver_sub.temp_x:
                    adjacent_subs.append(giver_sub.vision[i][j][1])
                if i == giver_sub.temp_y and j == giver_sub.temp_x + 1:
                    adjacent_subs.append(giver_sub.vision[i][j][1])
                if i == giver_sub.temp_y and j == giver_sub.temp_x + 1:
                    adjacent_subs.append(giver_sub.vision[i][j][1])

    if not len(adjacent_subs):
        for sub in giver_sub.sub_list:
            if sub.id == giver_sub.client_id:
                sub.static = 0
        return


    for adjacent_id in adjacent_subs:
        for sub in giver_sub.sub_list:
            if sub.id == int(adjacent_id):
                sub.secret_key = secret_key
                
    for sub in map.fleet:
        if sub.id == adjacent_id:
            for temp_sub in sub.sub_list:
                if int(temp_sub.id) == giver_sub.id:
                    temp_sub.secret_key = secret_key
                    
    print(f"Sub {giver_sub.id} and sub {adjacent_id} shared the secret key: {secret_key}")