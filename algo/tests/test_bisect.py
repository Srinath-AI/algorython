from algo.tests.utils import asc_seq, timeit
from algo.bisect import *


@timeit('bisect_find()')
def test_bisect():
    for seq in asc_seq(15):
        copy = seq.copy()
        for num in sorted(set(seq)):
            index = bisect_find(copy, num)
            assert index is not None and copy[index] == num, \
                'bisect_find({copy}, {num}) -> {index}'.format_map(vars())

        not_exists = [ (x + 0.5) for x in range(-1, max(seq) + 1) ] if seq else [0]
        for x in not_exists:
            assert bisect_find(copy, x) is None
