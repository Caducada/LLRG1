import random
import string
from .map import Map
from .submarine import Submarine


def general_share(share_type, giver_sub: Submarine, map: Map):
    if share_type == "missiles":
        share_missiles(giver_sub, map)
    elif share_type == "vision":
        share_vision(giver_sub, map)
    elif share_type == "secret":
        share_secret(giver_sub, map)


def normal_share(map: Map, cycle_count:int) -> None:
    """Tryckte ihop all 'gratis' kommunikation mellan ubåtar till en funktion för att förbättra prestandan"""
    for sub in map.fleet:
        for temp_sub in sub.sub_list:
            if cycle_count != 0:
                if sub.id != temp_sub.id:
                    if (
                        temp_sub.temp_x == sub.temp_x
                        and temp_sub.temp_y == sub.temp_y
                        and not temp_sub.endpoint_reached
                    ):
                        temp_sub.static += 1
                    else:
                        temp_sub.static = 0
                    temp_sub.prev_x = temp_sub.temp_x
                    temp_sub.prev_y = temp_sub.prev_y
                    temp_sub.temp_x = sub.temp_x
                    temp_sub.temp_y = sub.temp_y
                    temp_sub.is_alive = sub.is_alive
                    temp_sub.m_count = sub.m_count
                    temp_sub.xe = sub.xe
                    temp_sub.ye = sub.ye
                    temp_sub.endpoint_reached = sub.endpoint_reached
                if temp_sub.secret_key != None:
                    for real_sub in map.fleet:
                        if real_sub.id == temp_sub.id:
                            temp_sub.planned_route = sub.planned_route
            else:
                sub.sub_list.append(
                    Submarine(
                        id=sub.id,
                        temp_x=sub.temp_x,
                        temp_y=sub.temp_y,
                        m_count=sub.m_count,
                        xe = sub.xe,
                        ye = sub.ye,
                        endpoint_reached=sub.endpoint_reached
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