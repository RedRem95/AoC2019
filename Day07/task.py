from typing import List, Callable, Tuple, Iterable

from Day02.task import work_code, IntMachine, Mode
from Day05.task import my_mode_machine
from Day07 import INPUT
from helper import get_all_combs

custom_printer = print

my_mode_machine = my_mode_machine.copy()

INPUT = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"


class Signal:
    def __init__(self, init_signal=0):
        self.__signal = init_signal

    def set_signal(self, new_signal):
        self.__signal = new_signal

    def get_signal(self):
        return self.__signal


class Iterator:
    def __init__(self, init_it):
        self.__it = init_it

    def increase(self, by=1):
        self.__it += by

    def get(self):
        return self.__it


def check_amplifier(code: str, machine: IntMachine, phases: Iterable[int] = [], signal: int = 0):
    signal = Signal(signal)
    it = Iterator(0)

    for amp_id, phase in enumerate(phases):
        data = [phase, signal.get_signal()]

        def read(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
            # code[code[loc + 1]] = read_int()
            modes(1).write(code, loc + 1, data[it.get() % 2])
            it.increase(1)
            return False, loc + 2

        def write(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
            # print_int(loc + 1, code[code[loc + 1]])
            signal.set_signal(int(modes(1).read(code, loc + 1)))
            return False, loc + 2

        machine.register_action(3, read)
        machine.register_action(4, write)
        amp_code = work_code(code, machine)

    return signal.get_signal()


def check_amplifier_rep(code: str, machine: IntMachine, phases: Iterable[int] = [], signal: int = 0):
    signal = Signal(signal)

    def read(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        global __it
        # code[code[loc + 1]] = read_int()
        modes(1).write(code, loc + 1, data[__it % 2])
        __it += 1
        return False, loc + 2

    def write(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        # print_int(loc + 1, code[code[loc + 1]])
        signal.set_signal(int(modes(1).read(code, loc + 1)))
        return False, loc + 2

    machine.register_action(3, read)
    machine.register_action(4, write)


def main(printer: print):
    global custom_printer
    custom_printer = printer
    max_amp = 0
    max_comp = []
    custom_printer("A1")
    for x in get_all_combs():
        amp = check_amplifier(INPUT, my_mode_machine, x, 0)
        if amp > max_amp:
            max_amp = amp
            max_comp = x
    custom_printer("Max-AMP", max_amp, "@", max_comp)

    max_amp = 0
    max_comp = []
    custom_printer("A2")
    for x in get_all_combs(minimum=5, maximum=9):
        amp = check_amplifier(INPUT, my_mode_machine, x, 0)
        if amp > max_amp:
            max_amp = amp
            max_comp = x
    custom_printer("Max-AMP", max_amp, "@", max_comp)
