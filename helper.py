import inspect
from math import sqrt
from os.path import join, dirname
from typing import Union, List, Iterable


def load_input(file_name: str = None):
    file_name = file_name if file_name is not None else join(dirname(inspect.getmodule(inspect.stack()[1][0]).__file__),
                                                             "input.txt")
    with open(file_name, "r") as fin:
        lines = [str(x).strip() for x in fin.readlines()]
    return lines


class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def __str__(self):
        return "<%s,%s>" % (self.__x, self.__y)

    def copy(self):
        return Point(self.__x, self.__y)

    def __hash__(self) -> int:
        return hash((self.__x, self.__y))


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
                  prohibited: List[int] = []) -> Iterable[
    List[int]]:
    for i1 in (x for x in range(min(minimum, maximum), max(maximum, minimum) + 1, 1) if x not in prohibited):
        curr_list = start_list.copy()
        curr_list.append(i1)
        cur_prohibited = prohibited.copy()
        if just_once:
            cur_prohibited.append(i1)
        if length <= 0:
            yield curr_list.copy()
        else:
            for x in get_all_combs(minimum=minimum,
                                   maximum=maximum,
                                   start_list=curr_list,
                                   just_once=just_once,
                                   length=length - 1,
                                   prohibited=cur_prohibited):
                yield x


class Iterator:
    def __init__(self, init_it):
        self.__it = init_it

    def increase(self, by=1):
        self.__it += by

    def get(self):
        return self.__it
