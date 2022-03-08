#!/usr/bin/env python3

# [The 5 Sampling Algorithms every Data Scientist need to know]
#   (https://towardsdatascience.com/the-5-sampling-algorithms-every-data-scientist-need-to-know-43c7bc11d17c)

import random

from itertools import islice
from typing import (
        Any,
        Iterable,
        List,
        Tuple,
        )



def r(iterable: Iterable[Any], sample_size: int) -> List[str]:
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



def l(iterable: Iterable[Any], sample_size: int) -> List[str]:
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
