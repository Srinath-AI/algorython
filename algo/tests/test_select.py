from algo.tests.utils import gen_sort_case, get_func_name, timed_test
from algo.select import *


def test_nth_small():
    for func in (nth_small_mm, nth_small, nth_small_tail):
        with timed_test(get_func_name(func)):
            for seq in gen_sort_case(7):
                copy = seq.copy()
                if len(copy) == 0:
                    continue

                sorted_input = sorted(copy)
                for i in range(len(copy)):
                    n = i + 1
                    selected = func(copy.copy(), n)
                    assert selected == sorted_input[i], \
                        '{func_name}({copy}, {n}) -> {selected}'.format_map(vars())

    for large_func in (nth_large, nth_large_mm):
        with timed_test(get_func_name(large_func)):
            assert large_func(list(range(100)), 5) == 95
