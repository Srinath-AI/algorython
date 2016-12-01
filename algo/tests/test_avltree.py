from algo.tests.utils import timeit, gen_bstree_by_insert
from algo.tree.basetree import print_tree
from algo.tree.bstree import is_bstree
from algo.tree.avltree import AVLTree, is_avltree


def gen_avltree_by_insert(maxlen):
    yield from gen_bstree_by_insert(maxlen, AVLTree, lambda node: None)


@timeit('AVLTree::insert()')
def test_avltree_insert():
    tree_count = 0
    for tree, count in gen_avltree_by_insert(9):
        assert tree.count() == count \
            and is_avltree(tree) and is_bstree(tree), print_tree(tree)
        tree_count += 1
