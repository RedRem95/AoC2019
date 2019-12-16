from typing import Iterable, List, Tuple, Dict

from Day12 import INPUT
from helper import kgv

custom_printer = print


class Moon:

    def __init__(self, content, name=""):
        splitted = str(content).split(",")
        self.__x = int(splitted[0].split("=")[1])
        self.__y = int(splitted[1].split("=")[1])
        self.__z = int(splitted[2].split("=")[1].rstrip(">"))

        self.__vx = 0
        self.__vy = 0
        self.__vz = 0

        self.__name = name

        self.__my_way = []

    def get_pos(self):
        return self.get_x(), self.get_y(), self.get_z()

    def get_velo(self):
        return self.get_vx(), self.get_vy(), self.get_vz()

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
        return f"{f'{self.__name}: ' if len(self.__name) > 0 else ''}pos=<x={self.get_x()}, y={self.get_y()}, z={self.get_z()}>, vel=<x={self.get_vx()}, y={self.get_vy()}, z={self.get_vz()}>"

    def get_name(self):
        return self.__name

    def apply_velo(self):
        self.__my_way.append((self.get_pos(), self.get_velo()))
        self.__x += self.get_vx()
        self.__y += self.get_vy()
        self.__z += self.get_vz()

    def have_i_been_here(self):
        return self.get_pos() in self.__my_way

    def x_hist(self):
        return [(x[0][0], x[1][0]) for x in self.__my_way]

    def y_hist(self):
        return [(x[0][1], x[1][1]) for x in self.__my_way]

    def z_hist(self):
        return [(x[0][2], x[1][2]) for x in self.__my_way]

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


def __create_state(moons: List[Moon]) -> Dict[str, List[Tuple[int, int]]]:
    ret = {}
    for i, s in enumerate(["x", "y", "z"]):
        ret[s] = [(m.get_pos()[i], m.get_velo()[i]) for m in moons]
    return ret


def simulate(moons: List[Moon], steps=None):
    if steps is None:
        iteration = 0
        x_iter = -1
        y_iter = -1
        z_iter = -1
        init_state = __create_state(moons)
        while x_iter < 0 or y_iter < 0 or z_iter < 0:
            iteration += 1
            for m in moons:
                calc_velo(m, moons)
            for m in moons:
                m.apply_velo()
            comp_state = __create_state(moons)
            if x_iter < 0 and comp_state["x"] == init_state["x"]:
                x_iter = iteration
            if y_iter < 0 and comp_state["y"] == init_state["y"]:
                y_iter = iteration
            if z_iter < 0 and comp_state["z"] == init_state["z"]:
                z_iter = iteration
        return kgv(kgv(x_iter, y_iter), z_iter)

    else:
        custom_printer("After 0 steps")
        custom_printer("\n".join((str(x) for x in moons)))

        for i in range(steps):
            for m in moons:
                calc_velo(m, moons)
            for m in moons:
                m.apply_velo()
            if (i + 1) % 10 == 0 and i != steps - 1:
                custom_printer(f"After {i + 1} steps")
                custom_printer("\n".join((str(x) for x in moons)))

        custom_printer(f"After {steps} steps")
        custom_printer("\n".join((str(x) for x in moons)))
        custom_printer("Pot_energs:")
        custom_printer("\n".join(
            f"{x.get_name() if len(x.get_name()) > 0 else i}: {x.get_pot_energ()}" for i, x in enumerate(moons)))

        custom_printer(f"Sum pot energ: {sum(x.get_pot_energ() for x in moons)}")


def main(printer=print):
    global custom_printer
    custom_printer = printer
    simulate([Moon(x, name=f"Moon {i + 1}") for i, x in enumerate(INPUT)], 1000)
    custom_printer(
        f"After {int(simulate([Moon(x, name=f'Moon {i + 1}') for i, x in enumerate(INPUT)]))} steps history only repeats")
