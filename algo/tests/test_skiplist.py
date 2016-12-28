import random

from algo.skiplist import SkipList, SLNode
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


def test_skiplist_to_svg():
    sl = SkipList()
    check_repr_svg(sl)

    for _ in range(99):
        sl.insert(random.random())
    check_repr_svg(sl)
