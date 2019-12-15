from abc import ABC, abstractmethod
from multiprocessing import cpu_count
from multiprocessing.pool import Pool
from queue import PriorityQueue, Queue
from time import time
from typing import List, Callable, Tuple, Dict, Union, Optional, Type

from Day02.task import Mode, IntMachine, work_code, CustomList
from Day11.task import my_machine
from Day15 import INPUT
from helper import Point, Iterator, PrioritizedItem, get_all_combs
from main import AUTOMATIC

custom_printer = print


class MapObject(ABC):
    @abstractmethod
    def get_visual(self) -> str:
        pass

    def __str__(self):
        return self.get_visual()[0]


class Robot(MapObject):

    def get_visual(self) -> str:
        return "D"


class Wall(MapObject):

    def get_visual(self) -> str:
        return "#"


class Tank(MapObject):

    def get_visual(self) -> str:
        return "T"


class HallWay(MapObject):

    def get_visual(self) -> str:
        return " "


class MapBorder(MapObject):

    def get_visual(self) -> str:
        return "+"


direction_ops: Dict[int, Callable[[Point], Point]] = {
    1: lambda p: p.copy().set_y(p.get_y() + 1),
    2: lambda p: p.copy().set_y(p.get_y() - 1),
    3: lambda p: p.copy().set_x(p.get_x() - 1),
    4: lambda p: p.copy().set_x(p.get_x() + 1)
}


