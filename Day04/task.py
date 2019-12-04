from typing import List

from Day04 import INPUT
from helper import partner_check, only_increase, int_to_iter, atleast_one_pair_check


def create_passwords(min_pw=min(*INPUT), max_pw=max(*INPUT)) -> List:
    return [i for i in range(min_pw, max_pw + 1, 1) if partner_check(int_to_iter(i)) and only_increase(int_to_iter(i))]


def create_passwords_2(min_pw=min(*INPUT), max_pw=max(*INPUT)) -> List:
    return [i for i in range(min_pw, max_pw + 1, 1) if
            atleast_one_pair_check(int_to_iter(i)) and only_increase(int_to_iter(i))]


def main():
    print("Found %s passwords A1" % len(create_passwords()))
    print("Found %s passwords A2" % len(create_passwords_2()))
