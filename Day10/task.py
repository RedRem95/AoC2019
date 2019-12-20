from typing import List, Iterable

from Day10 import INPUT
from helper import Point, direction, ggt, angle, real_dist
from main import custom_print as custom_printer

ASTEROID_SYMBOL = "#"


class Asteroid(Point):
    def direction(self, other: Point):
        direct = direction(self, other)
        t = abs(ggt(direct.get_x(), direct.get_y()))
        return Point(direct.get_x() / t, direct.get_y() / t)

    def __str__(self):
        return f"Asteroid {super().__str__()}"

    def __repr__(self):
        return str(self)


def create_asteroids(inp: List[str]) -> Iterable[Asteroid]:
    for y, line in enumerate(inp):
        for x, s in enumerate(line):
            if s == ASTEROID_SYMBOL:
                yield Asteroid(x, y)


def vaporization(station: Asteroid, targets: Iterable[Asteroid]) -> Iterable[Asteroid]:
    targets_in_line = {}
    for target in targets:
        if target is not station:
            direct = station.direction(target)
            tmp = targets_in_line.get(direct, [])
            tmp.append(target)
            targets_in_line[direct] = tmp

    for key, value in targets_in_line.items():
        targets_in_line[key] = sorted(value, key=lambda x: real_dist(x, station))

    ref = Point(0, 1)

    lasers = sorted(targets_in_line.keys(), key=lambda x: angle(ref, x))
    it = 0
    while sum((len(x) for x in targets_in_line.values())) > 0:
        laser_fire = lasers[it % len(lasers)]
        it += 1
        targets_in_laser = targets_in_line[laser_fire]
        if len(targets_in_laser) > 0:
            yield targets_in_laser[0]
            targets_in_line[laser_fire] = targets_in_laser[1:]


def main():
    asteroids_list = list(create_asteroids(INPUT))
    custom_printer("A1")
    asteroid_with_partner = ((x, len(set([x.direction(y) for y in asteroids_list if x is not y]))) for x in
                             asteroids_list)
    asteroid_with_partner = sorted(asteroid_with_partner, key=lambda x: x[1])
    best_asteroid = asteroid_with_partner[-1]
    custom_printer(f"Best Ateroid: {best_asteroid[0]} with {best_asteroid[1]} visible partners")
    custom_printer("A2")
    interesting_kills = [1, 2, 3, 10, 20, 50, 100, 199, 200, 201, 299, -1]
    interesting_kills = [x for x in range(1, 299)] + [-1]
    kills = [x for x in vaporization(best_asteroid[0], (x for x in asteroids_list if x is not best_asteroid))]
    custom_printer("\n".join((
        f"The {'last' if x == -1 else f'{x}.'} asteroid to be vaporized is at {kills[x - 1 if x >= 0 else x].get_x()},{kills[x - 1 if x >= 0 else x].get_y()}"
        for x in interesting_kills if x - 1 < len(kills))))
    if len(kills) > 200:
        custom_printer(f"Answer: {kills[200 - 1].get_x() * 100 + kills[200 - 1].get_y()}")

    custom_printer([(i + 1, x) for i, x in enumerate(kills) if x == Point(9, 5)][0])
