from functools import partial
from itertools import groupby, chain

from algo.sort import *
from algo.tree import RBTree, AVLTree, Treap, BSTree
from algo.tests.utils import (
    gen_sort_case, gen_special_sort_case,
    get_func_name, print_matrix, timed_test
)


sort_funcs = (
    dict(func=qsort3),
    dict(func=partial(qsort3, part_func=qsort_part3_alt), name='qsort3+alt'),
    dict(func=partial(qsort3, part_func=qsort_part3_random), name='qsort3+rand'),
    dict(func=partial(qsort, part_func=qsort_part_head), name='qsort+head'),
    dict(func=partial(qsort, part_func=qsort_part_tail), name='qsort+tail'),
    dict(func=partial(qsort, part_func=qsort_part_hoare_like), name='qsort+hoare'),
    dict(func=partial(qsort, part_func=qsort_part_random), name='qsort+rand'),
    dict(func=heap_sort),
    dict(func=merge_sort, stable=True),
    dict(func=bucket_sort, stable=True),
    dict(func=partial(tree_sort, tree_type=RBTree), name='tree_sort+rbtree', stable=True),
    dict(func=partial(tree_sort, tree_type=AVLTree), name='tree_sort+avltree', stable=True),
    dict(func=partial(tree_sort, tree_type=Treap), name='tree_sort+treap', stable=True),
    dict(func=partial(tree_sort, tree_type=BSTree), name='tree_sort+bstree', stable=True, skip_large=True),
    dict(func=list.sort, name='list.sort', stable=True),
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
            for seq in gen_sort_case(maxlen):
                check_sorted(seq, func=func, **kwargs)

    for entry in sort_funcs:
        sorter = entry['func']
        desc = entry.get('name', get_func_name(sorter))

        perm_test(sorter, desc)
        # test ReversedKey and reversed sort
        check_sorted(list(range(100)), func=sorter, reverse=True)
        check_sorted(list(range(100, 0, -1)), func=sorter, reverse=True)


def test_stable_sort():
    def check_stable(indexed):
        for k, g in groupby(indexed, key=lambda x: x[1]):   # group by key
            indexes = list(x[0] for x in g)
            assert sorted(indexes) == indexes

    # for func, desc in stable_sort_funcs:
    for entry in sort_funcs:
        if not entry.get('stable', False):
            continue
        func = entry['func']
        desc = entry.get('name', get_func_name(func))

        def gen_spec_case(size):
            spec_cases = gen_special_sort_case(size)
            for case in ('rand', 'dup', 'dup99'):
                yield spec_cases[case]

        if entry.get('skip_large', False):
            print(desc, 'skipping large testcase.')
            case_size = 500
        else:
            case_size = 5000

        with timed_test(desc, 'stable sort'):
            for arr in chain(gen_sort_case(7), gen_spec_case(case_size)):
                indexed = list(enumerate(arr))      # index, key
                func(indexed, key=lambda x: x[1])   # sort by key
                check_stable(indexed)


def test_sort_perf():
    matrix = []
    cases = gen_special_sort_case(2000)

    for entry in sort_funcs:
        func = entry['func']
        desc = entry.get('name', get_func_name(func))
        if entry.get('skip_large', False):
            print(desc, 'skipping large testcase.')
            continue

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
