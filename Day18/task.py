from abc import ABC
from math import inf
from queue import Queue, PriorityQueue
from typing import List, Dict, Tuple

from Day15.task import MapObject, Wall as BasicWall, draw_map, fewest_steps
from Day18 import INPUT
from helper import Point
from main import custom_print as custom_printer


class LabyrinthObject(MapObject, ABC):
    pass


class Wall(LabyrinthObject, BasicWall):
    pass


class HallWay(LabyrinthObject):

    def get_visual(self) -> str:
        return "."


class Key(LabyrinthObject):

    def __init__(self, key_value: str):
        self.__key_value = key_value.lower()

    def get_visual(self) -> str:
        return self.__key_value

    def __repr__(self):
        return f"Key {self.get_visual()}"


class Player(LabyrinthObject):

    def __init__(self):
        self.__keys: List[Key] = []

    def get_visual(self) -> str:
        return "@"

    def get_keys(self) -> List[Key]:
        return self.__keys

    def add_key(self, key: Key):
        self.__keys.append(key)

    def copy(self):
        ret = Player()
        for k in self.__keys:
            ret.add_key(k)
        return ret


class Door(LabyrinthObject):

    def __init__(self, door_value: str):
        self.__door_value = door_value.upper()

    def get_visual(self) -> str:
        return self.__door_value

    def does_open(self, *key: Key):
        return self.__door_value.lower() in [str(x.get_visual()).lower() for x in key]


def create_map(inp: List[str]) -> Tuple[Dict[Point, LabyrinthObject], Point, Player]:
    player_pos = None
    player = None
    ret_map = {}
    for y, l in enumerate(inp):
        for x, c in enumerate(l):
            point = Point(x, y)
            obj = HallWay()
            if c == "#":
                obj = Wall()
            elif c == "@":
                player = Player()
                player_pos = point
            elif ord('a') <= ord(c[0]) <= ord('z'):
                obj = Key(c[0])
            elif ord('A') <= ord(c[0]) <= ord('Z'):
                obj = Door(c[0])
            ret_map[point] = obj
    return ret_map, player_pos, player


def keys_in_map(my_map: Dict[Point, LabyrinthObject]) -> List[Tuple[Point, Key]]:
    return [(x, y) for x, y in my_map.items() if isinstance(y, Key)]


def get_way(my_map: Dict[Point, LabyrinthObject], player_pos, player) -> Tuple[List[Key], int]:
    keys_in_my_map = keys_in_map(my_map)

    if len(keys_in_my_map) <= 0:
        return [], 0

    best_key_chain = None
    best_steps = inf

    class PrioritizedItem:
        def __init__(self, work_map: Dict[Point, LabyrinthObject], pos: Point, player_tmp: Player, steps_tmp: int):
            self.work_map = work_map
            self.pos = pos
            self.player = player_tmp
            self.steps = steps_tmp

        def __lt__(self, other):
            if not isinstance(other, PrioritizedItem):
                raise NotImplemented("This is not implemented")
            if len(self.player.get_keys()) == len(other.player.get_keys()):
                keys_in_map_s = len(keys_in_map(self.work_map))
                keys_in_map_o = len(keys_in_map(other.work_map))
                if keys_in_map_o == keys_in_map_s:
                    return self.steps < other.steps
                return keys_in_map_s < keys_in_map_o
            return len(self.player.get_keys()) > len(other.player.get_keys())

        def __gt__(self, other):
            if not isinstance(other, PrioritizedItem):
                raise NotImplemented("This is not implemented")
            return other < self

        def __eq__(self, other):
            if not isinstance(other, PrioritizedItem):
                return False
            return self.pos == other.pos and self.player == other.player and self.work_map == other.work_map

        def __str__(self):
            return f"<{self.player.get_keys()[-1] if len(self.player.get_keys()) > 0 else '@'}, {self.steps}s, {len(self.player.get_keys())}k>"

        def __repr__(self):
            return str(self)

    pq: Queue[PrioritizedItem] = PriorityQueue()
    pq.put(PrioritizedItem(my_map.copy(), player_pos.copy(), player.copy(), 0))

    while not pq.empty():
        pi = pq.get()
        work_map = pi.work_map
        work_player = pi.player
        work_player_pos = pi.pos
        work_steps = pi.steps

        keys_on_map = keys_in_map(work_map)

        if len(keys_on_map) <= 0:
            if best_key_chain is None or best_steps > work_steps:
                best_key_chain = work_player.get_keys()
                best_steps = work_steps
                custom_printer(f"Found new best way {best_steps} -> [{', '.join(str(x) for x in best_key_chain)}]")
        else:
            blocking = [y for y, x in work_map.items() if
                        isinstance(x, Door) and not x.does_open(*work_player.get_keys())]
            map_steps = {}
            fewest_steps(ship_map=work_map, start_point=work_player_pos, not_passable=blocking, tested_points=map_steps)

            for key_point, key in keys_on_map:
                try:
                    steps = map_steps[key_point]
                    next_map = work_map.copy()
                    next_map[key_point] = HallWay()
                    next_player = work_player.copy()
                    next_player.add_key(key)
                    pq.put(PrioritizedItem(next_map, key_point.copy(), next_player, work_steps + steps))
                except KeyError:
                    pass

    exit(2)

    for key_point, key, steps in ((key_point, key, steps) for key_point, key, steps in steps_to_key if
                                  steps is not None):
        next_map = my_map.copy()
        next_map[key_point] = HallWay()
        next_player = player.copy()
        next_player.add_key(key)
        next_best_chain, next_best_steps = get_way(next_map, key_point, next_player)
        if next_best_chain is not None and (best_key_chain is None or steps + next_best_steps < best_steps):
            best_key_chain = [key] + next_best_chain
            best_steps = steps + next_best_steps
            # custom_printer(f"Found a new best way with {best_steps} => [{', '.join(str(x) for x in best_key_chain)}]")

    return best_key_chain, best_steps


def main():
    my_map, player_pos, player = create_map(INPUT)

    custom_printer("A1")
    custom_printer("Playing map")
    custom_printer("\n".join(("".join((str(x) for x in l)) for l in
                              draw_map(my_map, robot_pos=player_pos, robot=player, default_object=HallWay()))))

    chain, steps = get_way(my_map, player_pos, player)

    custom_printer(f"Best steps in map {steps}: [{', '.join(str(x) for x in chain)}]")
