from functools import partial
from itertools import groupby
from time import perf_counter

from algo.sort import *
from algo.tests.utils import gen_case, gen_special_case, get_func_name, print_matrix


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
    # def is_sorted(arr, **kwargs):
    #     nkey = get_sort_key(**kwargs)
    #
    #     for i in range(len(arr) - 1):
    #         if nkey(arr[i + 1]) < nkey(arr[i]):
    #             return False
    #     else:
    #         return True

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
        ans = sorted(copy, **std_kwargs)

        # succ = is_sorted(copy, **kwargs)
        assert copy == ans, 'sort({arr}) -> {copy}'.format_map(vars())

    # test ReversedKey
    check_sorted([1, 2, 3, 4], reverse=True)
    # test reversed bucket_sort
    check_sorted(list(range(100)), func=bucket_sort, reverse=True)

    # check_sorted([])
    # check_sorted([3, 2, 1])
    # check_sorted([1, 2, 3, 0, 0])
    # check_sorted([1, 1, 1, 1])
    # check_sorted([1, 5, 6, 7, 8])
    # check_sorted([6, 1, 2, 3, 4, 5])
    # check_sorted([1, 2, 3, 4, 5])
    # check_sorted([5, 4, 3, 2, 1])

    def perm_test(func, maxlen=7):
        func_name = get_func_name(func)
        kwargs = getattr(func, 'keywords', {})

        t1 = perf_counter()
        for seq in gen_case(maxlen):
            check_sorted(seq, func=func, **kwargs)
        duration = perf_counter() - t1

        print('{func_name}(*, **{kwargs}) passed perm_test in {duration} s.'.format_map(locals()))

    for func, description in all_sort_funcs:
        perm_test(func)


def test_stable_sort():
    def check_stable(indexed):
        for k, g in groupby(indexed, key=lambda x: x[1]):   # group by key
            indexes = list(x[0] for x in g)
            assert sorted(indexes) == indexes

    for func, desc in stable_sort_funcs:
        t1 = perf_counter()
        for arr in gen_case(7):
            indexed = list(enumerate(arr))      # index, key
            func(indexed, key=lambda x: x[1])   # sort by key
            check_stable(indexed)
        duration = perf_counter() - t1

        print(desc, 'passed stable sort test in', duration, 's.')


def test_sort_perf():
    matrix = []
    cases = gen_special_case(2000)

    for func, description in all_sort_funcs:
        matrix.append([description, []])
        print('BEGIN {}'.format(description))

        for case, arr in cases.items():
            func_name = get_func_name(func)
            kwargs = getattr(func, 'keywords', {})

            t1 = perf_counter()
            try:
                func(arr.copy())
            except:
                print(func, arr)
                raise
            duration = perf_counter() - t1

            matrix[-1][1].append((case, duration))
            print('{func_name}(_{case}_, **{kwargs}) passed perf test in {duration} s.'
                  .format_map(locals()))

        print('END {}'.format(description))
        print()

    print_matrix(matrix)


if __name__ == '__main__':
    # import sys
    # sys.setrecursionlimit(5000)

    test_sort()
    test_stable_sort()
    test_sort_perf()
