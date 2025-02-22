import copy
import math
import random
from simulation.point import Point
from collections import deque


def status_control(method):
    def wrapper(self, *args, **kwargs):
        if not self.is_alive:
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
        secret_keys={},
        external_visions=[],
        prev_x=None,
        prev_y=None,
        m_count=0,
        endpoint_reached=False,
        temp_x=None,
        temp_y=None,
        static=0,
    ) -> None:
        """Map attribute needs to be updated each cycle"""
        self.is_alive = True
        self.id = id
        self.x0 = x0
        self.y0 = y0
        self.xe = xe
        self.ye = ye
        self.temp_x = temp_x
        self.temp_y = temp_y
        self.map = map
        self.prev_x = prev_x
        self.prev_y = prev_y
        self.vision = None
        self.endpoint_reached = endpoint_reached
        self.m_count = m_count
        self.planned_route = []
        self.secret_keys = secret_keys
        self.external_visions = external_visions
        self.sub_list = []
        self.visited_squares_counter = {(self.temp_y, self.temp_x): 0}
        self.endpoint_missiles_required = 0
        self.client_missiles_required = 0
        self.static = static
        self.client_id = None
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
        self.static = 0

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

    @status_control
    def basic_scan(self) -> None:
        """Den här metoden ska köras på varje u-båt i början av varje cykel"""
        self.update_vision()
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
        else:
            self.endpoint_reached = False
            self.vision[self.temp_y][self.temp_x] = "S"

    @status_control
    def advanced_scan(self):
        self.basic_scan()
        self.static += 1
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

    def __is_safe(self, point: Point) -> bool:
        for sub in self.sub_list:
            if sub.is_alive and sub.planned_route != None:
                if len(sub.planned_route) > 1:
                    if (
                        sub.planned_route[1] == "Move up"
                        and sub.prev_x == point.x
                        and sub.prev_y + 1 == point.y
                    ):
                        return False
                elif len(sub.planned_route) > 1:
                    if (
                        sub.planned_route[1] == "Move down"
                        and sub.prev_x == point.x
                        and sub.prev_y - 1 == point.y
                    ):
                        return False
                elif len(sub.planned_route) > 1:
                    if (
                        sub.planned_route[1] == "Move right"
                        and sub.prev_x == point.x
                        and sub.prev_y + 1 == point.y
                    ):
                        return False
                elif len(sub.planned_route) > 1:
                    if (
                        sub.planned_route[1] == "Move left"
                        and sub.prev_x == point.x
                        and sub.prev_y - 1 == point.y
                    ):
                        return False
        return True

    def __is_scared(
        self,
        point: Point,
    ) -> bool:

        if point.direction == "up":
            if (
                point.y < len(self.vision) - 1
                and str(self.vision[point.y + 1][point.x])[0] == "U"
            ):
                if random.randint(0, 4) != 0:
                    return True
            if (
                point.y < len(self.vision)
                and point.x < self.map_width - 1
                and str(self.vision[point.y][point.x + 1])[0] == "U"
            ):
                if random.randint(0, 4) != 0:
                    return True
            if (
                point.y < len(self.vision)
                and point.x - 1 >= 0
                and str(self.vision[point.y][point.x - 1])[0] == "U"
            ):
                if random.randint(0, 4) != 0:
                    return True

        elif point.direction == "down":
            if point.y > 1 and str(self.vision[point.y - 1][point.x])[0] == "U":
                if random.randint(0, 4) != 0:
                    return True
            if (
                point.y > 0
                and point.x < self.map_width - 1
                and str(self.vision[point.y][point.x + 1])[0] == "U"
            ):
                if random.randint(0, 4) != 0:
                    return True
            if (
                point.y > 0
                and point.x - 1 >= 0
                and str(self.vision[point.y][point.x - 1])[0] == "U"
            ):
                if random.randint(0, 4) != 0:
                    return True

        elif point.direction == "right":
            if (
                point.x < len(self.vision[0]) - 1
                and str(self.vision[point.y][point.x + 1])[0] == "U"
            ):
                if random.randint(0, 4) != 0:
                    return True
            if (
                point.x < len(self.vision[0])
                and point.y < self.map_height - 1
                and str(self.vision[point.y + 1][point.x])[0] == "U"
            ):
                if random.randint(0, 4) != 0:
                    return True
            if (
                point.x < len(self.vision[0])
                and point.y - 1 >= 0
                and str(self.vision[point.y - 1][point.x])[0] == "U"
            ):
                if random.randint(0, 4) != 0:
                    return True
            return False

        elif point.direction == "left":
            if point.x > 1 and str(self.vision[point.y][point.x - 1])[0] == "U":
                if random.randint(0, 4) != 0:
                    return True
            if (
                point.x > 0
                and point.y < self.map_height - 1
                and str(self.vision[point.y + 1][point.x])[0] == "U"
            ):
                if random.randint(0, 4) != 0:
                    return True
            if (
                point.x > 0
                and point.y - 1 >= 0
                and str(self.vision[point.y - 1][point.x])[0] == "U"
            ):
                if random.randint(0, 4) != 0:
                    return True

        return False

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
                elif str(self.vision[point.y][point.x])[0] == "U":
                    temp_banned_points.append(point)
                elif (
                    self.vision[point.y][point.x] in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    and self.m_count < self.vision[point.y][point.x]
                ):
                    temp_banned_points.append(point)
                elif self.__is_scared(point):
                    temp_banned_points.append(point)
                elif not self.__is_safe(point):
                    temp_banned_points.append(point)
                elif (point.y, point.x) in visited_squares_counter_copy.keys():
                    temp_banned_points.append(point)
                    new_points_visited.append(point)
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
                elif self.__breaker(loop_counter):
                    self.planned_route = ["Scan advanced"]
                    return
                visited_squares_counter_copy[(new_points[0].y, new_points[0].x)] = 0
            elif len(new_points_visited):
                least_visited = 999
                for point in new_points_visited:
                    if (
                        visited_squares_counter_copy[(point.y, point.x)]
                        <= least_visited
                        and str(self.vision[point.y][point.x])[0] != "U"
                    ):
                        least_visited = visited_squares_counter_copy[(point.y, point.x)]
                final_point = None
                for point in new_points_visited:
                    if (
                        visited_squares_counter_copy[(point.y, point.x)]
                        == least_visited
                        and str(self.vision[point.y][point.x])[0] != "U"
                        and self.__is_safe(point)
                    ):
                        final_point = point
                        break
                if final_point == None:
                    self.planned_route = ["Scan advanced"]
                    return
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
                elif self.__breaker(loop_counter):
                    self.planned_route = ["Scan advanced"]
                    return
            elif self.__breaker(loop_counter):
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
        if self.m_count - self.endpoint_missiles_required == 0:
            return False
        if self.temp_x == x_goal and self.temp_y == y_goal:
            self.__reset_visited_counter()
            self.planned_route = ["Share special"]
            return True

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
                elif str(self.vision[point.y][point.x])[0] == "U":
                    temp_banned_points.append(point)
                elif (
                    self.vision[point.y][point.x] in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    and self.m_count < self.vision[point.y][point.x]
                ):
                    temp_banned_points.append(point)
                elif not self.__is_safe(point):
                    temp_banned_points.append(point)
                elif (point.y, point.x) in visited_squares_counter_copy.keys():
                    temp_banned_points.append(point)
                    new_points_visited.append(point)
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
                elif self.__breaker(loop_counter):
                    return
                visited_squares_counter_copy[(new_points[0].y, new_points[0].x)] = 0
            elif len(new_points_visited):
                least_visited = 999
                for point in new_points_visited:
                    if (
                        visited_squares_counter_copy[(point.y, point.x)]
                        <= least_visited
                        and str(self.vision[point.y][point.x])[0] != "U"
                        and self.__is_safe(point)
                    ):
                        least_visited = visited_squares_counter_copy[(point.y, point.x)]
                final_point = None
                for point in new_points_visited:
                    if (
                        visited_squares_counter_copy[(point.y, point.x)]
                        == least_visited
                        and str(self.vision[point.y][point.x])[0] != "U"
                        and self.__is_safe(point)
                        and not self.__is_scared(point)
                    ):
                        final_point = point
                        break
                if final_point == None:
                    return False
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
                elif self.__breaker(loop_counter):
                    return False
            elif self.__breaker(loop_counter):
                return False
            else:
                visited_squares_counter_copy = {(self.temp_y, self.temp_x): 0}
                temp_x = self.temp_x
                temp_y = self.temp_y
                missiles_required = 0
                new_route = []
        self.client_missiles_required = missiles_required
        client = None
        for sub in self.sub_list:
            if sub.id == self.client_id:
                client = sub
                break
        if client != None:
            new_route.append("Share special")
            self.planned_route = new_route
        return True

    def __breaker(self, loop_counter: int) -> bool:
        if loop_counter > 100 * self.map_height * self.map_width:
            return True
        return False

    def __get_adjacent_square(self, point_x: int, point_y: int) -> str | bool:
        """Hittar en säker ruta bredvid en given ruta"""
        if point_y <= self.map_height - 1:
            if (
                self.vision[point_y + 1][point_x] == 0
                or self.vision[point_y + 1][point_x] == "S"
                or self.vision[point_y + 1][point_x] == "?"
            ):
                return str(point_y + 1) + str(point_x)
        if self.temp_y > 0:
            if (
                self.vision[point_y - 1][point_x] == 0
                or self.vision[point_y - 1][point_x] == "S"
                or self.vision[point_y - 1][point_x] == "?"
            ):
                return str(point_y - 1) + str(point_x)
        if point_x <= self.map_width - 1:
            if (
                self.vision[point_y][point_x+1] == 0
                or self.vision[point_y][point_x+1] == "S"
                or self.vision[point_y][point_x+1] == "?"
            ):
                return str(point_y) + str(point_x+1)
        if self.temp_x > 0:
            if (
                self.vision[point_y][point_x-1] == 0
                or self.vision[point_y][point_x-1] == "S"
                or self.vision[point_y][point_x-1] == "?"
            ):
                return str(point_y) + str(point_x-1)
        return False

    def __reset_visited_counter(self):
        for key in self.visited_squares_counter.keys():
            if self.visited_squares_counter[key] > 0:
                self.visited_squares_counter[key] = 0

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
        for sub in self.sub_list:
            if sub.static > 1 and not sub.endpoint_reached and sub.client_id == None:
                square = self.__get_adjacent_square(sub.temp_x, sub.temp_y)
                if square != False and self.m_count != 0:
                    if self.__get_client_route(int(square[0]), int(square[1])):
                            return sub.id
                    elif self.__is_adjacent(sub):
                        return sub.id

        return None

    @status_control
    def update_vision(self):
        for sub in self.sub_list:
            if sub.temp_x != None and sub.temp_y != None:
                for i in range(self.map_height):
                    for j in range(self.map_width):
                        if i == sub.temp_y and j == sub.temp_x:
                            self.vision[i][j] = "U" + str(sub.id)
                        elif self.vision[i][j] == "U" + str(sub.id):
                            self.vision[i][j] = 0
            if sub.vision != None:
                for i in range(self.map_height):
                    for j in range(self.map_width):
                        if (
                            sub.vision[i][j] not in {"S", "E", "?"}
                            and sub.vision[i][j] != self.vision[i][j]
                            and self.vision[i][j] not in {"S", "E"}
                        ):
                            self.vision[i][j] = sub.vision[i][j]
                        elif sub.vision[i][j] == "S":
                            self.vision[i][j] = "U" + str(sub.id)
        return

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


    def get_next_position(self, direction):
        """Beräknar nästa position om ubåten skulle flytta."""
        x, y = self.temp_x, self.temp_y
        if direction == "up":
            y += 1
        elif direction == "down":
            y -= 1
        elif direction == "right":
            x += 1
        elif direction == "left":
            x -= 1
        return x, y

    def find_sub_at(self, x, y):
        """Returnerar ubåten vid (x, y) om det finns en där."""
        for sub in self.sub_list:
            if sub.temp_x == x and sub.temp_y == y and sub.is_alive:
                return sub
        return None
