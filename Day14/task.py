from math import ceil
from multiprocessing import Pool
from time import time
from typing import Union, Iterable, Dict, Callable, List

import numpy as np

from Day14 import INPUT
from helper import IntWrapper
from main import custom_print as custom_printer

if False:
    INPUT = [
        "10 ORE => 10 A",
        "1 ORE => 1 B",
        "7 A, 1 B => 1 C",
        "7 A, 1 C => 1 D",
        "7 A, 1 D => 1 E",
        "7 A, 1 E => 1 FUEL"
    ]


class Reaction:
    def __init__(self, reaction: str):
        in_mat, out_mat = reaction.split("=>")[:2]
        self.__target_material = out_mat.strip().split(" ")[1].upper()
        self.__target_count = int(out_mat.strip().split(" ")[0])
        self.__origins = [(int(x.strip().split(" ")[0]), x.strip().split(" ")[1].upper()) for x in in_mat.split(",")]

    def reaction_possible(self, store: Dict[str, int]) -> bool:
        return self.reaction_can_run_times(store) > 0

    def reaction_can_run_times(self, store: Dict[str, int]) -> int:
        ret = 0
        for needed, name in self.__origins:
            if name not in store:
                return 0
            ret += int(store.get(name, 0) / needed)
        return ret

    def apply_reation(self, store: Dict[str, int], times: int = 1) -> Dict[str, int]:
        if self.reaction_can_run_times(store) < times:
            return store
        for needed, name in self.__origins:
            store[name] = store[name] - (needed * times)
        store[self.__target_material] = store.get(self.__target_material, 0) + (self.__target_count * times)
        return store

    def __str__(self):
        return f"{', '.join((f'{needed} {name}' for needed, name in self.__origins))} => {self.__target_count} {self.__target_material}"


def int_ceil_convert(value: float) -> int:
    return int(ceil(value))


class Material:
    def __init__(self, name: str):
        self.__name = name
        self.__i_create = []

    def add_reaction(self, of_me: int, create: int, material):
        self.__i_create.append((of_me, create, material))

    def get_count_of_me(self, convert: Callable[[float], float] = int_ceil_convert) -> int:
        return sum(convert(material.get_count_of_me() / create) * of_me for of_me, create, material in self.__i_create)

    def __str__(self):
        return self.__name


def create_materials(reactions: Iterable[str], *targets: Material) -> Dict[str, Material]:
    materials: Dict[str, Material] = {}
    for target in targets:
        materials[str(target)] = target
    for react in reactions:
        in_mat, out_mat = react.split("=>")[:2]
        target_mat = out_mat.strip().split(" ")[1].upper()
        if target_mat not in materials:
            target_mat = Material(out_mat.strip().split(" ")[1].upper())
            materials[target_mat.__str__()] = target_mat
        else:
            target_mat = materials[target_mat]
        target_count = int(out_mat.strip().split(" ")[0])
        for orig_count, orig_material in ((int(x.strip().split(" ")[0]), x.strip().split(" ")[1].upper()) for x in
                                          in_mat.split(",")):
            if orig_material not in materials:
                materials[orig_material] = Material(orig_material)
            materials[orig_material].add_reaction(orig_count, target_count, target_mat)
    return materials


def __apply_reaction(value) -> List[Dict[str, int]]:
    return [x for x in
            test_combinations(reactions=value["reactions"], store=value["store"], thread_count=value["thread_count"])]


def test_combinations(reactions: Iterable[Union[str, Reaction]], store: Dict[str, int],
                      thread_count: Union[int, None] = None) -> List[Dict[str, int]]:
    reactions = [x if isinstance(x, Reaction) else Reaction(x) for x in reactions]

    for poss_reaction, times in ((x, x.reaction_can_run_times(store)) for x in reactions if x.reaction_possible(store)):
        used_reactions = reactions.copy()
        used_reactions.remove(poss_reaction)

        applied_reactions = [poss_reaction.apply_reation(store.copy(), t) for t in range(times, 0, -1)]

        if isinstance(thread_count, int):
            with Pool(thread_count) as p:
                pool_res = p.map(__apply_reaction, [{"reactions": reactions, "store": x, "thread_count": None} for x in
                                                    applied_reactions])
        else:
            pool_res = [test_combinations(reactions=reactions, store=x, thread_count=None) for x in applied_reactions]

        for r in pool_res:
            for i in r:
                yield i

    yield store


def main():
    target = "FUEL"
    origin = "ORE"

    target_count = IntWrapper(1)

    class TargetMaterial(Material):
        def __init__(self, name, count):
            super().__init__(name)
            self.__count = count

        def get_count_of_me(self, **kwargs):
            return self.__count.get()

    FUEL = TargetMaterial(target, target_count)

    MATERIALS = create_materials(INPUT, FUEL)

    origin_count = MATERIALS[origin].get_count_of_me()
    custom_printer("A1")
    custom_printer(f"To create {target_count.get()} {target} you need {origin_count} {origin}")
    custom_printer("\nA2")

    found_origin = 1000000000000
    curr_max = 0

    target_count.set(curr_max + 1)

    times = []
    max_p_string = 1

    while MATERIALS[origin].get_count_of_me() < found_origin:
        start_time = time()
        curr_max = target_count.get()
        if target_count.get() % max(1, int(found_origin / 10000000)) == 0:
            now_time = np.average(times if len(times) > 0 else [0])
            if now_time != 0:
                now_time = 1 / now_time
            needed_mats = MATERIALS[origin].get_count_of_me()
            p_str = f"\r{curr_max:13.0f} still ok. It needs {needed_mats:13.0f}/{found_origin} {origin} ({(needed_mats / found_origin) * 100:6.2f}%) {now_time:.2f}ops"
            max_p_string = max(max_p_string, len(p_str))
            custom_printer(("{p_str:%s}" % max_p_string).format(p_str=p_str), new_line=False)
        target_count.increase()
        end_time = time()
        times.append(end_time - start_time)

    target_count.set(curr_max)

    needed_mats = MATERIALS[origin].get_count_of_me()

    p_str = f"\rWith {found_origin} you can create {curr_max} {target}. You will use {needed_mats}/{found_origin} {origin} ({(needed_mats / found_origin) * 100:6.2f}%)"
    custom_printer(("{p_str:%s}" % max_p_string).format(p_str=p_str))
