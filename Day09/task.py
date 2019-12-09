from typing import List, Tuple, Callable
from Day09 import INPUT

custom_printer = print

from Day05.task import my_mode_machine
from Day02.task import Mode, work_code, CustomCode

my_machine = my_mode_machine.copy()


class RelativeBase:
    def __init__(self, base: int=0):
        self.__base = base

    def get_base(self) -> int:
        return self.__base

    def set_base(self, base: int) -> int:
        self.__base = base
        return self.__base

    def adjust_base(self, inc: int) -> int:
        self.__base += inc
        return self.__base


class RelativeMode(Mode):

    def __init__(self, rel_base: RelativeBase):
        super().__init__()
        self.__rel_base: RelativeBase = rel_base

    def read(self, code: List[int], loc: int) -> int:
        return code[self.__rel_base.get_base() + code[loc]]

    def write(self, code: CustomCode, loc: int, value: int) -> CustomCode:
        code[self.__rel_base.get_base() + code[loc]] = value
        return code


__rel_base = RelativeBase(0)


def __adj_base(code: CustomCode, loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    __rel_base.adjust_base(modes(1).read(code, loc + 1))
    return False, loc + 2


my_machine.register_mode(2, RelativeMode(__rel_base))
my_machine.register_action(9, __adj_base)


def main(printer=print):
    global custom_printer
    custom_printer = printer
    work_code(INPUT, my_machine)

    #custom_printer("Resulting code:", res_code)
