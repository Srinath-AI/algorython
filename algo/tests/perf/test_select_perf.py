from functools import partial

from algo.select import *
from algo.tests.utils import gen_special_sort_case, get_func_name, timed_test, print_matrix


def test_nth_small_perf():
    matrix = []
    funcs = (
        dict(func=nth_small_mm),
        dict(func=partial(nth_small_mm, group=7), name='nth_small_mm+g7'),
        dict(func=partial(nth_small_mm, group=27), name='nth_small_mm+g27'),
        dict(func=nth_small),
        dict(func=nth_small_tail),
    )
    cases = gen_special_sort_case(2000)

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
