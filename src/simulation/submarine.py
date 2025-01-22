import copy
import math
from simulation.point import Point


def status_control(method):
    def wrapper(self, *args, **kwargs):
        if not self.is_alive:
            self.print_death_message(method.__name__)
            return
        return method(self, *args, **kwargs)

    return wrapper


class Submarine:
    def __init__(
        self,
        id: int,
        map: list | None = None,
        x0=None,
        y0=None,
        xe=None,
        ye=None,
        m_count=0,
        endpoint_reached=False,
        temp_x=None,
        temp_y=None,
    ) -> None:
        """Map attribute needs to be updated each cycle"""
        self.is_alive = True
        self.id = id
        self.x0 = x0
        self.y0 = y0
        self.xe = xe
        self.ye = ye
        self.vision = None
        self.temp_x = temp_x
        self.temp_y = temp_y
        self.map = map
        self.endpoint_reached = endpoint_reached
        self.m_count = m_count
        self.planned_route = ["Share position"]
        self.secret_key = None
        self.sub_list = []
        self.visited_squares_counter = {(self.temp_y, self.temp_x): 0}
        self.endpoint_missiles_required = 0
        self.client_missiles_required = 0
        self.static = 0
        self.client_id = None
        self.prev_x = None
        self.prev_y = None
        if self.x0 != None:
            self.temp_x = self.x0
        if self.y0 != None:
            self.temp_y = self.y0
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.endpoint_reached = True
        if map != None and self.temp_x != None and self.temp_y != None:
            if self.map[self.temp_y][self.temp_x] != 0:
                self.is_alive = False
            self.map_height = len(self.map)
            self.map_width = len(self.map[0])
            self.vision = self.__get_starting_vision()

    def print_death_message(self, name: str) -> None:
        print(f"Submarine {self.id} is dead and can't {name}")

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

    @status_control
    def missile_shoot(self) -> bool:
        if self.m_count >= 1:
            self.m_count -= 1
            return True
        else:
            return False

    @status_control
    def move_sub(self, direction: str) -> None:
        self.prev_x = self.temp_x
        self.prev_y = self.temp_y
        if direction == "up":
            if self.temp_y != self.map_height - 1:
                if self.temp_y != self.ye and self.xe != self.temp_x:
                    self.vision[self.temp_y][self.temp_x] = 0
                else:
                    self.vision[self.temp_y][self.temp_x] = "E"
                self.temp_y += 1
                if (
                    self.temp_y,
                    self.temp_x,
                ) in self.visited_squares_counter.keys():
                    self.visited_squares_counter[(self.temp_y, self.temp_x)] += 1
                else:
                    self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                self.vision[self.temp_y][self.temp_x] = "S"
        elif direction == "down":
            if self.temp_y != 0:
                if self.temp_y != self.ye and self.xe != self.temp_x:
                    self.vision[self.temp_y][self.temp_x] = 0
                else:
                    self.vision[self.temp_y][self.temp_x] = "E"
                self.temp_y -= 1
                if (
                    self.temp_y,
                    self.temp_x,
                ) in self.visited_squares_counter.keys():
                    self.visited_squares_counter[(self.temp_y, self.temp_x)] += 1
                else:
                    self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                self.vision[self.temp_y][self.temp_x] = "S"
        elif direction == "right":
            if self.temp_x != self.map_width - 1:
                if self.temp_x != self.map_width:
                    if self.temp_y != self.ye and self.xe != self.temp_x:
                        self.vision[self.temp_y][self.temp_x] = 0
                    else:
                        self.vision[self.temp_y][self.temp_x] = "E"
                    self.temp_x += 1
                    if (
                        self.temp_y,
                        self.temp_x,
                    ) in self.visited_squares_counter.keys():
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] += 1
                    else:
                        self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                    self.vision[self.temp_y][self.temp_x] = "S"
        elif direction == "left":
            if self.temp_x != 0:
                if self.temp_y != self.ye and self.xe != self.temp_x:
                    self.vision[self.temp_y][self.temp_x] = 0
                else:
                    self.vision[self.temp_y][self.temp_x] = "E"
                self.temp_x -= 1
                if (
                    self.temp_y,
                    self.temp_x,
                ) in self.visited_squares_counter.keys():
                    self.visited_squares_counter[(self.temp_y, self.temp_x)] += 1
                else:
                    self.visited_squares_counter[(self.temp_y, self.temp_x)] = 0
                self.vision[self.temp_y][self.temp_x] = "S"

    @status_control
    def display_vision(self):
        for row in self.vision[::-1]:
            print(" ".join(map(str, row)))

    @status_control
    def general_scan(self, scannning_type: str) -> None:
        if scannning_type == "basic":
            self.basic_scan()
        elif scannning_type == "advanced":
            self.advanced_scan()

    def __static_counter(self) -> None:
        if self.prev_x == self.temp_x and self.prev_y == self.temp_y:
            self.static += 1
        else:
            static = 0
        return

    @status_control
    def basic_scan(self) -> None:
        """Den här metoden ska köras på varje u-båt i början av varje cykel"""
        self.__static_counter()
        if self.temp_y != self.map_height - 1:
            self.vision[self.temp_y + 1][self.temp_x] = self.map[self.temp_y + 1][
                self.temp_x
            ]
            if str(self.vision[self.temp_y + 1][self.temp_x])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y + 1][self.temp_x])[1])
                safe_point = str(self.temp_y + 1) + str(self.temp_x)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        if self.temp_y != 0:
            self.vision[self.temp_y - 1][self.temp_x] = self.map[self.temp_y - 1][
                self.temp_x
            ]
            if str(self.vision[self.temp_y - 1][self.temp_x])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y - 1][self.temp_x])[1])
                safe_point = str(self.temp_y - 1) + str(self.temp_x)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        if self.temp_x != self.map_width - 1:
            self.vision[self.temp_y][self.temp_x + 1] = self.map[self.temp_y][
                self.temp_x + 1
            ]
            if str(self.vision[self.temp_y][self.temp_x + 1])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y][self.temp_x + 1])[1])
                safe_point = str(self.temp_y) + str(self.temp_x + 1)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        if self.temp_x != 0:
            self.vision[self.temp_y][self.temp_x - 1] = self.map[self.temp_y][
                self.temp_x - 1
            ]
            if str(self.vision[self.temp_y][self.temp_x - 1])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y][self.temp_x - 1])[1])
                safe_point = str(self.temp_y) + str(self.temp_x - 1)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        for i in range(len(self.vision)):
            for j in range(len(self.vision[i])):
                if i == self.ye and j == self.xe:
                    self.vision[i][j] = "E"
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.endpoint_reached = True
            self.vision[self.temp_y][self.temp_x] = "S"

    @status_control
    def advanced_scan(self):
        self.basic_scan()
        if self.temp_y + 2 < self.map_height:
            self.vision[self.temp_y + 2][self.temp_x] = self.map[self.temp_y + 2][
                self.temp_x
            ]
            if str(self.vision[self.temp_y + 2][self.temp_x])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y + 2][self.temp_x])[1])
                safe_point = str(self.temp_y + 2) + str(self.temp_x)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        if self.temp_y - 2 >= 0:
            self.vision[self.temp_y - 2][self.temp_x] = self.map[self.temp_y - 2][
                self.temp_x
            ]
            if str(self.vision[self.temp_y - 2][self.temp_x])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y - 2][self.temp_x])[1])
                safe_point = str(self.temp_y - 2) + str(self.temp_x)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        if self.temp_x + 2 < self.map_width:
            self.vision[self.temp_y][self.temp_x + 2] = self.map[self.temp_y][
                self.temp_x + 2
            ]
            if str(self.vision[self.temp_y][self.temp_x + 2])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y][self.temp_x + 2])[1])
                safe_point = str(self.temp_y) + str(self.temp_x + 2)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        if self.temp_x - 2 >= 0:
            self.vision[self.temp_y][self.temp_x - 2] = self.map[self.temp_y][
                self.temp_x - 2
            ]
            if str(self.vision[self.temp_y][self.temp_x - 2])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y][self.temp_x - 2])[1])
                safe_point = str(self.temp_y) + str(self.temp_x - 2)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        if self.temp_x + 1 < self.map_width and self.temp_y + 1 < self.map_height:
            self.vision[self.temp_y + 1][self.temp_x + 1] = self.map[self.temp_y + 1][
                self.temp_x + 1
            ]
            if str(self.vision[self.temp_y + 1][self.temp_x + 1])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y + 1][self.temp_x + 1])[1])
                safe_point = str(self.temp_y + 1) + str(self.temp_x + 1)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        if self.temp_x - 1 >= 0 and self.temp_y + 1 < self.map_height:
            self.vision[self.temp_y + 1][self.temp_x - 1] = self.map[self.temp_y + 1][
                self.temp_x - 1
            ]
            if str(self.vision[self.temp_y + 1][self.temp_x - 1])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y + 1][self.temp_x - 1])[1])
                safe_point = str(self.temp_y + 1) + str(self.temp_x - 1)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        if self.temp_x + 1 < self.map_width and self.temp_y - 1 >= 0:
            self.vision[self.temp_y - 1][self.temp_x + 1] = self.map[self.temp_y - 1][
                self.temp_x + 1
            ]
            if str(self.vision[self.temp_y - 1][self.temp_x + 1])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y - 1][self.temp_x + 1])[1])
                safe_point = str(self.temp_y - 1) + str(self.temp_x + 1)
                self.__remove_duplicate_subs(safe_point=safe_point, sub_index=sub_index)
        if self.temp_x - 1 >= 0 and self.temp_y - 1 >= 0:
            self.vision[self.temp_y - 1][self.temp_x - 1] = self.map[self.temp_y - 1][
                self.temp_x - 1
            ]
            if str(self.vision[self.temp_y - 1][self.temp_x - 1])[0] == "U":
                sub_index = int(str(self.vision[self.temp_y - 1][self.temp_x - 1])[1])
                safe_point = str(self.temp_y - 1) + str(self.temp_x - 1)
        for i in range(len(self.vision)):
            for j in range(len(self.vision[i])):
                if i == self.ye and j == self.xe:
                    self.vision[i][j] = "E"
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.endpoint_reached = True
            self.vision[self.temp_y][self.temp_x] = "S"

    def __get_gravel_squares(self) -> list:
        gravel_squares = []
        for i in range(len(self.vision)):
            for j in range(len(self.vision[i])):
                if isinstance(self.vision[i][j], int) and self.vision[i][j] != 0:
                    gravel_squares.append((i, j))
        return gravel_squares

    def __remove_duplicate_subs(self, safe_point: str, sub_index: int):
        for i in range(len(self.vision)):
            for j in range(len(self.vision[i])):
                if self.vision[i][j] == "U" + str(sub_index):
                    self.vision[i][j] = 0
                if int(safe_point[0]) == i and int(safe_point[1]) == j:
                    self.vision[i][j] = "U" + str(sub_index)

    def __get_endpoint_route(self) -> None:
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.planned_route = ["Scan advanced"]
            return
        new_route = []
        banned_squares = []
        missiles_required = 0
        temp_x = self.temp_x
        temp_y = self.temp_y
        visited_squares_counter_copy = copy.copy(self.visited_squares_counter)
        loop_counter = -1
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
            for point in new_points:
                if point.x >= self.map_width or 0 > point.x:
                    temp_banned_points.append(point)
                elif point.y >= self.map_height or 0 > point.y:
                    temp_banned_points.append(point)
                elif self.vision[point.y][point.x] in {"B", "x"}:
                    temp_banned_points.append(point)
                elif (point.y, point.x) in banned_squares:
                    temp_banned_points.append(point)
                elif (point.y, point.x) in visited_squares_counter_copy.keys():
                    temp_banned_points.append(point)
                    new_points_visited.append(point)
                elif str(self.vision[point.y][point.x])[0] == "U":
                    temp_banned_points.append(point)
                elif isinstance(self.vision[point.y][point.x], int):
                    if (
                        self.m_count - missiles_required - self.vision[point.y][point.x]
                        < 0
                    ):
                        temp_banned_points.append(point)
                elif point.direction == "up" and point.y < len(self.vision) - 1:
                    if str(self.vision[point.y + 1][point.x])[0] == "U":
                        temp_banned_points.append(point)
                elif point.direction == "down" and point.y > 1:
                    if str(self.vision[point.y - 1][point.x])[0] == "U":
                        temp_banned_points.append(point)
                elif point.direction == "right" and point.x < len(self.vision[0]) - 1:
                    if str(self.vision[point.y][point.x + 1])[0] == "U":
                        temp_banned_points.append(point)
                elif point.direction == "left" and point.x > 1:
                    if str(self.vision[point.y][point.x - 1])[0] == "U":
                        temp_banned_points.append(point)
            for point in temp_banned_points:
                new_points.remove(point)
            if len(new_points):
                if (
                    isinstance(self.vision[new_points[0].y][new_points[0].x], int)
                    and self.vision[new_points[0].y][new_points[0].x] != 0
                ):
                    missiles_required = (
                        missiles_required
                        + self.vision[new_points[0].y][new_points[0].x]
                    )
                    for i in range(self.vision[new_points[0].y][new_points[0].x]):
                        new_route.append(f"Shoot {new_points[0].direction}")
                    new_route.append(f"Move {new_points[0].direction}")
                else:
                    new_route.append(f"Move {new_points[0].direction}")
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
                elif loop_counter > self.map_height * self.map_width + self.m_count:
                    return
                visited_squares_counter_copy[(new_points[0].y, new_points[0].x)] = 0
            elif len(new_points_visited):
                least_visited = 9999
                for point in new_points_visited:
                    if (
                        visited_squares_counter_copy[(point.y, point.x)]
                        <= least_visited
                        and str(self.vision[point.y][point.x])[0] != "U"
                    ):
                        least_visited = visited_squares_counter_copy[(point.y, point.x)]
                final_point = new_points_visited[0]
                for point in new_points_visited:
                    if (
                        visited_squares_counter_copy[(point.y, point.x)]
                        == least_visited
                        and str(self.vision[point.y][point.x])[0] != "U"
                    ):
                        final_point = point
                        break
                visited_squares_counter_copy[(final_point.y, final_point.x)] += 1
                if (
                    isinstance(self.vision[final_point.y][final_point.x], int)
                    and self.vision[final_point.y][final_point.x] != 0
                ):
                    missiles_required = (
                        missiles_required + self.vision[final_point.y][final_point.x]
                    )
                    for i in range(self.vision[final_point.y][final_point.x]):
                        new_route.append(f"Shoot {final_point.direction}")
                else:
                    new_route.append(f"Move {final_point.direction}")
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
                elif (
                    loop_counter
                    > (self.map_height * self.map_width + self.m_count) * 10
                ):
                    self.planned_route = ["Scan advanced"]
                    return
            elif loop_counter > (self.map_height * self.map_width + self.m_count) * 10:
                self.planned_route = ["Scan advanced"]
                return
            else:
                visited_squares_counter_copy = {(self.temp_y, self.temp_x): 0}
                temp_x = self.temp_x
                temp_y = self.temp_y
                missiles_required = 0
                new_route = []
        self.planned_route = new_route

    def __get_client_route(self, y_goal: int, x_goal: int) -> bool:
        if self.temp_x == x_goal and self.temp_y == y_goal:
            client = None
            for sub in self.sub_list:
                if sub.id == self.client_id:
                    client = sub
                    secret_key = sub.secret_key
                    break
            if secret_key == None:
                self.planned_route = ["Share secret", "Share vision", "Share missiles"]
                return True
            elif client.vision == None:
                self.planned_route = ["Share vision", "Share missiles"]
                return True
            elif self.m_count - self.endpoint_missiles_required > 0:
                self.planned_route = ["Share missiles"]
                return True
            else:
                return False
        new_route = []
        banned_squares = []
        missiles_required = 0
        temp_x = self.temp_x
        temp_y = self.temp_y
        visited_squares_counter_copy = copy.copy(self.visited_squares_counter)
        loop_counter = -1
        while True:
            loop_counter += 1
            new_points_visited = []
            new_points = [
                Point(
                    y=temp_y + 1,
                    x=temp_x,
                    direction="up",
                    e_distance=math.sqrt(
                        (y_goal - (temp_y + 1)) ** 2 + (x_goal - temp_x) ** 2
                    ),
                ),
                Point(
                    y=temp_y - 1,
                    x=temp_x,
                    direction="down",
                    e_distance=math.sqrt(
                        (y_goal - (temp_y - 1)) ** 2 + (x_goal - temp_x) ** 2
                    ),
                ),
                Point(
                    y=temp_y,
                    x=temp_x + 1,
                    direction="right",
                    e_distance=math.sqrt(
                        (y_goal - temp_y) ** 2 + (x_goal - (temp_x + 1)) ** 2
                    ),
                ),
                Point(
                    y=temp_y,
                    x=temp_x - 1,
                    direction="left",
                    e_distance=math.sqrt(
                        (y_goal - temp_y) ** 2 + (x_goal - (temp_x - 1)) ** 2
                    ),
                ),
            ]
            new_points = sorted(
                new_points, key=lambda point: point.e_distance, reverse=False
            )
            temp_banned_points = []
            for point in new_points:
                if point.x >= self.map_width or 0 > point.x:
                    temp_banned_points.append(point)
                elif point.y >= self.map_height or 0 > point.y:
                    temp_banned_points.append(point)
                elif self.vision[point.y][point.x] in {"B", "x"}:
                    temp_banned_points.append(point)
                elif (point.y, point.x) in banned_squares:
                    temp_banned_points.append(point)
                elif (point.y, point.x) in visited_squares_counter_copy.keys():
                    temp_banned_points.append(point)
                    new_points_visited.append(point)
                elif str(self.vision[point.y][point.x])[0] == "U":
                    temp_banned_points.append(point)
                elif isinstance(self.vision[point.y][point.x], int):
                    if (
                        self.m_count - missiles_required - self.vision[point.y][point.x]
                        < 0
                    ):
                        temp_banned_points.append(point)
            for point in temp_banned_points:
                new_points.remove(point)
            if len(new_points):
                if (
                    isinstance(self.vision[new_points[0].y][new_points[0].x], int)
                    and self.vision[new_points[0].y][new_points[0].x] != 0
                ):
                    missiles_required = (
                        missiles_required
                        + self.vision[new_points[0].y][new_points[0].x]
                    )
                    for i in range(self.vision[new_points[0].y][new_points[0].x]):
                        new_route.append(f"Shoot {new_points[0].direction}")
                else:
                    new_route.append(f"Move {new_points[0].direction}")
                if new_points[0].direction == "up":
                    temp_y += 1
                elif new_points[0].direction == "down":
                    temp_y -= 1
                elif new_points[0].direction == "right":
                    temp_x += 1
                elif new_points[0].direction == "left":
                    temp_x -= 1
                if x_goal == temp_x and y_goal == temp_y:
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
                elif loop_counter > self.map_height * self.map_width + self.m_count:
                    return
                visited_squares_counter_copy[(new_points[0].y, new_points[0].x)] = 0
            elif len(new_points_visited):
                least_visited = 9999
                for point in new_points_visited:
                    if (
                        visited_squares_counter_copy[(point.y, point.x)]
                        <= least_visited
                        and str(self.vision[point.y][point.x])[0] != "U"
                    ):
                        least_visited = visited_squares_counter_copy[(point.y, point.x)]
                final_point = new_points_visited[0]
                for point in new_points_visited:
                    if (
                        visited_squares_counter_copy[(point.y, point.x)]
                        == least_visited
                        and str(self.vision[point.y][point.x])[0] != "U"
                    ):
                        final_point = point
                        break
                visited_squares_counter_copy[(final_point.y, final_point.x)] += 1
                if (
                    isinstance(self.vision[final_point.y][final_point.x], int)
                    and self.vision[final_point.y][final_point.x] != 0
                ):
                    missiles_required = (
                        missiles_required + self.vision[final_point.y][final_point.x]
                    )
                    for i in range(self.vision[final_point.y][final_point.x]):
                        new_route.append(f"Shoot {final_point.direction}")
                else:
                    new_route.append(f"Move {final_point.direction}")
                if final_point.direction == "up":
                    temp_y += 1
                elif final_point.direction == "down":
                    temp_y -= 1
                elif final_point.direction == "right":
                    temp_x += 1
                elif final_point.direction == "left":
                    temp_x -= 1
                if x_goal == temp_x and y_goal == temp_y:
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
                elif (
                    loop_counter
                    > (self.map_height * self.map_width + self.m_count) * 10
                ):
                    return False
            elif loop_counter > (self.map_height * self.map_width + self.m_count) * 10:
                return False
            else:
                visited_squares_counter_copy = {(self.temp_y, self.temp_x): 0}
                temp_x = self.temp_x
                temp_y = self.temp_y
                missiles_required = 0
                new_route = []
        self.client_missiles_required = missiles_required
        new_route.append("Share secret")
        new_route.append("Share vision")
        new_route.append("Share missiles")
        self.planned_route = new_route
        return True

    def __get_adjacent_square(self, point_x: int, point_y: int) -> str | bool:
        """Hittar en säker ruta bredvid en given ruta"""
        if point_y != self.map_height - 1:
            if (
                self.vision[point_y + 1][point_x] == 0
                or self.vision[point_y + 1][point_x] == "S"
            ):
                return str(point_y + 1) + str(point_x)
        if self.temp_y != 0:
            if (
                self.vision[point_y - 1][point_x] == 0
                or self.vision[point_y - 1][point_x] == "S"
            ):
                return str(point_y - 1) + str(point_x)
        if point_x != self.map_width - 1:
            if (
                self.vision[point_y][point_x] == 0
                or self.vision[point_y][point_x] == "S"
            ):
                return str(point_y) + str(point_x)
        if self.temp_x != 0:
            if (
                self.vision[point_y][point_x] == 0
                or self.vision[point_y][point_x] == "S"
            ):
                return str(point_y) + str(point_x)
        return False

    def __is_adjacent(self, sub) -> bool:
        """Kontrollerar om det står en ubåt bredvid ubåten"""
        if sub.temp_y + 1 == self.temp_y and sub.temp_x == self.temp_x:
            return True
        elif sub.temp_y - 1 == self.temp_y and sub.temp_x == self.temp_x:
            return True
        elif sub.temp_y == self.temp_y and sub.temp_x + 1 == self.temp_x:
            return True
        elif sub.temp_y == self.temp_y and sub.temp_x - 1 == self.temp_x:
            return True
        return False

    def __get_client_id(self) -> int | None:
        """Retunerar ett ID på en ubåt som behöver hjälp"""
        if self.client_id == None:
            for sub in self.sub_list:
                if sub.static:
                    square = self.__get_adjacent_square(sub.temp_x, sub.temp_y)
                    if square:
                        if self.__get_client_route(int(square[1]), int(square[0])):
                            if (
                                self.m_count
                                - self.endpoint_missiles_required
                                - self.client_missiles_required
                                >= 0
                            ):
                                return sub.id
        else:
            for sub in self.sub_list:
                if self.client_id == sub.id:
                    if (
                        self.__is_adjacent(sub)
                        and self.m_count
                        - self.endpoint_missiles_required
                        > 0
                    ):
                        return sub.id
        return None

    @status_control
    def update_vision(self):
        for sub in self.sub_list:
            if sub.temp_x != None and sub.temp_y != None:
                for i in range(len(self.vision)):
                    for j in range(len(self.vision[i])):
                        if i == sub.temp_y and j == sub.temp_x:
                            self.vision[i][j] = "U" + str(sub.id)
                        elif str(self.vision[i][j])[0] == "U":
                            self.vision[i][j] = 0

    @status_control
    def update_path(self):
        self.client_id = self.__get_client_id()
        if self.client_id == None:
            self.__get_endpoint_route()
        else:
            client = None
            for sub in self.sub_list:
                if sub.id == self.client_id:
                    client = sub
                    break
            square = self.__get_adjacent_square(client.temp_x, client.temp_y)
            if square != False:
                self.__get_client_route(int(square[0]), int(square[1]))
            else:
                self.__get_endpoint_route()
