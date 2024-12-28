import itertools
from enum import Enum
import random

import numpy as np

MIN_LEN = 3
MAX_LEN = 7
NUM_TRIALS = 21


class Group(Enum):
    ACTIVE = "A"
    CONTROL = "C"
    BLANK = "_"


def run_iter():
    group = random.choice([Group.ACTIVE, Group.CONTROL])
    while True:
        if group == Group.ACTIVE:
            group = Group.CONTROL
        else:
            group = Group.ACTIVE
        run_len = random.choice([2, 3, 6, 8])
        for _ in range(run_len):
            yield group


def gen_runs(num_trials):
    return np.array(list(itertools.islice(run_iter(), num_trials)))


def generate_schedules_ab():
    mask_4 = np.array([
        True, True, False, False,
        True, True, False, False,
        False, False, True, True,
        False, False, True, True
    ]).reshape((4, 4), order="F")
    mask_3 = np.array([
        True, True, False,
        True, True, False,
        False, False, True,
        False, False, True
    ]).reshape((3, 4), order="F")
    mask_2 = np.array([
        True, False,
        True, False,
        False, True,
        False, True
    ]).reshape((2, 4), order="F")

    mask = np.concatenate([mask_4, mask_4, mask_4, mask_4, mask_3, mask_2])

    while True:
        runs = gen_runs(28).reshape((7, 4), order="F")
        num_intervention = sum([c == Group.ACTIVE for c in runs.flatten()])
        if num_intervention >= 28 * 0.45 and (28 - num_intervention) >= 0.45:
            runs = np.concatenate([runs, runs, runs])
            break

    pi = list(range(21))
    random.shuffle(pi)
    pi = np.array(pi)

    permuted = runs[pi]

    schedule_a = permuted.copy()
    schedule_a[mask] = Group.BLANK
    schedule_b = permuted.copy()
    schedule_b[~mask] = Group.BLANK

    # invert pi
    pi_tups = [(src, dest) for (src, dest) in enumerate(pi)]
    pi_inverse = [t[0] for t in sorted(pi_tups, key=lambda t: t[1])]
    return {
        "truth": runs,
        "a": schedule_a,
        "b": schedule_b,
        "pi": pi_inverse,
    }


def pprint_grid(grid):
    grid = grid.T
    res = ""
    for row in grid:
        res += "".join([x.value for x in row])
        res += "\n"
    return res


if __name__ == "__main__":
    schedules = generate_schedules_ab()
    with open("truth.txt", "w") as f:
        f.write("Ground Truth\n\n")
        f.write(
            pprint_grid(schedules["truth"])
        )

    with open("schedule_a.txt", "w") as f:
        f.write("Schedule A\n\n")
        f.write(
            pprint_grid(schedules["a"])
        )

    with open("schedule_b.txt", "w") as f:
        f.write("Schedule B\n\n")
        f.write(
            pprint_grid(schedules["b"])
        )

    with open("schedule_c.txt", "w") as f:
        f.write("Schedule C\n\n")
        label = [f"{x + 1:2d}" for x in range(21)]
        permutation = [f"{x + 1:2d}" for x in schedules["pi"]]
        for label, permutation in zip(label, permutation):
            f.write(f"{permutation} -> {label}\n")

