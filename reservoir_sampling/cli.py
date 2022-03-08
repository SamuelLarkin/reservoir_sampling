#!/usr/bin/env python3
import click
import random
import sys

from more_itertools import with_iter
from operator import itemgetter
from pathlib import Path
from reservoir_sampling import (
        a_exp_j,
        l,
        )
from typing import List

#@click.group()
#@click.help_option("-h", "--help")

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
        samples = l(sample_stream, sample_size)
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
