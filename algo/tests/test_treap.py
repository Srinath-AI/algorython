from algo.tests.utils import (
    gen_bstree_by_insert, run_bstree_insert_test, run_bstree_insert_test_large,
    run_bstree_remove_test,)
from algo.tree.treap import Treap, TreapNode, is_treap


def gen_treap_by_insert(maxlen):
    yield from gen_bstree_by_insert(maxlen, Treap, lambda node: None)


def test_is_treap():
    def gen_treap_node(tup):
        if tup is None:
            return None
        if not isinstance(tup, tuple):
            tup = (tup,)

        node = TreapNode(0)
        node.priority = tup[0]
        if len(tup) > 1:
            node.left = gen_treap_node(tup[1])
        if len(tup) > 2:
            node.right = gen_treap_node(tup[2])

        return node

    cases = [
        (True, None),
        (True, (1,)),
        (True, (1, 2, 2)),
        (True, (1, 1)),
        (False, (2, 2, 1)),
        (False, (2, 1, 2)),
        (False, (2, None, 1)),
    ]
    for ans, tup in cases:
        tree = Treap(gen_treap_node(tup))
        assert is_treap(tree) is ans


def test_treap_insert():
    run_bstree_insert_test(7, gen_treap_by_insert, is_treap, 'Treap::insert()')


def test_treap_insert_large():
    run_bstree_insert_test_large(2000, Treap, is_treap, 'Treap::insert() large case')


def test_treap_remove():
    run_bstree_remove_test(7, gen_treap_by_insert, is_treap, 'Treap::remove()')
