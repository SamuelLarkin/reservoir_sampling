#!/usr/bin/env python3

import click

from .unweighted import cli as cli_unweighted
from .weighted import cli as cli_weighted


@click.group()
@click.help_option("-h", "--help")
def cli():
    """
    Weighted or unweighted reservoir sampling.

    https://en.wikipedia.org/wiki/Reservoir_sampling
    """
    pass


cli.add_command(cli_unweighted)
cli.add_command(cli_weighted)





if __name__ == '__main__':
    cli()
