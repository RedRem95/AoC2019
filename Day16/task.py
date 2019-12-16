from time import time
from typing import List

import numpy as np

from Day16 import INPUT
from helper import kgv
from main import AUTOMATIC
from main import custom_print as custom_printer

INPUT = [int(y) for y in "03036732577212944063491565474664"]


def phase_shift(phase: List[int], base_pattern: List[int], phases: int, numpy_version: bool = True,
                phase_repetition: int = 1) -> List[int]:
    phase_repetition = abs(phase_repetition)
    if phase_repetition <= 0:
        raise SystemError("You cant repeat something 0 times and expect a result. Duhh")
    custom_printer("Creating iterator")
    if numpy_version:
        custom_printer("Creating numpy array")
        phase = np.array(phase)

    times = []

    needed_phase_len = min(max(kgv(len(phase), len(base_pattern)), len(phase) * len(base_pattern)),
                           len(phase) * phase_repetition)

    custom_printer(
        f"Will create the phase after {phases} shifts with an input of length {len(phase)} repeated {phase_repetition} times and {base_pattern} as the multiplication pattern")

    phase_tmp = phase.copy()

    init_phase_len = len(phase)

    while len(phase) < needed_phase_len:
        phase = np.hstack((phase, phase_tmp))

    del phase_tmp

    for i in range(phases):
        now_time = np.average(times if len(times) > 0 else [0])
        if now_time != 0:
            now_time = 1 / now_time
        custom_printer(
            f"\rCalculating phases at {now_time:.2f}pps {((i + 1) / phases) * 100:6.2f}% ({i + 1}/{phases}) remaining {round((phases - (i + 1)) / now_time, ndigits=2) if now_time > 0 else '<inf>'}s",
            new_line=False)

        start_time = time()
        if numpy_version:
            new_phase = []
            for k in range(len(phase)):
                pattern = np.vectorize(lambda x: base_pattern[int((x + 1) / (k + 1)) % len(base_pattern)])(
                    np.arange(len(phase)))
                new_phase.append(int(str(np.sum(np.multiply(phase, pattern)))[-1]))
        else:
            new_phase = [int(str(
                sum(phase[j] * base_pattern[int((j + 1) / (k + 1)) % len(base_pattern)] for j in range(len(phase))))[
                                 -1]) for k in range(len(phase))]
        end_time = time()
        times.append((end_time - start_time))
        phase = new_phase
    custom_printer(
        f"\rCalculated {phases} with an input of length {len(phase)} repeated {phase_repetition} times in {sum(times):.2f}s. On average a step took {np.average(times):.2f}s")

    phase_tmp = phase.copy()

    while len(phase) < init_phase_len * phase_repetition:
        phase = np.hstack((phase, phase_tmp))

    return phase


def main(printer=print):
    count_shifts = 100
    shifted_phase = phase_shift(INPUT, [0, 1, 0, -1], count_shifts, numpy_version=False, phase_repetition=1)
    custom_printer("A1")
    count_digits = 8
    custom_printer(
        f"First {count_digits} digits of new shift are {''.join((str(x) for x in shifted_phase[:count_digits]))}")
    if not AUTOMATIC:
        custom_printer("\nA2")
        shifted_phase = phase_shift(INPUT, [0, 1, 0, -1], count_shifts, numpy_version=True, phase_repetition=10000)
        offset = int("".join((str(x) for x in INPUT[:7])))
        custom_printer(
            f"First {count_digits} digits of new shift are {''.join((str(x) for x in shifted_phase[offset:offset + count_digits]))}")
