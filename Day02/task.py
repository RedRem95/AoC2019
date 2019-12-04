from typing import List, Callable, Tuple, Dict, Iterable, Union

from Day02 import INPUT


def add(code: List[int], loc: int) -> Tuple[bool, int]:
    code[code[loc + 3]] = code[code[loc + 1]] + code[code[loc + 2]]
    return False, 3


def mult(code: List[int], loc: int) -> Tuple[bool, int]:
    code[code[loc + 3]] = code[code[loc + 1]] * code[code[loc + 2]]
    return False, 3


def halt(code: List[int], loc: int) -> Tuple[bool, int]:
    return True, 0


class IntMachine:

    def __init__(self):
        self.__action: Dict[int, Callable[[List[int], int], Tuple[bool, int]]] = {}

    def register_action(self, code: int, action: Callable[[List[int], int], Tuple[bool, int]]):
        self.__action[code] = action

    def has_code(self, code: int) -> bool:
        return code in self.__action

    def get_action(self, code: int) -> Callable[[List[int], int], Tuple[bool, int]]:
        return self.__action[code]

    def get_avaiable_actions(self) -> Iterable[int]:
        return (int(x) for x in self.__action.keys())


default_int_machine = IntMachine()
default_int_machine.register_action(1, add)
default_int_machine.register_action(2, mult)
default_int_machine.register_action(99, halt)


def parse_int_code(codes: str) -> List[int]:
    return [int(str(x).strip()) for x in str(codes).split(",")]


def work_code(code: Union[List[int], str], machine: IntMachine = default_int_machine):
    if not isinstance(code, list):
        code = parse_int_code(code)
    else:
        code = code.copy()
    loc = 0

    try:
        while machine.has_code(code[loc]):
            halt_code, param_count = machine.get_action(code[loc])(code, loc)
            if halt_code:
                return code
            loc += (param_count + 1)
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


def main():
    code = parse_int_code(INPUT)
    print("A1:", calc_output(code, 12, 2))
    searched_output = 19690720
    out_count = 0
    calc_ans = lambda n, v: 100 * n + v
    print("A2:")
    for noun in range(0, 99 + 1, 1):
        for verb in range(0, 99 + 1, 1):
            output = calc_output(code, noun, verb)
            if output == searched_output:
                out_count += 1
                print("\tOut %s" % out_count)
                print("\t\tNoun:", noun)
                print("\t\tVerb:", verb)
                print("\t\t Ans:", calc_ans(noun, verb))
                print("\t\t Out:", output)
