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



Sample = Any
Weight = float
WeightedSample = Tuple[float, Any]
UnweightedSamples = List[Sample]
WeightedSamples = List[WeightedSample]



def r(iterable: Iterable[Any], sample_size: int) -> UnweightedSamples:
    """
    sample_size:int Size of the reservoir
    """
    if sample_size <= 0:
        return []

    reservoir = []
    for i, item in enumerate(iterable, start=1):
        if i <= sample_size:
            reservoir.append(item)
        else:
            k = random.randint(0, i)
            if k < sample_size:
                reservoir[k] = item

    return reservoir



def l(iterable: Iterable[Any], sample_size: int) -> UnweightedSamples:
    """
    sample_size:int Size of the reservoir
    [An optimal algorithm](https://en.wikipedia.org/wiki/Reservoir_sampling)
    iterable:
    """
    from math import (
            exp,
            floor,
            log,
            )
    if sample_size <= 0:
        return []

    items = iter(iterable)

    reservoir = list(islice(items, sample_size))

    W = exp(log(random.random()) / sample_size)
    next_item_index = sample_size + floor(log(random.random()) / log(1-W)) + 1

    for i, item in enumerate(items, start=sample_size):
        if i == next_item_index:
            k = random.randint(0, sample_size-1)
            reservoir[k] = item
            W = W * exp(log(random.random())/sample_size)
            next_item_index += floor(log(random.random()) / log(1-W)) + 1

    return reservoir



def a_exp_j(iterable: Iterable[WeightedSample], sample_size: int) -> WeightedSamples:
    """
    [Algorithm A-ExpJ](https://en.wikipedia.org/wiki/Reservoir_sampling)
    iterable: Yields a tuple of weight and item.
    """
    from heapq import (
            heapify,
            heappop,
            heappush,
            )
    from math import log

    if sample_size <= 0:
        return []

    items = iter(iterable)
    h = [
            (random.random() ** (1. / weight), value)
            for weight, value in islice(items, sample_size)
            ]
    heapify(h)

    if len(h) > 0:
        X = log(random.random()) / log(h[0][0])

        for weight, value in items:
            X -= weight
            if X <= 0.:
                t = h[0][0] ** weight
                r = random.uniform(t, 1) ** (1. / weight)

                heappop(h)
                heappush(h, (r, value))

                X = log(random.random()) / log(h[0][0])

    #return [heappop(h) for i in range(len(h))]
    return h
