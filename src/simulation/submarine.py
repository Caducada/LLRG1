import math
from simulation.point import Point


class Submarine:
    def __init__(
        self,
        id: int,
        map: list,
        planned_route: list = [],
        secret_keys: dict = {},
        temp_x: int = -1,
        temp_y: int = -1,
        x0=None,
        y0=None,
        xe=None,
        ye=None,
        m_count=0,
        endpoint_status=None,
        is_alive=True,
    ) -> None:
        self.id = id
        self.x0 = x0
        self.y0 = y0
        self.temp_x = temp_x
        self.temp_y = temp_y
        self.xe = xe
        self.ye = ye
        self.m_count = m_count
        self.planned_route = planned_route
        self.secret_keys = secret_keys
        self.map = list(reversed(map))
        self.sub_list = []
        self.map_height = len(self.map)
        self.map_width = len(self.map[0])
        self.vision = self.__get_starting_vision()
        self.endpoint_status = endpoint_status
        self.is_alive = is_alive
        if self.y0 != None:
            self.temp_y = self.y0
        if self.x0 != None:
            self.temp_x = self.x0

    def __get_starting_vision(self) -> list:
        wrapper_list = []
        for i in range(self.map_height):
            inner_list = []
            for j in range(self.map_width):
                if j == self.temp_x and i == self.temp_y:
                    inner_list.append("0")
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
        self.set_endpoint_status()
        if not self.is_alive:
            raise ValueError("Can't move terminated sub")
        elif self.endpoint_reached:
            raise ValueError("Endpoint reached")
        if direction == "up":
            if self.temp_y != self.map_height:
                if self.map[self.temp_y - 1][self.temp_x] == "B":
                    self.is_alive = False
                elif self.map[self.temp_y - 1][self.temp_x] == 0:
                    self.temp_y += 1
                    self.vision[self.temp_y][self.temp_x] = 0
        elif direction == "down":
            if self.temp_y != 0:
                if self.map[self.temp_y + 1][self.temp_x] == "B":
                    self.is_alive = False
                elif self.map[self.temp_y + 1][self.temp_x] == 0:
                    self.temp_y -= 1
                    self.vision[self.temp_y][self.temp_x] = 0
        elif direction == "right":
            if self.temp_x != self.map_width:
                if self.map[self.temp_y][self.temp_x + 1] == "B":
                    self.is_alive = False
                elif self.map[self.temp_y][self.temp_x + 1] == 0:
                    self.temp_x += 1
                    self.vision[self.temp_y][self.temp_x] = 0
        elif direction == "left":
            if self.temp_x != 0:
                if self.map[self.temp_y][self.temp_x - 1] == "B":
                    self.is_alive = False
                elif self.map[self.temp_y][self.temp_x - 1] == 0:
                    self.temp_x -= 1
                    self.vision[self.temp_y][self.temp_x] = 0
        else:
            raise ValueError("Invalid direction")

    def set_endpoint_status(self) -> None:
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.endpoint_reached = True
        self.endpoint_reached = False

    def get_vision(self, external_id: int, external_vision: list) -> None:
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

    def get_endpoint_data(
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
                sub.endpoint_status = external_endpoint_status
                return
        self.sub_list.append(
            Submarine(
                id=external_id,
                xe=external_xe,
                ye=external_ye,
                endpoint_status=external_endpoint_status,
                map=self.map,
            )
        )

    def get_missile_data(self, external_id: int, external_m_count: int) -> None:
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

    def get_route(self, external_id, external_route) -> None:
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

    def get_secret(self, external_id, external_key) -> None:
        self.secret_keys.setdefault(external_id, external_key)

    def scan_area(self):
        if self.temp_y != self.map_height:
            self.vision[self.temp_y + 1][self.temp_x] = self.map[self.temp_y + 1][
                self.temp_x
            ]
        if self.temp_y != 0:
            self.vision[self.temp_y - 1][self.temp_x] = self.map[self.temp_y + 1][
                self.temp_x
            ]
        if self.temp_x != self.map_width:
            self.vision[self.temp_y][self.temp_x + 1] = self.map[self.temp_y][
                self.temp_x + 1
            ]
        if self.temp_x != 0:
            self.vision[self.temp_y][self.temp_x - 1] = self.map[self.temp_y][
                self.temp_x - 1
            ]
        self.get_new_route()

    def get_new_route(self) -> None:
        banned_squares = []
        temp_x = self.temp_x
        temp_y = self.temp_y
        time_points = {str(temp_y) + str(temp_x):0}
        while True:
            breaker = True
            new_route = []
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
            for point in new_points:
                if point.x >= self.map_width:
                    new_points.remove(point)
                elif point.y >= self.map_height:
                    new_points.remove(point)
                elif (
                    self.vision[point.y][point.x] != 0
                    and self.vision[point.y][point.x] != "?"
                ):
                    new_points.remove(point)
                elif point in banned_squares:
                    new_points.remove(point)
                elif str(point.y) + str(point.x) in time_points:
                    new_points_visited.append(point)
                    new_points.remove(point)
            if not len(new_points):
                new_points_visited = sorted(
                    new_points_visited,
                    key=lambda point: time_points[str(point.y) + str(point.x)],
                )
                banned_squares.append(point)
                breaker = False
                new_route.append(new_points_visited[0])
                if new_points_visited[0].direction == "up":
                    temp_y += 1
                elif new_points_visited[0].direction == "down":
                    temp_y -= 1
                elif new_points_visited[0].direction == "right":
                    temp_x += 1
                elif new_points_visited[0].direction == "left":
                    temp_x -= 1
            else:
                if point in banned_squares:
                    banned_squares.remove(point)
                time_points.setdefault(
                    str(new_points[0].y) + str(new_points[0].x), len(new_route)
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
                if self.xe == temp_x and self.ye == temp_y and breaker:
                    break
        self.planned_route = new_route
