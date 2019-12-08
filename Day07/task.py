import threading
from queue import Queue
from typing import List, Callable, Tuple, Iterable, Union

from Day02.task import work_code, IntMachine, Mode
from Day05.task import my_mode_machine
from Day07 import INPUT
from helper import get_all_combs

custom_printer = print


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
            signal.set_signal(int(modes(1).read(code, loc + 1)))
            return False, loc + 2

        machine.register_action(3, read)
        machine.register_action(4, write)
        amp_code = work_code(code, machine)

    return signal.get_signal()


__lock = threading.Lock()


class IntCodeThread(threading.Thread):

    def __init__(self, my_id: int, max_ids: int, my_queue: Queue, target_queue: Queue,
                 my_code: Union[str, List[int]], my_machine):
        super().__init__(name="InCodeThread->%s" % my_id)
        self.my_id = my_id
        self.__max_ids = max_ids
        self.__my_queue = my_queue
        self.__my_code = my_code
        self.__my_machine = my_machine
        self.__target_queue = target_queue

    def read(self, code_loc: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        # code[code[loc + 1]] = read_int()
        data = self.__my_queue.get()
        modes(1).write(code_loc, loc + 1, data)
        return False, loc + 2

    def write(self, code_loc: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        # print_int(loc + 1, code[code[loc + 1]])
        data = int(modes(1).read(code_loc, loc + 1))
        self.__target_queue.put(data)
        return False, loc + 2

    def run(self) -> None:
        self.__my_machine.register_action(3, self.read)
        self.__my_machine.register_action(4, self.write)
        work_code(self.__my_code, self.__my_machine)


def check_amplifier_rep(code: str, machine: IntMachine, phases: List[int] = [], signal: int = 0):
    threads = []
    queues: List[Queue[int]] = []

    for i, phase in enumerate(phases):
        my_queue: Queue[int] = Queue()
        my_queue.put(phase)
        if i == 0:
            my_queue.put(signal)
        queues.append(my_queue)

    class CustomInt:

        def __init__(self, value):
            self.__value = value

        def set_value(self, value):
            self.__value = value

        def get_value(self):
            return self.__value

    for j in range(len(phases)):
        thread = IntCodeThread(my_id=j, max_ids=len(queues), my_queue=queues[j],
                               target_queue=queues[(j + 1) % len(queues)], my_code="%s" % code,
                               my_machine=machine.copy())

        thread.start()

        threads.append(thread)

    for t in threads:
        t.join()

    return queues[0].get()


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
        amp = check_amplifier_rep(INPUT, my_mode_machine, x, 0)
        if amp > max_amp:
            max_amp = amp
            max_comp = x
    custom_printer("Max-AMP", max_amp, "@", max_comp)
