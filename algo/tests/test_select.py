from functools import partial
from itertools import chain

from algo.tests.utils import gen_sort_case, gen_special_sort_case, get_func_name, timed_test
from algo.select import *


all_select_funcs = (
    dict(func=nth_small_mm),
    dict(func=partial(nth_small_mm, group=7), name='nth_small_mm+g7'),
    dict(func=partial(nth_small_mm, group=27), name='nth_small_mm+g27'),
    dict(func=nth_small, is_random=True),
    dict(func=nth_small_tail, skip_large=True),
)


def test_nth_small():
    for entry in all_select_funcs:
        func = entry['func']
        desc = entry.get('name', get_func_name(func))
        if entry.get('skip_large', False):
            print(desc, 'skipping large testcase.')
            case_size = 500
        else:
            case_size = 5000

        with timed_test(desc):
            for seq in chain(gen_sort_case(7), gen_special_sort_case(case_size).values()):
                copy = seq.copy()
                if len(copy) == 0:
                    continue

                sorted_input = sorted(copy)

                if len(copy) > 20:
                    ranger = range(0, len(copy), len(copy) // 10)
                else:
                    ranger = range(len(copy))

                for i in ranger:
                    n = i + 1
                    selected = func(copy.copy(), n)
                    assert selected == sorted_input[i], \
                        '{desc}({copy}, {n}) -> {selected}'.format_map(vars())

    for large_func in (nth_large, nth_large_mm):
        with timed_test(get_func_name(large_func)):
            assert large_func(list(range(100)), 5) == 95
