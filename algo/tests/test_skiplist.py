import random
import math
import statistics
from collections import defaultdict

from algo.skiplist import SkipList, SLNode, sl_height
from algo.container.treeset import MultiTreeSet
from algo.tests.utils import timed_test, check_repr_svg, gen_special_sort_case


def sl_verify(sl: SkipList):
    project = []

    def run(node: SLNode):
        if node.tower[0] is not None:
            run(node.tower[0])

        # check current node
        for i, next_node in enumerate(node.tower):
            if i < len(project):
                assert next_node is project[i]
            else:
                assert next_node is None

        project[:len(node.tower)] = [node] * len(node.tower)

    run(sl.head)
    # check sl.head too tall
    assert all(next_node is not None for next_node in sl.head.tower[1:])


def test_sl_height_distribution():
    p = 0.25
    d = defaultdict(int)
    for _ in range(1000000):
        d[sl_height(p)] += 1

    threshold = max(d.keys()) // 2
    norm = [ math.log(d[x], 1 / p) + x for x in range(1, threshold) ]
    assert statistics.stdev(norm) < 0.01


def test_skiplist_insert():
    size = 900
    cases = [ (name, case) for name, case in gen_special_sort_case(size).items()
              if name in {'ascending', 'descending', 'dup', 'rand_dup20'} ]

    for name, case in cases:
        with timed_test('SkipList::insert(), {name}'.format_map(locals())):
            sl = SkipList()
            for i, x in enumerate(case):
                sl.insert(x)
                sl_verify(sl)
                assert list(sl.data_iter()) == sorted(case[:(i + 1)])


def test_skiplist_remove_find():
    rand_case = gen_special_sort_case(900)['rand_dup20']

    sorted_case = sorted(rand_case)
    shuffled_case = rand_case.copy()
    random.shuffle(shuffled_case)

    remove_orders = dict(
        ascending=sorted_case,
        descending=list(reversed(sorted_case)),
        origin=rand_case,
        random=shuffled_case
    )

    for name, case in remove_orders.items():
        all_nums = MultiTreeSet(rand_case)
        sl = SkipList()
        for x in rand_case:
            sl.insert(x)
        sl_verify(sl)

        with timed_test('SkipList::remove() & SkipList::find(), {name}'.format_map(locals())):
            for x in case:
                # test find()
                found = sl.find(x)
                assert found.data == x

                removed = sl.remove(x)
                assert removed.data == x
                sl_verify(sl)

                all_nums.remove(x)
                assert list(sl.data_iter()) == list(all_nums)


def test_skiplist_to_svg():
    sl = SkipList()
    check_repr_svg(sl)

    for _ in range(99):
        sl.insert(random.random())
    check_repr_svg(sl)
