class Submarine:
    def __init__(
        self,
        id: int,
        map_height: int,
        map_width: int,
        map: list,
        planned_route: list = [],
        secret_keys: dict = {},
        temp_x: int = -1,
        temp_y: int = -1,
        x0=None,
        y0=None,
        xe=None,
        ye=None,
        m_count=None,
        endpoint_status=None,
    ) -> None:
        self.id = id
        self.x0 = x0
        self.y0 = y0
        self.temp_x = temp_x
        self.temp_y = temp_y
        self.xe = xe
        self.ye = ye
        self.m_count = m_count
        self.map_height = map_height
        self.map_width = map_width
        self.map = map
        self.planned_route = planned_route
        self.secret_keys = secret_keys
        self.sub_list = []
        self.vision = self.get_vision()
        self.endpoint_status = endpoint_status

    def get_vision(self) -> list:
        wrapper_list = []
        for i in range(self.map_height):
            inner_list = []
            for j in range(self.map_width):
                if j == self.temp_x and i == self.temp_y:
                    inner_list.append("0")
                else:
                    inner_list.append("?")
            self.vision.append(inner_list)
        return wrapper_list

    def missile_shoot(self) -> bool:
        if self.m_count >= 1:
            self.m_count -= 1
            return True
        else:
            return False

    def move_sub(self, direction: str) -> None:
        self.set_endpoint_status()
        if self.endpoint_reached:
            raise ValueError("Endpoint reached")
        if direction == "up":
            if self.temp_y < self.map_height:
                self.temp_y += 1
        elif direction == "down":
            if self.temp_y > 0:
                self.temp_y -= 1
        elif direction == "right":
            if self.temp_x < self.map_width:
                self.temp_x += 1
        elif direction == "left":
            if self.temp_x > 0:
                self.temp_x -= 1
        else:
            raise ValueError("Invalid direction")

    def set_endpoint_status(self) -> None:
        if self.temp_x == self.xe and self.temp_y == self.ye:
            self.endpoint_reached = True
        self.endpoint_reached = False

    def get_vision(self, external_id: int, external_vision: list) -> None:
        for sub in self.sub_list:
            if sub.id == external_id:
                sub.vision == external_vision
                return
        new_sub = Submarine(
            id=external_id,
            map_height=self.map_height,
            map_width=self.map_width,
            map=self.map,
        )
        new_sub.vision = external_vision
        self.sub_list.append(new_sub)

    def merge_vision(self):
        pass

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
                map_height=self.map_height,
                map_width=self.map_width,
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
                map_height=self.map_height,
                map_width=self.map_width,
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
                map_height=self.map_height,
                map_width=self.map_width,
                map=self.map,
                planned_route=external_route,
            )
        )

    def get_secret(self, external_id, external_key):
        self.secret_keys.setdefault(external_id, external_key)

    def scan_area(self):
        pass
