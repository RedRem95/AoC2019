from abc import ABC
from typing import List, Callable, Tuple, Union, Dict, Type

from Day02.task import Mode, CustomList, IntMachine, work_code
from Day15.task import MapObject, draw_map, my_machine
from Day17 import INPUT
from helper import Point, Iterator
from main import custom_print as custom_printer


class WorldObject(MapObject, ABC):

    @classmethod
    def get_all_visuals(cls) -> List[str]:
        return [cls().__str__()]


class Robot(WorldObject):

    @classmethod
    def get_all_visuals(cls) -> List[str]:
        return [x for x in Robot.direction_map.values()]

    def get_visual(self) -> str:
        return Robot.direction_map.get(self.__direction, "?")

    direction_map = {
        1: "^",
        2: "v",
        3: "<",
        4: ">",
        0: "X"
    }

    def __init__(self, direction: Union[int, str]):
        if isinstance(direction, str):
            self.__direction = -1
            for key, value in Robot.direction_map.items():
                if value == direction[0]:
                    self.__direction = key
                    break
        else:
            self.__direction = direction


class Scaffold(WorldObject):

    def get_visual(self) -> str:
        return "#"


class Space(WorldObject):

    def get_visual(self) -> str:
        return "."


class World:
    world_objects: List[Type[WorldObject]] = [Scaffold, Space]

    def __init__(self):
        self.__world: Dict[Point, WorldObject] = {}
        self.__robot_pos: Point = None

    def add_object(self, point: Point, world_object: Union[WorldObject, str]):
        if isinstance(world_object, str):
            for t, r in [(x, x.get_all_visuals()) for x in World.world_objects]:
                if world_object in r:
                    return self.add_object(point, t())
        self.__world[point] = world_object
        return

    def draw_map(self, print_crossways_special: Union[str, None] = None) -> List[List[str]]:
        return draw_map(self.__world, robot_pos=self.__robot_pos, default_object=Space(),
                        gone_way=None,
                        point_indexes=None if print_crossways_special is None else {x: print_crossways_special for x in
                                                                                    self.get_crossways(
                                                                                        way_type=Scaffold)})

    def get_crossways(self, way_type: Type[MapObject] = Scaffold) -> List[Point]:

        way_points = [x for x, y in self.__world.items() if isinstance(y, way_type)]

        return [x for x in way_points if all(
            [x.point_up() in way_points, x.point_down() in way_points, x.point_right() in way_points,
             x.point_left() in way_points])]

    def str(self, *args, **kwargs) -> str:
        return "\n".join(("".join((str(x) for x in l)) for l in self.draw_map(*args, **kwargs)))

    def __str__(self):
        return self.str()


def get_world(inp: Union[List[int], str, CustomList], machine: IntMachine) -> World:
    the_world = World()

    deploy_machine = machine.copy()
    deploy_machine.reset_machine()

    line = Iterator(0)
    column = Iterator(0)

    def get_char(value: int) -> str:
        return chr(value)

    def custom_write(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        value = get_char(modes(1).read(read_code, loc + 1))
        if value == "\n":
            line.increase()
            column.reset()
        else:
            the_world.add_object(Point(column.get(), line.get()), value)
            column.increase()
        return False, loc + 2

    def custom_read(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        raise SystemError("Cant write to this machine right now")
        # modes(1).write(read_code, loc + 1, direction)
        return False, loc + 2

    deploy_machine.register_action(3, custom_read)
    deploy_machine.register_action(4, custom_write)

    work_code(inp, deploy_machine)

    return the_world


def main():
    my_world = get_world(INPUT, my_machine)

    custom_printer("The world is like")
    custom_printer(my_world.str(print_crossways_special="O"))
    alignement_parameters = [x.get_x() * x.get_y() for x in my_world.get_crossways()]
    custom_printer("A1")
    custom_printer(
        f"Alignement parameter sum: {sum(alignement_parameters)} => {', '.join(str(x) for x in alignement_parameters)}")
