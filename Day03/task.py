from typing import List, Dict, Tuple

from Day03 import INPUT
from helper import Point, line_intersect, manhattan_distance, real_dist


def create_points(way: str, origin: Point = Point(0, 0)) -> List[Point]:
    ret: List[Point] = [origin.copy()]
    for direction in (str(x).strip().lower() for x in str(way).split(",")):
        last_point = ret[-1]
        try:
            if direction.startswith("u"):
                ret.append(Point(last_point.get_x(), last_point.get_y() + float(direction[1:])))
            elif direction.startswith("r"):
                ret.append(Point(last_point.get_x() + float(direction[1:]), last_point.get_y()))
            elif direction.startswith("l"):
                ret.append(Point(last_point.get_x() - float(direction[1:]), last_point.get_y()))
            elif direction.startswith("d"):
                ret.append(Point(last_point.get_x(), last_point.get_y() - float(direction[1:])))
            else:
                raise Exception()
        except Exception:
            raise SystemError("Could not parse direction \"%s\"" % direction)
    return ret


def main():
    origin = Point(0, 0)
    points = [create_points(x, origin) for x in INPUT[:2]]
    cross: Dict[Point, Tuple[int, int]] = {}
    i_traveled_dist = 0

    def special_min(x, y):
        x = abs(x)
        y = abs(y)
        if x <= 0:
            return y
        if y <= 0:
            return x
        return min(x, y)

    for i in range(0, len(points[0]) - 1, 1):
        p11 = points[0][i]
        p12 = points[0][i + 1]
        j_traveled_dist = 0
        for j in range(0, len(points[1]) - 1, 1):
            p21 = points[1][j]
            p22 = points[1][j + 1]
            poss_cross = line_intersect(p11, p12, p21, p22)
            if poss_cross:
                if poss_cross not in cross:
                    cross[poss_cross] = (0, 0)
                cross[poss_cross] = (
                    int(special_min(i_traveled_dist + real_dist(p11, poss_cross), cross[poss_cross][0])),
                    int(special_min(j_traveled_dist + real_dist(p21, poss_cross), cross[poss_cross][1])))
            j_traveled_dist += real_dist(p21, p22)
        i_traveled_dist += real_dist(p11, p12)

    print("\tFound crosses %s" % len(cross))
    min_cross = \
        sorted([x for x in cross.keys() if x.get_x() != 0 or x.get_y()],
               key=lambda x: abs(manhattan_distance(x, origin)))[
            0]

    def special_compare(x):
        return x[1][0] + x[1][1]

    fast_cross = sorted([x for x in [(x1, y1) for x1, y1 in cross.items()] if x[0].get_x() != 0 or x[0].get_y() != 0],
                        key=special_compare)[0][0]
    print("\tClosest cross %s at distance %s" % (min_cross, manhattan_distance(min_cross, origin)))
    print("\tCircuit 1 steps: %s" % cross[min_cross][0])
    print("\tCircuit 2 steps: %s" % cross[min_cross][1])
    print("\t Combined steps: %s" % (cross[min_cross][0] + cross[min_cross][1]))
    print("\tFastest cross %s at distance %s" % (fast_cross, manhattan_distance(fast_cross, origin)))
    print("\tCircuit 1 steps: %s" % cross[fast_cross][0])
    print("\tCircuit 2 steps: %s" % cross[fast_cross][1])
    print("\t Combined steps: %s" % (cross[fast_cross][0] + cross[fast_cross][1]))
