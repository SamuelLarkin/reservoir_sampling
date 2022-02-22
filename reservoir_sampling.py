#!/usr/bin/env python3

# [The 5 Sampling Algorithms every Data Scientist need to know]
#   (https://towardsdatascience.com/the-5-sampling-algorithms-every-data-scientist-need-to-know-43c7bc11d17c)

import click
import random
import sys

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
def main(
        sample_size: int,
        line_number: bool,
        seed: int,
        ):
    """
    Sample stdin with reservoir sampling technique.
    """
    random.seed(seed)
    samples = reservoir_sampling_optimal(sys.stdin, sample_size)
    if line_number:
        samples = map(lambda x: '%d\t%s'%x, samples)
    else:
        samples = map(lambda x: x[1], samples)
    print(*samples, sep='\n')






if __name__ == '__main__':
    main()
