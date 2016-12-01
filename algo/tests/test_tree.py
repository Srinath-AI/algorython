from algo.tests.utils import get_func_name, timed_test, gen_bst
from algo.tree.basetree import *
from algo.tree.bstree import *


def test_middle_iter():
    for iterator in (middle_iter, middle_iter_bystack, middle_iter_sm):
        with timed_test(get_func_name(iterator)):
            for root in gen_bst(4):
                count = BSTree(root).count()
                expanded = list(iterator(root))
                expanded_sorted = sorted(expanded, key=lambda n: n.data)
                assert len(expanded) == count \
                    and expanded_sorted == expanded == list(middle_iter(root)), \
                    ('{expanded}'.format_map(vars()), print_tree(BSTree(root)))
