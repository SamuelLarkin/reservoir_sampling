#!/usr/bin/env python3

import click
import random

from reservoir_sampling import l
from typing import (
        TextIO,
        )



@click.command("unweighted")
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
def cli(
        population: TextIO,
        sample_size: int,
        show_line_number: bool,
        seed: int,
        ):
    """
    Unweighted reservoir sampling.
    """
    if seed is not None:
        random.seed(seed)

    population = map(str.strip, population)
    if show_line_number:
        population = enumerate(population, start=1)

    samples = l(population, sample_size)

    if show_line_number:
        samples = map(lambda e: f"{e[0]}\t{e[-1]}", samples)

    print(*samples, sep='\n')





if __name__ == "__main__":
    cli()
