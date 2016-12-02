from algo.tests.utils import timeit, gen_bstree_by_insert
from algo.tree.basetree import print_tree
from algo.tree.bstree import is_bstree
from algo.tree.avltree import AVLTree, is_avltree


def gen_avltree_by_insert(maxlen):
    yield from gen_bstree_by_insert(maxlen, AVLTree, lambda node: None)


@timeit('AVLTree::insert()')
def test_avltree_insert():
    tree_count = 0
    maxsize = 9
    for tree, count in gen_avltree_by_insert(maxsize):
        assert tree.count() == count \
            and is_avltree(tree) and is_bstree(tree), print_tree(tree)
        tree_count += 1
    print('tree_count', tree_count, 'maxsize', maxsize)


@timeit('AVLTree::remove()')
def test_avltree_remove():
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
            assert is_avltree(test_tree)
            assert is_bstree(test_tree)

        test_tree = t.deepcopy()
        assert test_tree.remove(min(flatten, default=0) - 1) is None
        assert test_tree.remove(max(flatten, default=0) + 1) is None

    for tree, count in gen_avltree_by_insert(9):
        test_remove(tree)
