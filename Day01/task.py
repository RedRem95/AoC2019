import math

from Day01 import INPUT


def default_rule(x: float) -> float:
    return math.floor(int(x) / 3) - 2


def real_fuel(mod_mass: float, rule=default_rule):
    ret_sum = rule(mod_mass)
    req_fuel = rule(ret_sum)
    while req_fuel > 0:
        ret_sum += req_fuel
        req_fuel = rule(req_fuel)
    return ret_sum


def main(rule=default_rule):
    raw = [int(x) for x in INPUT]
    res = sum([rule(x) for x in raw])
    print("Module Fuel:", res)
    res = sum([real_fuel(x, rule) for x in raw])
    print(" Fuel  Fuel:", res)
