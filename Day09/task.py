from typing import List, Tuple, Callable

from Day09 import INPUT
from helper import Iterator
from main import AUTOMATIC

custom_printer = print

from Day05.task import my_mode_machine
from Day02.task import Mode, work_code, CustomList

my_machine = my_mode_machine.copy()


class RelativeBase:
    def __init__(self, base: int = 0):
        self.__base = base
        self.__init_base = base

    def get_base(self) -> int:
        return self.__base

    def set_base(self, base: int) -> int:
        self.__base = base
        return self.__base

    def adjust_base(self, inc: int) -> int:
        self.__base += inc
        return self.__base

    def reset_base(self):
        self.__base = self.__init_base


class RelativeMode(Mode):

    def machine_restarts(self):
        self.__rel_base.reset_base()

    def __init__(self, rel_base: RelativeBase):
        super().__init__()
        self.__rel_base: RelativeBase = rel_base

    def read(self, code: List[int], loc: int) -> int:
        return code[self.__rel_base.get_base() + code[loc]]

    def write(self, code: CustomList, loc: int, value: int) -> CustomList:
        code[self.__rel_base.get_base() + code[loc]] = value
        return code

    def copy(self) -> Mode:
        return RelativeMode(RelativeBase(self.__rel_base.get_base()))


__rel_base = RelativeBase(0)


def __adj_base(code: CustomList, loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    __rel_base.adjust_base(modes(1).read(code, loc + 1))
    return False, loc + 2


my_machine.register_mode(2, RelativeMode(__rel_base))
my_machine.register_action(9, __adj_base)


def main(printer=print):
    global custom_printer
    custom_printer = printer

    used_machine1 = my_machine.copy()
    used_machine2 = my_machine.copy()

    if AUTOMATIC:
        it = Iterator(0)

        def memory():
            ret = [1, 2][it.get() % 2]
            it.increase()
            custom_printer("Memory said", ret)
            return ret

        def read_memory(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
            modes(1).write(code, loc + 1, memory())
            return False, loc + 2

        used_machine1 = used_machine1.copy()
        used_machine2 = used_machine2.copy()
        used_machine1.register_action(3, read_memory)
        used_machine2.register_action(3, read_memory)

    custom_printer("A1")
    work_code(INPUT, used_machine1)
    custom_printer("A2")
    work_code(INPUT, used_machine2)

    # custom_printer("Resulting code:", res_code)
