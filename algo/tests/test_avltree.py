from algo.tests.utils import (
    gen_bstree_by_insert, run_bstree_insert_test, run_bstree_insert_test_large,
    run_bstree_remove_test, run_bstree_remove_test_large,
)
from algo.tree.basetree import print_tree
from algo.tree.avltree import AVLTree, AVLNode, is_avltree, avl_reheight


def gen_avltree_by_insert(maxlen):
    yield from gen_bstree_by_insert(maxlen, AVLTree, lambda node: None)


def test_is_avltree():
    serial = 0

    def avlnode_from_tuple(tup):
        nonlocal serial
        if tup is None:
            return None
        assert len(tup) == 2

        node = AVLNode(None)
        node.left = avlnode_from_tuple(tup[0])
        node.data = serial
        serial += 1
        node.right = avlnode_from_tuple(tup[1])
        avl_reheight(node)

        return node

    cases = [
        (True, None),
        (True, (None, None)),
        (True, (None, (None, None))),
        (False, ((None, (None, None)), None)),
        (False, (((None, None), None), None)),
        (True, ((None, (None, None)), (None, None))),
        (True, ((None, None), ((None, None), None))),
        (True, (((None, None), None), (None, None))),
    ]

    for ans, tup in cases:
        tree = AVLTree(avlnode_from_tuple(tup))
        assert is_avltree(tree) is ans, print_tree(tree)

    tree = AVLTree(avlnode_from_tuple((None, None)))
    tree.root.height += 1
    assert is_avltree(tree) is False, print_tree(tree)
    tree.root.height -= 2
    assert is_avltree(tree) is False, print_tree(tree)
    tree.root.height -= 2
    assert is_avltree(tree) is False, print_tree(tree)


def test_avltree_insert():
    run_bstree_insert_test(9, gen_avltree_by_insert, is_avltree, 'AVLTree::insert()')


def test_avltree_insert_large():
    run_bstree_insert_test_large(2000, AVLTree, is_avltree, 'AVLTree::insert() large case')


def test_avltree_remove():
    run_bstree_remove_test(9, gen_avltree_by_insert, is_avltree, 'AVLTree::remove()')


def test_avltree_remove_large():
    run_bstree_remove_test_large(1000, AVLTree, is_avltree, 'AVL::remove() large case')
