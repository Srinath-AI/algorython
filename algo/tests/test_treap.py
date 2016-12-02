from algo.tests.utils import timeit, gen_bstree_by_insert
from algo.tree.basetree import print_tree
from algo.tree.bstree import is_bstree
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


@timeit('Treap::insert()')
def test_treap_insert():
    tree_count = 0
    maxsize = 7
    for tree, count in gen_treap_by_insert(maxsize):
        assert tree.count() == count \
            and is_treap(tree) and is_bstree(tree), print_tree(tree)
        tree_count += 1
    print('tree_count', tree_count, 'maxsize', maxsize)


@timeit('Treap::remove()')
def test_treap_remove():
    def removed_one(arr, el):
        arr = arr.copy()
        arr.remove(el)
        return arr

    def test_remove(t):
        flatten = list(t.data_iter())
        for to_remove in sorted(set(flatten)):
            test_tree = t.deepcopy()
            removed_node = test_tree.remove(to_remove)
            assert removed_node.data == to_remove
            assert list(test_tree.data_iter()) == removed_one(flatten, to_remove)
            assert is_treap(test_tree)
            assert is_bstree(test_tree)

        test_tree = t.deepcopy()
        assert test_tree.remove(min(flatten, default=0) - 1) is None
        assert test_tree.remove(max(flatten, default=0) + 1) is None

    for tree, count in gen_treap_by_insert(7):
        test_remove(tree)
