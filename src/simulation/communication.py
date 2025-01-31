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


def normal_share(map: Map) -> None:
    """Tryckte ihop all 'gratis' kommunikation mellan ubåtar till en funktion för att förbättra prestandan"""
    for sub in map.fleet:
        sub.sub_list = []
        for append_sub in map.fleet:
            if append_sub.id != sub.id:
                sub.sub_list.append(
                    Submarine(
                        id=append_sub.id,
                        temp_x=append_sub.temp_x,
                        temp_y=append_sub.temp_y,
                        prev_x=append_sub.prev_x,
                        prev_y=append_sub.prev_y,
                        m_count=append_sub.m_count,
                        xe = append_sub.xe,
                        ye = append_sub.ye,
                        endpoint_reached=append_sub.endpoint_reached,
                        static = append_sub.static
                    ))
                if append_sub.id in sub.secret_keys.keys():
                    sub.sub_list[-1].planned_route = append_sub.planned_route
                if append_sub.id in sub.external_visions:
                    sub.sub_list[-1].vision = append_sub.vision

                



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


    missiles_shared = giver_sub.m_count
    giver_sub.m_count = 0

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

    for adjacent_id in adjacent_subs:
        for sub in map.fleet:
            if sub.id == int(adjacent_id):
                client = sub
                
    client.external_visions.append(giver_sub.id)
    giver_sub.external_visions.append(client.id)
    print(f"Sub {giver_sub.id} and  sub {client.id} shared map info with eachother")


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

    for adjacent_id in adjacent_subs:
        for sub in map.fleet:
            if sub.id == int(adjacent_id):
                client = sub
                
    client.secret_keys.setdefault(giver_sub.id, secret_key)
    giver_sub.secret_keys.setdefault(client.id, secret_key)
                    
    print(f"Sub {giver_sub.id} and sub {adjacent_id} shared the secret key: {secret_key}")