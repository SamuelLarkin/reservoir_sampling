#!/usr/bin/env python3

import click
import random

from operator import itemgetter
from reservoir_sampling import a_exp_j
from typing import (
        TextIO,
        )



@click.command("weighted")
@click.option(
        '--seed',
        'seed',
        type=int,
        default=None,
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
        "population",
        type=click.File(mode='r', encoding="UTF-8"),
        )
@click.argument(
        "weights",
        type=click.File(mode='r', encoding="UTF-8"),
        )
def cli(
        population: TextIO,
        weights: TextIO,
        sample_size: int,
        show_line_number: bool,
        show_weights: bool,
        seed: int,
        ):
    """
    Weighted reservoir sampling.
    """
    if seed is not None:
        random.seed(seed)

    population = map(str.strip, population)
    if show_line_number:
        population = enumerate(population)

    weights = map(str.strip, weights)
    weights = map(float, weights)

    weighted_population = zip(weights, population)

    samples = a_exp_j(weighted_population, sample_size)

    if show_line_number:
        if show_weights:
            samples = map(lambda e: f"{e[1][0]}\t{e[0]}\t{e[1][1]}", samples)
        else:
            samples = map(lambda e: f"{e[1][0]}\t{e[1][1]}", samples)
    else:
        if show_weights:
            samples = map(lambda e: f"{e[0]}\t{e[1]}", samples)
        else:
            samples = map(itemgetter(1), samples)

    print(*samples, sep='\n')





if __name__ == '__main__':
    cli()
