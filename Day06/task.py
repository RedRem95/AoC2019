from Day06 import INPUT

custom_print = print

class SpaceObject:
    __space_objects = {}

    def __init__(self, name, *orbits):
        self.__name = str(name)
        self.__orbits = [x for x in orbits]
        self.__moons = []
        for x in self.__orbits:
            x.add_moons(self)

        SpaceObject.__space_objects[name] = self

    def add_orbit(self, *names):
        self.__orbits.extend(names)
        for x in [SpaceObject.get_space_object(name) for name in names]:
            x.add_moons(self)

    def set_orbit(self, *names):
        self.__orbits = []
        self.add_orbit(*names)

    def __get_orbit_space_object(self):
        return [x for x in self.__orbits if x is not None and isinstance(x, SpaceObject)]

    def get_direct_orbits(self):
        return self.__get_orbit_space_object()

    def get_moons(self):
        return [x for x in self.__moons if x is not None and isinstance(x, SpaceObject)]

    def add_moons(self, *moon):
        self.__moons.extend([x for x in moon])

    def set_moons(self, *moon):
        self.__moons = []
        self.add_moons(*moon)

    def get_indrect_orbits(self):
        objects = []
        for obj in self.__get_orbit_space_object():
            objects.extend(obj.get_direct_orbits())
            objects.extend(obj.get_indrect_orbits())
        return objects

    def get_all_orbits(self):
        ret = self.get_direct_orbits().copy()
        ret.extend(self.get_indrect_orbits())
        return ret

    def get_indirect_moons(self):
        objects = []
        for obj in self.get_moons():
            objects.extend(obj.get_moons())
            objects.extend(obj.get_indirect_moons())
        return objects

    def get_all_moons(self):
        ret = self.get_moons().copy()
        ret.extend(self.get_indirect_moons())
        return ret

    def find_ways(self, target, traveled=[], ways=[], only_first=True):
        if self in traveled:
            return []
        traveled.append(self)
        if SpaceObject.get_space_object(target) == self:
            ways.append(traveled.copy())
            return ways

        for x in self.get_moons() + self.get_direct_orbits():
            way_len_prev = len(ways)
            SpaceObject.get_space_object(x).find_ways(target, traveled=traveled.copy(), ways=ways)
            if way_len_prev < len(ways) and only_first:
                return ways

        return ways

    @staticmethod
    def get_space_object(name):
        if isinstance(name, SpaceObject):
            return name
        if name not in SpaceObject.__space_objects:
            SpaceObject(name)
        return SpaceObject.__space_objects[name]

    @staticmethod
    def get_all_space_objects():
        return [x for x in SpaceObject.__space_objects.values()]

    def __str__(self):
        return self.__name


SpaceObject("COM")


def parse():
    for planet, moon in [x.split(")") for x in INPUT]:
        SpaceObject.get_space_object(moon).set_orbit(SpaceObject.get_space_object(planet))


def main(printer=print):
    global custom_print
    custom_print = printer
    parse()
    custom_print("\tA1:")
    custom_print("\t\tAll the space objects:",
                 sum((len(x.get_all_orbits()) for x in SpaceObject.get_all_space_objects())))

    all_the_ways = sorted(
        [x for x in SpaceObject.get_space_object("YOU").find_ways(SpaceObject.get_space_object("SAN"))],
        key=lambda x: len(x))
    shortest_way = all_the_ways[0]
    count_transfers = max(0, len(shortest_way) - 3)
    custom_print("\tA2:")
    custom_print("\t\tNeeded transfers:", count_transfers)
    custom_print("\t\t    Shortest way:",
                 "->".join((str(x) for x in shortest_way[1:-1])) if count_transfers > 0 else "<You are already there>")
