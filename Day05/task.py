from typing import List, Tuple, Callable

from Day02.task import default_int_machine, work_code, Mode
from Day05 import INPUT

my_machine = default_int_machine.copy()


def read_int():
    while True:
        try:
            return int(input("Give int pls: "))
        except ValueError:
            print("Not a valid int")


def print_int(pos: int, value: int):
    print(value)


def read(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    # code[code[loc + 1]] = read_int()
    modes(1).write(code, loc + 1, read_int())
    return False, loc + 2


def write(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    # print_int(loc + 1, code[code[loc + 1]])
    print_int(loc + 1, modes(1).read(code, loc + 1))
    return False, loc + 2


def jump_if_true(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    if modes(1).read(code, loc + 1) != 0:
        return False, modes(2).read(code, loc + 2)
    return False, loc + 3


def jump_if_false(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    if modes(1).read(code, loc + 1) == 0:
        return False, modes(2).read(code, loc + 2)
    return False, loc + 3


def less_than(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    modes(3).write(code, loc + 3, 1 if modes(1).read(code, loc + 1) < modes(2).read(code, loc + 2) else 0)
    return False, loc + 4


def equal_with(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    modes(3).write(code, loc + 3, 1 if modes(1).read(code, loc + 1) == modes(2).read(code, loc + 2) else 0)
    return False, loc + 4


my_machine.register_action(3, read)
my_machine.register_action(4, write)


def main():
    print("A1")
    work_code(INPUT, my_machine)
    print("A2")
    my_machine.register_action(5, jump_if_true)
    my_machine.register_action(6, jump_if_false)
    my_machine.register_action(7, less_than)
    my_machine.register_action(8, equal_with)
    work_code(INPUT, my_machine)
