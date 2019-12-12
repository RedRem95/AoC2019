from typing import Iterable, List

from Day12 import INPUT

custom_printer = print

INPUT = [
    "<x=-8, y=-10, z=0>",
    "<x=5, y=5, z=10>",
    "<x=2, y=-7, z=3>",
    "<x=9, y=-8, z=-3>"
]

INPUT = [
    "<x=-1, y=0, z=2>",
    "<x=2, y=-10, z=-7>",
    "<x=4, y=-8, z=8>",
    "<x=3, y=5, z=-1>",
]


class Moon:

    def __init__(self, content):
        splitted = str(content).split(",")
        self.__x = int(splitted[0].split("=")[1])
        self.__y = int(splitted[1].split("=")[1])
        self.__z = int(splitted[2].split("=")[1].rstrip(">"))

        self.__vx = 0
        self.__vy = 0
        self.__vz = 0

        self.__my_way = []

    def get_pos(self):
        return self.get_x(), self.get_y(), self.get_z()

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_z(self):
        return self.__z

    def get_vx(self):
        return self.__vx

    def get_vy(self):
        return self.__vy

    def get_vz(self):
        return self.__vz

    def get_pot_energ(self):
        return (abs(self.get_x()) + abs(self.get_y()) + abs(self.get_z())) * (
                abs(self.get_vx()) + abs(self.get_vy()) + abs(self.get_vz()))

    def __str__(self):
        return f"pos=<x={self.get_x()}, y={self.get_y()}, z={self.get_z()}>, vel=<x={self.get_vx()}, y={self.get_vy()}, z={self.get_vz()}>"

    def apply_velo(self):
        self.__my_way.append(self.get_pos())
        self.__x += self.get_vx()
        self.__y += self.get_vy()
        self.__z += self.get_vz()

    def have_i_been_here(self):
        return self.get_pos() in self.__my_way

    def velo_by(self, other):
        if other.get_x() > self.get_x():
            self.__vx += 1
        elif other.get_x() < self.get_x():
            self.__vx -= 1

        if other.get_y() > self.get_y():
            self.__vy += 1
        elif other.get_y() < self.get_y():
            self.__vy -= 1

        if other.get_z() > self.get_z():
            self.__vz += 1
        elif other.get_z() < self.get_z():
            self.__vz -= 1


def calc_velo(moon: Moon, other_moons: Iterable[Moon]):
    for other_moon in (x for x in other_moons if x is not moon):
        moon.velo_by(other_moon)


def simulate(moons: List[Moon], steps=None):
    if steps is None:
        iteration = 0
        while True:
            iteration += 1
            if iteration % 100 == 0:
                custom_printer(f"Currently in iteration {iteration}/2772 {(iteration / 2772) * 100:.2f}%")
            for m in moons:
                calc_velo(m, moons)
            for m in moons:
                m.apply_velo()
            if all(x.have_i_been_here() for x in moons):
                return iteration
    else:
        custom_printer("After 0 steps")
        custom_printer("\n".join((str(x) for x in moons)))

        for i in range(steps):
            for m in moons:
                calc_velo(m, moons)
            for m in moons:
                m.apply_velo()
            if (i + 1) % 10 == 0:
                custom_printer(f"After {i + 1} steps")
                custom_printer("\n".join((str(x) for x in moons)))

        custom_printer(f"After {steps} steps")
        custom_printer("\n".join((str(x) for x in moons)))
        custom_printer("Pot_energ:")
        custom_printer("\n".join(f"{i}: {x.get_pot_energ()}" for i, x in enumerate(moons)))

        custom_printer(f"Sum pot energ: {sum(x.get_pot_energ() for x in moons)}")


def main(printer=print):
    global custom_printer
    custom_printer = printer
    simulate([Moon(x) for x in INPUT], 1000)
    custom_printer(f"After {simulate([Moon(x) for x in INPUT])} steps history only repeats")