def __create_map_by_order(big):
    order: List[int] = big[0]
    i: int = big[1]
    deploy_machine: IntMachine = big[2]
    template1, template2 = big[3]
    ship_map: Dict[Point, MapObject] = big[4]
    ps: bool = big[5]
    bat: bool = big[6]
    input_code: Union[List[int], str, CustomList] = big[7]
    order_len: int = big[8]

    custom_printer(template1.format(i=i + 1, prec=((i + 1) / order_len) * 100, order=order))
    robot_pos = Point(0, 0)
    deploy_machine.reset_machine()

    def direction_from_point(p1: Point, p2: Point) -> int:
        for direction, operation in direction_ops.items():
            if operation(p1).equals(p2):
                return direction
        raise SystemError(f"You cant get from {p1} to {p2} using the given operations")

    lastDirection = [-1]
    gone_way = []
    it = Iterator(1)

    def custom_write(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        new_pos = direction_ops[lastDirection[0]](robot_pos)
        status = modes(1).read(read_code, loc + 1)
        if status == 0:
            ship_map[new_pos] = Wall()
        elif status == 1:
            gone_way.append(robot_pos.copy())
            if new_pos not in gone_way:
                it.reset()
            else:
                it.increase()
            robot_pos.set_x(new_pos.get_x())
            robot_pos.set_y(new_pos.get_y())
        elif status == 2:
            ship_map[new_pos] = Tank()
            return bat, loc + 2
        if ps:
            custom_printer("\n")
            custom_printer(
                "\n".join(("".join((str(x) for x in l)) for l in draw_map(ship_map, robot_pos, gone_way=gone_way))))
            custom_printer(f"Robot-pos {robot_pos}")
        return False, loc + 2

    def custom_read(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        for direction, operation in sorted(((x, y) for x, y in direction_ops.items()), key=lambda x: order.index(x[0])):
            new_pos = operation(robot_pos)
            if not isinstance(ship_map.get(new_pos, HallWay()), Wall) and new_pos not in gone_way:
                modes(1).write(read_code, loc + 1, direction)
                lastDirection[0] = direction
                return False, loc + 2
        try:
            new_pos = gone_way[it.get() * -1]
            it.increase()
            direction = direction_from_point(robot_pos, new_pos)
            modes(1).write(read_code, loc + 1, direction)
            lastDirection[0] = direction
            return False, loc + 2
        except IndexError:
            raise SystemError("No direction is possible, wtf")

    deploy_machine.register_action(3, custom_read)
    deploy_machine.register_action(4, custom_write)

    work_code(input_code, deploy_machine)

    custom_printer(template2.format(i=i + 1, prec=((i + 1) / order_len) * 100, order=order))

    return ship_map


def get_map(inp: Union[List[int], str, CustomList], machine: IntMachine, print_steps=False, break_at_tank=True,
            initial_map: Dict[Point, MapObject] = {}, thread_count: int = cpu_count()) -> Dict[Point, MapObject]:
    global_map: Dict[Point, MapObject] = {}
    orders = [x for x in get_all_combs(minimum=1, maximum=4, just_once=True, length=4)]
    tmpl1 = "Starting  order {i:%s}/%s ({prec:6.2f}%s) -> {order}" % (len(str(len(orders))), len(orders), "%")
    tmpl2 = "Finishing order {i:%s}/%s ({prec:6.2f}%s) -> {order}" % (len(str(len(orders))), len(orders), "%")

    with Pool(thread_count) as thread_pool:
        start_time = time()
        custom_printer(f"Starting to calculate {len(orders)} configurations on {thread_count} processes")
        ship_maps = thread_pool.map(__create_map_by_order, [
            (x, i, machine.copy(), (tmpl1, tmpl2), initial_map.copy(), print_steps, break_at_tank, inp, len(orders)) for
            i, x in enumerate(orders)])
        end_time = time()
        custom_printer(
            f"It took {(end_time - start_time) * 1000:10.3f}ms to let the robot run with {len(orders)} configurations on {thread_count} processes")

    for ship_map in ship_maps:
        for p, obj in ship_map.items():
            if p not in global_map:
                global_map[p] = obj
            elif global_map[p].__class__ != obj.__class__:
                raise SystemError("Diffrent movements get diffrent maps. Thats weired")

    return global_map


def draw_map(ship_map: Dict[Point, MapObject], robot_pos: Optional[Point] = None,
             default_object: Union[MapObject, str] = HallWay(), gone_way: List[Point] = None, point_indexes=None) -> \
        List[List[str]]:
    x_l = [x.get_x() for x in [x for x in ship_map.keys()] + ([robot_pos] if isinstance(robot_pos, Point) else [])]
    y_l = [x.get_y() for x in [x for x in ship_map.keys()] + ([robot_pos] if isinstance(robot_pos, Point) else [])]
    min_x, max_x = min(x_l), max(x_l)
    min_y, max_y = min(y_l), max(y_l)

    map_to_draw = ship_map.copy()
    for x in range(min_x - 1, max_x + 2, 1):
        map_to_draw[Point(x, min_y - 1)] = MapBorder()
        map_to_draw[Point(x, max_y + 1)] = MapBorder()

    for y in range(min_y - 1, max_y + 2, 1):
        map_to_draw[Point(min_x - 1, y)] = MapBorder()
        map_to_draw[Point(max_x + 1, y)] = MapBorder()

    def get_hallway(p: Point):
        try:
            if isinstance(gone_way, list):
                return str(gone_way.index(p))[-1]
            elif isinstance(point_indexes, dict):
                return str(point_indexes[p])[-1]
        except Exception:
            return default_object

    return [[str(Robot() if robot_pos is not None and Point(x, y).__eq__(robot_pos) else map_to_draw.get(Point(x, y),
                                                                                                         get_hallway(
                                                                                                             Point(x,
                                                                                                                   y))))
             for x in range(min_x - 1, max_x + 2, +1)] for y in
            range(max_y + 1, min_y - 2, -1)]


def fewest_steps(ship_map: Dict[Point, MapObject], start_point: Point = Point(0, 0),
                 target_point: Optional[Point] = None,
                 evil_objects: List[Type[MapObject]] = [Wall], tested_points: Dict[Point, int] = {}, current_index=0) -> \
        Union[int, None]:
    if start_point == target_point:
        return 0
    if (start_point in tested_points and current_index > tested_points[start_point]) or any(
            isinstance(ship_map[start_point], x) if start_point in ship_map else False for x in evil_objects):
        return None
    x_l = [x.get_x() for x in ship_map.keys()]
    y_l = [x.get_y() for x in ship_map.keys()]
    min_x, max_x = min(x_l), max(x_l)
    min_y, max_y = min(y_l), max(y_l)

    it = Iterator(0)

    pq: Queue[PrioritizedItem] = PriorityQueue()
    pq.put(PrioritizedItem(it.get(), start_point))

    while not pq.empty():
        testing_point = pq.get()
        index, testing_point = testing_point.priority, testing_point.item
        if testing_point == target_point:
            return index
        index += 1
        test_points = [x(testing_point) for x in direction_ops.values()]
        for tp in (x for x in test_points if min_x <= x.get_x() <= max_x and min_y <= x.get_y() <= max_y and not any(
                isinstance(ship_map[x], y) if x in ship_map else False for y in evil_objects)):
            if tp not in tested_points or tested_points[tp] > index:
                pq.put(PrioritizedItem(index, tp))
                tested_points[tp] = index

    return max((x for x in tested_points.values()))


def main(printer=print):
    global custom_printer
    custom_printer = printer
    if not AUTOMATIC:
        custom_printer("Robot gets started to draw a map")
        created_map = get_map(INPUT, my_machine, print_steps=False, break_at_tank=True, thread_count=cpu_count() - 1)
        custom_printer("Resulting map")
        custom_printer("\n".join(("".join((str(x) for x in l)) for l in draw_map(created_map, robot_pos=Point(0, 0)))))
        point_indexes = {}
        shortes_way = fewest_steps(ship_map=created_map, start_point=Point(0, 0),
                                   target_point=[x for x, y in created_map.items() if isinstance(y, Tank)][0],
                                   tested_points=point_indexes)
        if shortes_way is None:
            custom_printer("You cant get to the tank")
        else:
            custom_printer(f"Fewest steps to the tank are {shortes_way}")

        point_indexes = {}
        shortes_way = fewest_steps(ship_map=created_map,
                                   start_point=[x for x, y in created_map.items() if isinstance(y, Tank)][0],
                                   target_point=None,
                                   tested_points=point_indexes)
        if shortes_way is None:
            custom_printer("You cant fill everything")
        else:
            custom_printer(f"Fewest steps to fill everything are {shortes_way}")
