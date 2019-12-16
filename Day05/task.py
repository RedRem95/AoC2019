from typing import List, Tuple, Callable

from Day02.task import default_int_machine, work_code, Mode
from Day05 import INPUT
from helper import Iterator
from main import AUTOMATIC

my_machine = default_int_machine.copy()

custom_print = print


def read_int(message: str = "Give int pls: "):
    while True:
        try:
            return int(input(message))
        except ValueError:
            custom_print("Not a valid int")


def print_int(pos: int, value: int):
    custom_print(value)


def read(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
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

my_mode_machine = my_machine.copy()

my_mode_machine.register_action(5, jump_if_true)
my_mode_machine.register_action(6, jump_if_false)
my_mode_machine.register_action(7, less_than)
my_mode_machine.register_action(8, equal_with)


def main(printer=print):
    global custom_print
    used_machine1 = my_machine
    used_machine2 = my_mode_machine.copy()

    if AUTOMATIC:
        it = Iterator(0)

        def memory():
            ret = [1, 5][it.get() % 2]
            it.increase()
            custom_print("Memory said", ret)
            return ret

        def read_memory(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
            modes(1).write(code, loc + 1, memory())
            return False, loc + 2

        used_machine1 = used_machine1.copy()
        used_machine2 = used_machine2.copy()
        used_machine1.register_action(3, read_memory)
        used_machine2.register_action(3, read_memory)

    custom_print = printer
    custom_print("A1")
    work_code(INPUT, used_machine1)
    custom_print("A2")
    work_code(INPUT, used_machine2)
