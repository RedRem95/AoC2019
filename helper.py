import inspect
from math import sqrt, acos, pi
from os import getenv
from os.path import join, dirname, exists
from typing import Union, List, Iterable

import requests


class DownloadFailedError(Exception):
    pass


YEAR = 2019


def load_input(file_name: str = None):
    file_name = file_name if file_name is not None else join(dirname(inspect.getmodule(inspect.stack()[1][0]).__file__),
                                                             "input.txt")
    if not exists(file_name):
        try:
            day = int(dirname(inspect.getmodule(inspect.stack()[1][0]).__file__)[-2:])
            sessid = getenv("ADVENT_OF_CODE_SESSIONID", None)
            if sessid is None:
                print(
                    f"Please give your sessionid as enviroment variable \"{'ADVENT_OF_CODE_SESSIONID'}\" to "
                    f"automatically download the input. Or insert a input.txt with your input into the respective "
                    f"Day* folder")
                raise DownloadFailedError()
            cookies = {'session': sessid}
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}/input', cookies=cookies,
                                    headers=headers)
            print(f"Did the download for Day {day}")
            webpage = response.text
            with open(file_name, "w") as fin:
                fin.write(webpage)
        except:
            raise SystemError("Input does not exist and download of input failed. Sad")
    with open(file_name, "r") as fin:
        return [str(x).strip() for x in fin.readlines()]


class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_x(self, x):
        self.__x = x
        return self

    def set_y(self, y):
        self.__y = y
        return self

    def point_up(self):
        return self.copy().set_y(self.get_y() + 1)

    def point_down(self):
        return self.copy().set_y(self.get_y() - 1)

    def point_right(self):
        return self.copy().set_x(self.get_x() + 1)

    def point_left(self):
        return self.copy().set_x(self.get_x() - 1)

    def __str__(self):
        return "<%s,%s>" % (self.__x, self.__y)

    def __repr__(self):
        return str(self)

    def copy(self):
        return Point(self.__x, self.__y)

    def __hash__(self) -> int:
        return hash((self.__x, self.__y))

    def __eq__(self, other):
        return self.equals(other) if isinstance(other, Point) else False

    def __ne__(self, other):
        return self.__eq__(other)

    def equals(self, other):
        return self.get_x() == other.get_x() and self.get_y() == other.get_y()


def vector_intersect(p11: Point, p12: Point, p21: Point, p22: Point) -> Union[bool, Point]:
    xdiff = (p11.get_x() - p12.get_x(), p21.get_x() - p22.get_x())
    ydiff = (p11.get_y() - p12.get_y(), p21.get_y() - p22.get_y())

    def det(p1: Point, p2: Point):
        return p1.get_x() * p2.get_y() - p2.get_x() * p1.get_y()

    div = det(Point(xdiff[0], xdiff[1]), Point(ydiff[0], ydiff[1]))
    if div == 0:
        return False

    d = (det(p11, p12), det(p21, p22))
    x = det(Point(d[0], d[1]), Point(xdiff[0], xdiff[1])) / div
    y = det(Point(d[0], d[1]), Point(ydiff[0], ydiff[1])) / div
    return Point(x, y)


def line_intersect(p11: Point, p12: Point, p21: Point, p22: Point) -> Union[bool, Point]:
    vec_in = vector_intersect(p11, p12, p21, p22)
    if not vec_in:
        return vec_in
    if not (p11.get_x() <= vec_in.get_x() <= p12.get_x() or p11.get_x() >= vec_in.get_x() >= p12.get_x()):
        return False
    if not (p21.get_x() <= vec_in.get_x() <= p22.get_x() or p21.get_x() >= vec_in.get_x() >= p22.get_x()):
        return False
    if not (p11.get_y() <= vec_in.get_y() <= p12.get_y() or p11.get_y() >= vec_in.get_y() >= p12.get_y()):
        return False
    if not (p21.get_y() <= vec_in.get_y() <= p22.get_y() or p21.get_y() >= vec_in.get_y() >= p22.get_y()):
        return False
    return vec_in


