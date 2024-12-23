import math
from simulation.point import Point


class Submarine:
    def __init__(
        self,
        id: int,
        map: list,
        planned_route: list = [],
        secret_keys: dict = {},
        x0=None,
        y0=None,
        xe=None,
        ye=None,
        m_count=0,
    ) -> None:
        """Map attribute needs to be updated each cycle"""
        self.id = id
        self.x0 = x0
        self.y0 = y0
        self.xe = xe
        self.ye = ye
        self.map = map
        if self.y0 == None:
            self.temp_y = -1
        else:
            self.temp_y = self.y0
        if self.x0 == None:
            self.temp_x = -1
        else:
            self.temp_x = self.x0
        self.endpoint_reached = False
        self.is_alive = True
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.endpoint_reached = True
        if self.map[self.temp_y][self.temp_x] != 0:
            self.is_alive = False
        self.m_count = m_count
        self.planned_route = planned_route
        self.secret_keys = secret_keys
        self.sub_list = []
        self.map_height = len(self.map)
        self.map_width = len(self.map[0])
        self.vision = self.__get_starting_vision()
        self.visited_squares_counter = {(self.temp_y, self.temp_x):0}

    def print_death_message(self) -> None:
        print(f"Submarine {self.id} is dead and can't perform this action")

    def display_planned_route(self) -> None:
        print(self.planned_route)

    def __get_starting_vision(self) -> list:
        wrapper_list = []
        for i in range(self.map_height):
            inner_list = []
            for j in range(self.map_width):
                if j == self.temp_x and i == self.temp_y:
                    inner_list.append("S")
                elif j == self.xe and i == self.ye:
                    inner_list.append("E")
                else:
                    inner_list.append("?")
            wrapper_list.append(inner_list)
        return wrapper_list

    def missile_shoot(self) -> bool:
        if self.m_count >= 1:
            self.m_count -= 1
            return True
        else:
            return False

    def move_sub(self, direction: str) -> None:
        if not self.is_alive:
            print("Can't move terminated sub")
            return
        if direction == "up":
            if self.temp_y != self.map_height - 1:
                if (
                    self.map[self.temp_y + 1][self.temp_x] == "B"
                    or self.map[self.temp_y + 1][self.temp_x] == "U"
                ):
                    self.temp_y += 1
                    if (self.temp_y, self.temp_x) in self.visited_squares_counter.keys():
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] +=1
                    else:   
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                    self.is_alive = False
                    return
                elif (
                    self.map[self.temp_y + 1][self.temp_x] == 0
                    or self.map[self.temp_y + 1][self.temp_x] == "E"
                ):
                    self.vision[self.temp_y][self.temp_x] = 0
                    self.temp_y += 1
                    if (self.temp_y, self.temp_x) in self.visited_squares_counter.keys():
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] +=1
                    else:   
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                    self.vision[self.temp_y][self.temp_x] = "S"
        elif direction == "down":
            if self.temp_y != 0:
                if (
                    self.map[self.temp_y - 1][self.temp_x] == "B"
                    or self.map[self.temp_y - 1][self.temp_x] == "U"
                ):
                    self.temp_y -= 1
                    if (self.temp_y, self.temp_x) in self.visited_squares_counter.keys():
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] +=1
                    else:   
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                    self.is_alive = False
                    return
                elif (
                    self.map[self.temp_y - 1][self.temp_x] == 0
                    or self.map[self.temp_y - 1][self.temp_x] == "E"
                ):
                    self.vision[self.temp_y][self.temp_x] = 0
                    self.temp_y -= 1
                    if (self.temp_y, self.temp_x) in self.visited_squares_counter.keys():
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] +=1
                    else:   
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                    self.vision[self.temp_y][self.temp_x] = "S"
        elif direction == "right":
            if self.temp_x != self.map_width - 1:
                if self.temp_x != self.map_width:
                    if (
                        self.map[self.temp_y][self.temp_x + 1] == "B"
                        or self.map[self.temp_y][self.temp_x + 1] == "U"
                    ):
                        self.temp_x += 1
                        if (self.temp_y, self.temp_x) in self.visited_squares_counter.keys():
                            self.visited_squares_counter[(self.temp_y, self.temp_x)] +=1
                        else:   
                            self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                        self.is_alive = False
                        return
                    elif (
                        self.map[self.temp_y][self.temp_x + 1] == 0
                        or self.map[self.temp_y][self.temp_x + 1] == "E"
                    ):
                        self.vision[self.temp_y][self.temp_x] = 0
                        self.temp_x += 1
                        if (self.temp_y, self.temp_x) in self.visited_squares_counter.keys():
                            self.visited_squares_counter[(self.temp_y, self.temp_x)] +=1
                        else:   
                            self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                        self.vision[self.temp_y][self.temp_x] = "S"
        elif direction == "left":
            if self.temp_x != 0:
                if (
                    self.map[self.temp_y][self.temp_x - 1] == "B"
                    or self.map[self.temp_y][self.temp_x - 1] == "U"
                ):
                    self.temp_x -= 1
                    if (self.temp_y, self.temp_x) in self.visited_squares_counter.keys():
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] +=1
                    else:   
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                    self.is_alive = False
                    return
                elif (
                    self.map[self.temp_y][self.temp_x - 1] == 0
                    or self.map[self.temp_y][self.temp_x - 1] == "e"
                ):
                    self.vision[self.temp_y][self.temp_x] = 0
                    self.temp_x -= 1
                    if (self.temp_y, self.temp_x) in self.visited_squares_counter.keys():
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] +=1
                    else:   
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                    self.vision[self.temp_y][self.temp_x] = "S"
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.endpoint_reached = True
            self.vision[self.temp_y][self.temp_x] = "S"

    def get_vision_from_sub(self, external_id: int, external_vision: list) -> None:
        for sub in self.sub_list:
            if sub.id == external_id:
                sub.vision = external_vision
                self.__merge_vision(sub)
                self.get_new_route()
                return
        new_sub = Submarine(
            id=external_id,
            map=self.map,
        )
        new_sub.vision = external_vision
        self.__merge_vision(new_sub)
        self.sub_list.append(new_sub)
        self.get_new_route()

    def display_vision(self):
        for row in self.vision[::-1]:
            print(" ".join(map(str, row)))

    def __merge_vision(self, external_sub) -> None:
        for i in range(self.map_height):
            for j in range(self.map_width):
                if self.vision[i][j] == "?" and external_sub.vision[i][j] != "?":
                    self.vision[i][j] = external_sub.vision[i][j]
                elif self.vision[i][j] != "?" and external_sub.vision[i][j] == "?":
                    external_sub.vision[i][j] = self.vision[i][j]
                elif (
                    self.vision[i][j] != "?"
                    and external_sub.vision[i][j] != "?"
                    and self.vision[i][j] != external_sub.vision[i][j]
                    and self.id < external_sub.id
                ):
                    external_sub.vision[i][j] = self.vision[i][j]
                elif (
                    self.vision[i][j] != "?"
                    and external_sub.vision[i][j] != "?"
                    and self.vision[i][j] != external_sub.vision[i][j]
                    and self.id > external_sub.id
                ):
                    self.vision[i][j] = external_sub.vision[i][j]

    def trade_missiles(self, m_change: int) -> None:
        if (m_change * -1) > self.m_count:
            raise ValueError("Not enough missiles to perform trade")
        elif m_change == 0:
            raise ValueError("Can't trade w/o missiles")
        self.m_count += m_change

    def get_endpoint_data_from_sub(
        self,
        external_id: int,
        external_xe: int,
        external_ye: int,
        external_endpoint_status: int,
    ) -> None:
        for sub in self.sub_list:
            if sub.id == external_id:
                sub.xe = external_xe
                sub.ye = external_ye
                sub.endpoint_reached = external_endpoint_status
                return
        self.sub_list.append(
            Submarine(
                id=external_id,
                xe=external_xe,
                ye=external_ye,
                endpoint_reached=external_endpoint_status,
                map=self.map,
            )
        )

    def get_missile_data_from_sub(
        self, external_id: int, external_m_count: int
    ) -> None:
        for sub in self.sub_list:
            if sub.id == external_id:
                sub.m_count = external_m_count
                return
        self.sub_list.append(
            Submarine(
                id=external_id,
                map=self.map,
                m_count=external_m_count,
            )
        )

    def get_route_from_sub(self, external_id, external_route) -> None:
        for sub in self.sub_list:
            if sub.id == external_id:
                sub.planned_route = external_route
                return
        self.sub_list.append(
            Submarine(
                id=external_id,
                map=self.map,
                planned_route=external_route,
            )
        )

    def get_secret_from_sub(self, external_id, external_key) -> None:
        self.secret_keys.setdefault(external_id, external_key)

    def basic_scan(self, plan_route=True):
        """Den här metoden ska köras på varje u-båt i början av varje cykel"""
        if self.temp_y != self.map_height - 1:
            self.vision[self.temp_y + 1][self.temp_x] = self.map[self.temp_y + 1][
                self.temp_x
            ]
        if self.temp_y != 0:
            self.vision[self.temp_y - 1][self.temp_x] = self.map[self.temp_y - 1][
                self.temp_x
            ]
        if self.temp_x != self.map_width - 1:
            self.vision[self.temp_y][self.temp_x + 1] = self.map[self.temp_y][
                self.temp_x + 1
            ]
        if self.temp_x != 0:
            self.vision[self.temp_y][self.temp_x - 1] = self.map[self.temp_y][
                self.temp_x - 1
            ]
        for i in range(len(self.vision)):
            for j in range(len(self.vision[i])):

                if i == self.ye and j == self.xe:

                    self.vision[i][j] = "E"
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.endpoint_reached = True
            self.vision[self.temp_y][self.temp_x] = "S"
        if plan_route:
            self.get_new_route()
            
    def __get_gravel_squares(self) -> list:
        gravel_squares = []
        for i in range(len(self.vision)):
            for j in range(len(self.vision[i])):
                if isinstance(self.vision[i][j], int) and self.vision[i][j] != 0:
                    gravel_squares.append((i, j))
        return gravel_squares
                    
       

    def advanced_scan(self):
        self.basic_scan(False)
        if self.temp_y + 2 < self.map_height:
            self.vision[self.temp_y + 2][self.temp_x] = self.map[self.temp_y + 2][
                self.temp_x
            ]
        if self.temp_y - 1 != 0:
            self.vision[self.temp_y - 2][self.temp_x] = self.map[self.temp_y - 2][
                self.temp_x
            ]
        if self.temp_x + 2 < self.map_width:
            self.vision[self.temp_y][self.temp_x + 2] = self.map[self.temp_y][
                self.temp_x + 2
            ]
        if self.temp_x - 1 != 0:
            self.vision[self.temp_y][self.temp_x - 2] = self.map[self.temp_y][
                self.temp_x - 2
            ]
        for i in range(len(self.vision)):
            for j in range(len(self.vision[i])):
                if i == self.ye and j == self.xe:
                    self.vision[i][j] = "E"
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.endpoint_reached = True
            self.vision[self.temp_y][self.temp_x] = "S"
        self.get_new_route()

    def get_new_route(self) -> None:
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.planned_route = []
            return
        new_route = []
        banned_squares = []
        missiles_required = 0
        temp_x = self.temp_x
        temp_y = self.temp_y
        visited_squares_counter_copy = self.visited_squares_counter
        loop_counter = 0
        while True:
            loop_counter += 1
            new_points_visited = []
            new_points = [
                Point(
                    y=temp_y + 1,
                    x=temp_x,
                    direction="up",
                    e_distance=math.sqrt(
                        (self.ye - (temp_y + 1)) ** 2 + (self.xe - temp_x) ** 2
                    ),
                ),
                Point(
                    y=temp_y - 1,
                    x=temp_x,
                    direction="down",
                    e_distance=math.sqrt(
                        (self.ye - (temp_y - 1)) ** 2 + (self.xe - temp_x) ** 2
                    ),
                ),
                Point(
                    y=temp_y,
                    x=temp_x + 1,
                    direction="right",
                    e_distance=math.sqrt(
                        (self.ye - temp_y) ** 2 + (self.xe - (temp_x + 1)) ** 2
                    ),
                ),
                Point(
                    y=temp_y,
                    x=temp_x - 1,
                    direction="left",
                    e_distance=math.sqrt(
                        (self.ye - temp_y) ** 2 + (self.xe - (temp_x - 1)) ** 2
                    ),
                ),
            ]
            new_points = sorted(
                new_points, key=lambda point: point.e_distance, reverse=False
            )
            temp_banned_points = []
            if temp_x == 2 and temp_y == 2:
                pass
            for point in new_points:
                if point.x >= self.map_width or 0 > point.x:
                    temp_banned_points.append(point)
                elif point.y >= self.map_height or 0 > point.y:
                    temp_banned_points.append(point)
                elif self.vision[point.y][point.x] in {"U", "B", "x"}:
                    temp_banned_points.append(point)
                elif (point.y, point.x) in banned_squares:
                    temp_banned_points.append(point)
                elif (point.y, point.x) in visited_squares_counter_copy.keys():
                    temp_banned_points.append(point)
                    new_points_visited.append(point)
            for point in temp_banned_points:
                new_points.remove(point)
            if len(new_points):
                if isinstance(self.vision[new_points[0].y][new_points[0].x], int):
                    missiles_required = (
                        missiles_required
                        + self.vision[new_points[0].y][new_points[0].x]
                    )
                new_route.append(new_points[0].direction)
                if new_points[0].direction == "up":
                    temp_y += 1
                elif new_points[0].direction == "down":
                    temp_y -= 1
                elif new_points[0].direction == "right":
                    temp_x += 1
                elif new_points[0].direction == "left":
                    temp_x -= 1
                if self.xe == temp_x and self.ye == temp_y:
                    if missiles_required > self.m_count:
                        for square in self.__get_gravel_squares():
                            banned_squares.append(square)
                        new_route = []
                        missiles_required = 0
                        loop_counter = 0
                        temp_x = self.temp_x
                        temp_y = self.temp_y
                    else:      
                        break
                elif loop_counter > 9999:
                    return
                visited_squares_counter_copy[(new_points[0].y, new_points[0].x)] = 0
            elif len(new_points_visited):
                least_visited = 9999
                for point in new_points_visited:
                    if visited_squares_counter_copy[(point.y, point.x)] <= least_visited:
                        least_visited = visited_squares_counter_copy[(point.y, point.x)] 
                final_point = new_points_visited[0]  
                for point in new_points_visited:
                    if visited_squares_counter_copy[(point.y, point.x)] == least_visited:
                        final_point = point
                        break
                visited_squares_counter_copy[(final_point.y, final_point.x)] += 1
                if isinstance(self.vision[final_point.y][final_point.x], int):
                    missiles_required = (
                        missiles_required + self.vision[final_point.y][final_point.x]
                    )
                new_route.append(final_point.direction)
                if final_point.direction == "up":
                    temp_y += 1
                elif final_point.direction == "down":
                    temp_y -= 1
                elif final_point.direction == "right":
                    temp_x += 1
                elif final_point.direction == "left":
                    temp_x -= 1
                if self.xe == temp_x and self.ye == temp_y:
                    if missiles_required > self.m_count:
                        for square in self.__get_gravel_squares():
                            banned_squares.append(square)
                        new_route = []
                        missiles_required = 0
                        loop_counter = 0
                        temp_x = self.temp_x
                        temp_y = self.temp_y
                    else:      
                        break
                elif loop_counter > 9999:
                    return
            else:
                visited_squares_counter_copy = {(self.temp_y, self.temp_x):0}
                temp_x = self.temp_x
                temp_y = self.temp_y
                missiles_required = 0
                new_route = []
        self.planned_route = new_route
