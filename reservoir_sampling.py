#!/usr/bin/env python3

# [The 5 Sampling Algorithms every Data Scientist need to know]
#   (https://towardsdatascience.com/the-5-sampling-algorithms-every-data-scientist-need-to-know-43c7bc11d17c)

import click
import random
import sys

from math import log
from pathlib import Path
from typing import (
        Iterable,
        List,
        )



def reservoir_sampling(iterable: Iterable[str], sample_size: int) -> List[str]:
    """
    sample_size:int Size of the reservoir
    """
    reservoir = []
    for i, line in enumerate(iterable, 1):
        if i <= sample_size:
            reservoir.append((i, line.strip()))
        else:
            k = random.randint(0, i)
            if k < sample_size:
                reservoir[k] = (i, line.strip())

    return reservoir



def reservoir_sampling_optimal(iterable: Iterable[str], sample_size: int) -> List[str]:
    """
    sample_size:int Size of the reservoir
    [An optimal algorithm](https://en.wikipedia.org/wiki/Reservoir_sampling)
    """
    from math import (
            exp,
            floor,
            log,
            )
    reservoir = []
    W = exp(log(random.random()) / sample_size)
    next_item_index = sample_size + floor(log(random.random())/log(1-W)) + 1

    for i, line in enumerate(iterable, 1):
        if i <= sample_size:
            reservoir.append((i, line.strip()))
        elif i == next_item_index:
            k = random.randint(0, sample_size-1)
            reservoir[k] = (i, line.strip())
            W = W * exp(log(random.random())/sample_size)
            next_item_index += floor(log(random.random())/log(1-W)) + 1

    return reservoir



def a_exp_j(iterable: Iterable[str], sample_size: int) -> List[str]:
    """
    [Algorithm A-ExpJ](https://en.wikipedia.org/wiki/Reservoir_sampling)
    """
    import heapq
    iterable = iter(iterable)
    h = []
    for i, (w, v) in enumerate(iterable, 1):
        r = random.random() ** (1. / w)
        heapq.heappush(h, (r, v))
        if i == sample_size:
            break

    X = log(random.random()) / log(h[0][0])

    for w, v in iterable:
        X -= w
        if X <= 0.:
            t = h[0][0] ** w
            r = random.uniform(t, 1) ** (1. / w)

            heapq.heappop(h)
            heapq.heappush(h, (r, v))

            X = log(random.random()) / log(h[0][0])

    return h



@click.command()
@click.option(
        '--seed',
        'seed',
        type=int,
        default=2021,
        show_default=True,
        help="Seed the random number generator to get reproductible results")
@click.option(
        '-n',
        '--line-number/--no-line-number',
        'line_number',
        default=False,
        help="Prepend with line number")
@click.option(
        '-s',
        '--size',
        "sample_size",
        type=int,
        default=100,
        show_default=True,
        help="Sample size")
@click.argument(
        "samples",
        nargs=-1,
        type=Path,
        )
def main(
        samples: List[Path],
        sample_size: int,
        line_number: bool,
        seed: int,
        ):
    """
    Sample stdin with reservoir sampling technique.
    """
    random.seed(seed)
    if len(samples) == 0:
        samples = (sys.stdin,)

    if len(samples) == 1:
        samples = reservoir_sampling_optimal(sys.stdin, sample_size)
        if line_number:
            samples = map(lambda x: '%d\t%s'%x, samples)
        else:
            samples = map(lambda x: x[1], samples)
    elif len(samples) == 2:
        samples_fn, weights_fn = samples
        with samples_fn.open(mode="r", encoding="UTF-8") as samples, weights_fn.open(mode="r", encoding="UTF-8") as weights:
            samples = map(str.strip, samples)
            weights = map(str.strip, weights)
            weights = map(float, weights)
            samples = a_exp_j(zip(weights, samples), sample_size)
    else:
        assert f"Invalid number of files ({len(samples)})"

    print(*samples, sep='\n')






if __name__ == '__main__':
    main()
