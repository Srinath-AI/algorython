from functools import partial
from itertools import groupby, chain

from algo.sort import *
from algo.tests.utils import gen_case, gen_special_case, get_func_name, print_matrix, timed_test


all_sort_funcs = (
    (qsort3, 'qsort3'),
    (partial(qsort3, part_func=qsort_part3_alt), 'qsort3+alt'),
    (partial(qsort3, part_func=qsort_part3_random), 'qsort3+rand'),
    (partial(qsort, part_func=qsort_part_head), 'qsort+head'),
    (partial(qsort, part_func=qsort_part_tail), 'qsort+tail'),
    (partial(qsort, part_func=qsort_part_hoare_like), 'qsort+hoare'),
    (partial(qsort, part_func=qsort_part_random), 'qsort+rand'),
    (heap_sort, 'heap_sort'),
    (merge_sort, 'merge_sort'),
    (bucket_sort, 'bucket_sort'),
    (list.sort, 'list.sort'),
)

stable_sort_funcs = (
    (merge_sort, 'merge_sort'),
    (bucket_sort, 'bucket_sort'),
)


def test_sort():
    def check_sorted(arr, func=qsort, **kwargs):
        copy = arr.copy()
        try:
            func(copy, **kwargs)
        except Exception:
            print('exception', copy)
            raise

        std_kwargs = {
            x: kwargs[x] for x in ('reverse', 'key') if x in kwargs
        }

        # this is the fastest way to check wether arr is sorted
        ans = sorted(copy, **std_kwargs)
        assert copy == ans, 'sort({arr}) -> {copy}'.format_map(vars())

    def perm_test(func, desc, maxlen=7):
        kwargs = getattr(func, 'keywords', {})

        with timed_test(desc, 'permutation'):
            for seq in gen_case(maxlen):
                check_sorted(seq, func=func, **kwargs)

    for sorter, description in all_sort_funcs:
        perm_test(sorter, description)
        # test ReversedKey and reversed sort
        check_sorted(list(range(100)), func=sorter, reverse=True)
        check_sorted(list(range(100, 0, -1)), func=sorter, reverse=True)


def test_stable_sort():
    def check_stable(indexed):
        for k, g in groupby(indexed, key=lambda x: x[1]):   # group by key
            indexes = list(x[0] for x in g)
            assert sorted(indexes) == indexes

    for func, desc in stable_sort_funcs:
        def gen_spec_case(size):
            spec_cases = gen_special_case(size)
            for case in ('rand', 'dup', 'dup99'):
                yield spec_cases[case]

        with timed_test(desc, 'stable sort'):
            for arr in chain(gen_case(7), gen_spec_case(5000)):
                indexed = list(enumerate(arr))      # index, key
                func(indexed, key=lambda x: x[1])   # sort by key
                check_stable(indexed)


def test_sort_perf():
    matrix = []
    cases = gen_special_case(2000)

    for func, desc in all_sort_funcs:
        matrix.append([desc, []])
        print('BEGIN {}'.format(desc))

        for case, arr in cases.items():
            func_name = get_func_name(func)
            kwargs = getattr(func, 'keywords', {})

            try:
                with timed_test('{desc}(_{case}_)'.format_map(locals()), 'performance') as get_duration:
                    func(arr.copy())
            except:
                print(desc, arr)
                raise
            else:
                matrix[-1][1].append((case, get_duration()))

        print('END {}'.format(desc))
        print()

    print_matrix(matrix)


if __name__ == '__main__':
    # import sys
    # sys.setrecursionlimit(5000)

    test_sort()
    test_stable_sort()
    test_sort_perf()
