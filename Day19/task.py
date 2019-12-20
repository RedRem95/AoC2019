from typing import Iterable, Tuple, List, Callable, Union

from Day02.task import Mode, IntMachine, CustomList, work_code
from Day17.task import my_machine
from Day19 import INPUT
from helper import Iterator, Point, get_all_combs
from main import custom_print as custom_printer


def get_affected_pos(inp: Union[List[int], str, CustomList], machine: IntMachine, test_pos: Iterable[Point]) -> List[
    Point]:
    deploy_machine = machine.copy()
    deploy_machine.reset_machine()

    ret: List[Tuple[int, int]] = []

    it = Iterator(0)
    point = Point(0, 0)

    def custom_write(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        value = modes(1).read(read_code, loc + 1)
        if value == 1:
            ret.append(point.copy())
        return False, loc + 2

    def custom_read(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        modes(1).write(read_code, loc + 1, point[it.get() % len(point)])
        it.increase()
        return False, loc + 2

    deploy_machine.register_action(3, custom_read)
    deploy_machine.register_action(4, custom_write)

    for pos in test_pos:
        point.set(pos)
        deploy_machine.reset_machine()
        work_code(inp, deploy_machine)

    return ret


def main():
    aff_points = get_affected_pos(INPUT, my_machine,
                                  (Point(x[0], x[1]) for x in get_all_combs(0, 49, length=2, just_once=False)))

    custom_printer("A1")
    custom_printer(f"Affected points {len(aff_points)}: {', '.join(str(x) for x in aff_points)}")
