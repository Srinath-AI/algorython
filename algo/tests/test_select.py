from time import perf_counter
from functools import partial

from algo.tests.utils import get_func_name, gen_case, gen_special_case, print_matrix
from algo.select import *


def test_nth_small():
    for func in (nth_small_mm, nth_small):
        func_name = get_func_name(func)
        t1 = perf_counter()
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

        duration = perf_counter() - t1
        print(func_name, 'passed test in', duration, 's')

    for large_func in (nth_large, nth_large_mm):
        assert large_func(list(range(100)), 5) == 95
        print(get_func_name(large_func), 'passed test')


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
            t1 = perf_counter()
            func(arr.copy(), len(arr) // 2)
            duration = perf_counter() - t1
            matrix[-1][1].append((case, duration))

            print('{func_name}(*{case}*) pass performance test in {duration} s.'.format_map(locals()))

        print('END', func_name)
        print()

    print_matrix(matrix)


if __name__ == '__main__':
    test_nth_small()
    test_nth_small_perf()
