from functools import partial

from algo.tests.utils import get_func_name, gen_case, gen_special_case, print_matrix, timed_test
from algo.select import *


def test_nth_small():
    for func in (nth_small_mm, nth_small):
        with timed_test(get_func_name(func)):
            for seq in gen_case(7):
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


def test_nth_small_perf():
    matrix = []
    funcs = (
        dict(func=nth_small_mm),
        dict(func=partial(nth_small_mm, group=7), name='nth_small_mm+g7'),
        dict(func=partial(nth_small_mm, group=27), name='nth_small_mm+g27'),
        dict(func=nth_small),
        dict(func=nth_small_tail),
    )
    cases = gen_special_case(2000)

    for test_func in funcs:
        func = test_func['func']
        func_name = test_func.get('name', get_func_name(func))

        matrix.append([func_name, []])
        print('BEGIN', func_name)

        for case, arr in cases.items():
            desc = '{func_name}(_{case}_)'.format_map(locals())
            with timed_test(desc, 'performance') as get_duration:
                func(arr.copy(), len(arr) // 2)
            matrix[-1][1].append((case, get_duration()))

        print('END', func_name)
        print()

    print_matrix(matrix)


if __name__ == '__main__':
    test_nth_small()
    test_nth_small_perf()