def direction(p1: Point, p2: Point) -> Point:
    return Point(p1.get_x() - p2.get_x(), p1.get_y() - p2.get_y())


def angle(p1: Point, p2: Point) -> float:
    if p1.get_x() - p2.get_x() >= 0:
        return acos((p1.get_x() * p2.get_x() + p1.get_y() * p2.get_y()) / (
                sqrt(p1.get_x() * p1.get_x() + p1.get_y() * p1.get_y()) * sqrt(
            p2.get_x() * p2.get_x() + p2.get_y() * p2.get_y())))
    else:
        return 2 * pi - acos((p1.get_x() * p2.get_x() + p1.get_y() * p2.get_y()) / (
                sqrt(p1.get_x() * p1.get_x() + p1.get_y() * p1.get_y()) * sqrt(
            p2.get_x() * p2.get_x() + p2.get_y() * p2.get_y())))


def manhattan_distance(p1: Point, p2: Point) -> float:
    return abs(p1.get_x() - p2.get_x()) + abs(p1.get_y() - p2.get_y())


def real_dist(p1: Point, p2: Point) -> float:
    d1 = p1.get_x() - p2.get_x()
    d2 = p1.get_y() - p2.get_y()
    return sqrt((d1 * d1) + (d2 * d2))


def partner_check(pw: List[int]):
    for i in range(0, len(pw) - 1, 1):
        if pw[i] == pw[i + 1]:
            return True
    return False


def atleast_one_pair_check(pw: List[int]):
    i = 0
    while i < len(pw):
        sames = 0
        for j in range(i + 1, len(pw), 1):
            if pw[i] == pw[j]:
                sames += 1
            else:
                break
        if sames == 1:
            return True
        i += sames + 1
    return False


def only_increase(pw: List[int]):
    for i in range(0, len(pw) - 1, 1):
        if pw[i] > pw[i + 1]:
            return False
    return True


def int_to_iter(value: int) -> List[int]:
    return [int(x) for x in str(value)]


def get_all_combs(minimum: int = 0, maximum: int = 4, start_list=[], just_once=True, length: int = 4,
                  prohibited: List[int] = []) -> Iterable[List[int]]:
    for i1 in (x for x in range(min(minimum, maximum), max(maximum, minimum) + 1, 1) if x not in prohibited):
        curr_list = start_list.copy()
        curr_list.append(i1)
        cur_prohibited = prohibited.copy()
        if just_once:
            cur_prohibited.append(i1)
        if length <= 1:
            yield curr_list.copy()
        else:
            for x in get_all_combs(minimum=minimum,
                                   maximum=maximum,
                                   start_list=curr_list,
                                   just_once=just_once,
                                   length=length - 1,
                                   prohibited=cur_prohibited):
                yield x


class IntWrapper:
    def __init__(self, init_it: int = 0):
        self.__it: int = init_it
        self.__init_it: int = init_it

    def reset(self):
        self.__it = self.__init_it

    def increase(self, by: int = 1):
        self.__it += by

    def get(self):
        return self.__it

    def set(self, value):
        self.__it = value

    def __str__(self):
        return f"Integer at {self.__it}"


class Iterator(IntWrapper):
    def __init__(self, init_it: int = 0):
        super().__init__(init_it)

    def set(self, value):
        raise NotImplemented("Iterators cant set their value")

    def __str__(self):
        return f"Iterator at {self.__it}"


def ggt(a, b):
    while b != 0:
        c = a % b
        a, b = b, c
    return a


def kgv(a, b):
    return (a * b) / ggt(a, b)


def get_all_combinations(orig: List[List[object]]) -> Iterable[List[object]]:
    if len(orig) > 0:
        for l in orig[0]:
            for x in get_all_combinations(orig[1:]):
                yield [l] + x
    else:
        yield []


from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)
