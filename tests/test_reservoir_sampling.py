from operator import itemgetter
from reservoir_sampling.reservoir_sampling import (
        a_exp_j,
        reservoir_sampling_optimal,
        )



class TestReservoirSamplingOptimal:
    """
    Unweighted Sampling Unittests.
    """
    def test_empty(self):
        """
        """
        samples = reservoir_sampling_optimal((), 7)
        assert len(samples) == 0

    def test_short(self):
        """
        """
        samples = reservoir_sampling_optimal(range(5), 7)
        assert len(samples) == 5
        samples = map(itemgetter(-1), samples)
        assert all(a == b for a, b in zip(samples, range(5)))

    def test_long(self):
        """
        """
        samples = reservoir_sampling_optimal(range(100), 7)
        assert len(samples) == 7
        assert all(0 <= v < 100 for v in map(itemgetter(1), samples))



class TestAExpJ:
    """
    Weighted Sampling Unittests.
    """
    def test_empty(self):
        """
        """
        samples = a_exp_j(zip((), ()), 7)
        assert len(samples) == 0

    def test_short(self):
        """
        """
        weight_stream = map(lambda v: 1./(v+1.), range(5))
        sample_stream = range(5)
        samples = a_exp_j(zip(weight_stream, sample_stream), 7)
        assert len(samples) == 5
        samples = map(itemgetter(-1), samples)
        #samples = list(samples)
        #assert samples == list(range(5))
        #assert all(a == b for a, b in zip(samples, range(5)))
        assert set(samples) == set(range(5))

    def test_long(self):
        """
        """
        weight_stream = map(lambda v: 1./(v+1.), range(100))
        sample_stream = range(100)
        samples = a_exp_j(zip(weight_stream, sample_stream), 7)
        assert len(samples) == 7
        assert all(0 <= v < 100 for v in map(itemgetter(1), samples))
