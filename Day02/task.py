from abc import ABC, abstractmethod
from typing import List, Callable, Tuple, Dict, Iterable, Union

from Day02 import INPUT
from helper import int_to_iter

custom_print = print


class Mode(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def read(self, code: List[int], loc: int) -> int:
        pass

    @abstractmethod
    def write(self, code: List[int], loc: int, value: int) -> List[int]:
        pass


def add(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    # code[code[loc + 3]] = code[code[loc + 1]] + code[code[loc + 2]]
    modes(3).write(code, loc + 3, modes(1).read(code, loc + 1) + modes(2).read(code, loc + 2))
    return False, loc + 4


def mult(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    # code[code[loc + 3]] = code[code[loc + 1]] * code[code[loc + 2]]
    modes(3).write(code, loc + 3, modes(1).read(code, loc + 1) * modes(2).read(code, loc + 2))
    return False, loc + 4


def halt(code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
    return True, loc + 1


class PositionMode(Mode):

    def read(self, code: List[int], loc: int):
        return code[code[loc]]

    def write(self, code: List[int], loc: int, value: int):
        code[code[loc]] = value
        return code


class ImmediateMode(Mode):

    def read(self, code: List[int], loc: int) -> int:
        return code[loc]

    def write(self, code: List[int], loc: int, value: int) -> List[int]:
        raise SystemError("Cant write in ImmediateMode")


class IntMachine:

    def __init__(self):
        self.__action: Dict[int, Callable[[List[int], int, Callable[[int], Mode]], Tuple[bool, int]]] = {}
        self.__modes: Dict[int, Mode] = {}
        self.__default_mode = None

    def register_action(self, code: int, action: Callable[[List[int], int, Callable[[int], Mode]], Tuple[bool, int]]):
        self.__action[code] = action

    def register_mode(self, code: int, mode: Mode):
        self.__modes[code] = mode

    def has_action(self, code: int) -> bool:
        return code in self.__action

    def has_mode(self, code: int) -> bool:
        return code in self.__modes

    def get_action(self, code: int) -> Callable[[List[int], int, Callable[[int], Mode]], Tuple[bool, int]]:
        return self.__action[code]

    def get_mode(self, code: int) -> Mode:
        if code is None:
            return self.__default_mode
        return self.__modes.get(code, self.__default_mode)

    def set_default_mode(self, code_mode: Union[Mode, int]):
        if isinstance(code_mode, int):
            code_mode = self.get_mode(code_mode)
        self.__default_mode = code_mode

    def get_avaiable_actions(self) -> Iterable[int]:
        return (int(x) for x in self.__action.keys())

    def copy(self):
        ret = IntMachine()
        for x, y in self.__action.items():
            ret.register_action(x, y)
        for x, y in self.__modes.items():
            ret.register_mode(x, y)
        ret.set_default_mode(self.__default_mode)
        return ret


default_int_machine = IntMachine()
default_int_machine.register_action(1, add)
default_int_machine.register_action(2, mult)
default_int_machine.register_action(99, halt)
default_int_machine.register_mode(0, PositionMode())
default_int_machine.register_mode(1, ImmediateMode())
default_int_machine.set_default_mode(0)


def parse_int_code(codes: str) -> List[int]:
    if len(codes) > 0:
        return [int(str(x).strip()) for x in str(codes).split(",")]
    else:
        return []


def work_code(code: Union[List[int], str], machine: IntMachine = default_int_machine) -> List[int]:
    if not isinstance(code, list):
        code = parse_int_code(code)
    else:
        code = code.copy()
    loc = 0

    def generate_op_mode(loc: int) -> Tuple[int, Callable[[int], Union[int, None]]]:
        ints = int_to_iter(loc)
        if len(ints) == 1:
            return ints[0], lambda x: None
        op = int(str("".join([str(x) for x in ints[-2:]])))
        return op, lambda x: ints[-1 * x - 2] if x - 1 < len(ints) - 2 else None

    try:
        while machine.has_action(generate_op_mode(code[loc])[0]):
            op, modes_gen = generate_op_mode(code[loc])
            halt_code, new_loc = machine.get_action(op)(code, loc, lambda x: machine.get_mode(modes_gen(x)))
            if halt_code:
                return code
            loc = new_loc
        raise SystemError(
            "Code %s unknown. Known codes: [%s]" % (
                code[loc], ", ".join([str(x) for x in machine.get_avaiable_actions()])))
    except IndexError:
        raise SystemError("code at place %s unparsable cause of Indexerror" % code[loc])


def calc_output(code, noun, verb):
    code = code.copy()
    code[1] = noun
    code[2] = verb
    return work_code(code)[0]


def main(printer=print):
    global custom_print
    custom_print = printer
    code = parse_int_code(INPUT)
    custom_print("A1:", calc_output(code, 12, 2))
    searched_output = 19690720
    out_count = 0
    calc_ans = lambda n, v: 100 * n + v
    custom_print("A2:")
    for noun in range(0, 99 + 1, 1):
        for verb in range(0, 99 + 1, 1):
            output = calc_output(code, noun, verb)
            if output == searched_output:
                out_count += 1
                custom_print("\tOut %s" % out_count)
                custom_print("\t\tNoun:", noun)
                custom_print("\t\tVerb:", verb)
                custom_print("\t\t Ans:", calc_ans(noun, verb))
                custom_print("\t\t Out:", output)
