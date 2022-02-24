#!/usr/bin/env python3

# [The 5 Sampling Algorithms every Data Scientist need to know]
#   (https://towardsdatascience.com/the-5-sampling-algorithms-every-data-scientist-need-to-know-43c7bc11d17c)

import click
import random
import sys

from itertools import islice
from more_itertools import with_iter
from operator import itemgetter
from pathlib import Path
from typing import (
        Any,
        Iterable,
        List,
        Tuple,
        )



def reservoir_sampling(iterable: Iterable[Any], sample_size: int) -> List[str]:
    """
    sample_size:int Size of the reservoir
    """
    reservoir = []
    for i, line in enumerate(iterable, start=1):
        if i <= sample_size:
            reservoir.append((i, line))
        else:
            k = random.randint(0, i)
            if k < sample_size:
                reservoir[k] = (i, line)

    return reservoir



def reservoir_sampling_optimal(iterable: Iterable[Any], sample_size: int) -> List[str]:
    """
    sample_size:int Size of the reservoir
    [An optimal algorithm](https://en.wikipedia.org/wiki/Reservoir_sampling)
    """
    from math import (
            exp,
            floor,
            log,
            )
    items = iter(iterable)

    reservoir = list(islice(enumerate(items, start=1), sample_size))

    W = exp(log(random.random()) / sample_size)
    next_item_index = sample_size + floor(log(random.random()) / log(1-W)) + 1

    for i, line in enumerate(items, start=sample_size):
        if i == next_item_index:
            k = random.randint(0, sample_size-1)
            reservoir[k] = (i+1, line)
            W = W * exp(log(random.random())/sample_size)
            next_item_index += floor(log(random.random()) / log(1-W)) + 1

    return reservoir



def a_exp_j(iterable: Iterable[Tuple[float, Any]], sample_size: int) -> List[str]:
    """
    [Algorithm A-ExpJ](https://en.wikipedia.org/wiki/Reservoir_sampling)
    """
    from heapq import (
            heapify,
            heappop,
            heappush,
            )
    from math import log

    items = iter(iterable)
    h = [
            (random.random() ** (1. / w), i, v)
            for i, (w, v) in enumerate(islice(items, sample_size), start=1)
            ]
    heapify(h)

    if len(h) > 0:
        X = log(random.random()) / log(h[0][0])

        for i, (w, v) in enumerate(items, start=sample_size):
            X -= w
            if X <= 0.:
                t = h[0][0] ** w
                r = random.uniform(t, 1) ** (1. / w)

                heappop(h)
                heappush(h, (r, i+1, v))

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
        'show_line_number',
        default=False,
        show_default=True,
        help="Prepend with line number")
@click.option(
        "-w",
        "--weight",
        "show_weights",
        is_flag=True,
        show_default=True,
        default=False,
        type=bool,
        help="Show weights when doing weighted sampling.")
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
        show_line_number: bool,
        show_weights: bool,
        seed: int,
        ):
    """
    Sample stdin with reservoir sampling technique.
    """
    random.seed(seed)

    if len(samples) < 2:
        print("Unweighted Sampling", file=sys.stderr)
        if len(samples) == 0:
            sample_stream = sys.stdin
        else:
            sample_stream = with_iter(samples[0].open(mode="r", encoding="UTF-8"))
        sample_stream = map(str.strip, sample_stream)
        samples = reservoir_sampling_optimal(sample_stream, sample_size)
    elif len(samples) == 2:
        print("Weighted Sampling", file=sys.stderr)
        samples_fn, weights_fn = samples
        with samples_fn.open(mode="r", encoding="UTF-8") as sample_stream, weights_fn.open(mode="r", encoding="UTF-8") as weight_stream:
            sample_stream = map(str.strip, sample_stream)
            weight_stream = map(str.strip, weight_stream)
            weight_stream = map(float, weight_stream)
            samples = a_exp_j(zip(weight_stream, sample_stream), sample_size)
        if show_weights:
            samples = map(lambda e: (e[1], f"{e[0]}\t{e[-1]}"), samples)
        else:
            samples = map(lambda e: (e[1], e[-1]), samples)
    else:
        assert False, f"Invalid number of files ({len(samples)})"

    if show_line_number:
        samples = map(lambda e: f"{e[0]}\t{e[-1]}", samples)
    else:
        samples = map(itemgetter(1), samples)
    print(*samples, sep='\n')






if __name__ == '__main__':
    main()
