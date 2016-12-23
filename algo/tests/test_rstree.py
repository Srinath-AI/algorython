from algo.tests.utils import (
    gen_bstree_by_insert, run_bstree_insert_test, run_bstree_insert_test_large,
    run_bstree_remove_test, run_bstree_remove_test_large,
)
from algo.tree.rstree import RSNode, RSTree, is_rstree


def gen_rstree_by_insert(maxlen):
    yield from gen_bstree_by_insert(maxlen, RSTree, lambda node: None)


def test_is_rstree():
    def gen_rstree_node(tup):
        if tup is None:
            return None
        if not isinstance(tup, tuple):
            tup = (tup,)

        node = RSNode(0)
        node.size = tup[0]
        if len(tup) > 1:
            node.left = gen_rstree_node(tup[1])
        if len(tup) > 2:
            node.right = gen_rstree_node(tup[2])

        return node

    cases = [
        (True, None),
        (False, (0,)),
        (True, (1,)),
        (True, (2, 1)),
        (True, (3, 1, 1)),
        (False, (2, 1, 1)),
        (False, (3, None, 2)),
        (True, (2, None, 1)),
    ]
    for ans, tup in cases:
        tree = RSTree(gen_rstree_node(tup))
        assert is_rstree(tree) is ans


def test_rstree_insert():
    run_bstree_insert_test(7, gen_rstree_by_insert, is_rstree, 'RSTree::insert()')


def test_rstree_insert_large():
    run_bstree_insert_test_large(2000, RSTree, is_rstree, 'RSTree::insert() large case')


def test_rstree_remove():
    run_bstree_remove_test(7, gen_rstree_by_insert, is_rstree, 'RSTree::remove()')


def test_rstree_remove_large():
    run_bstree_remove_test_large(1000, RSTree, is_rstree, 'RSTree::remove() large case')
