from algo.tests.utils import timeit, gen_bstree_by_insert
from algo.tree.basetree import print_tree
from algo.tree.bstree import is_bstree
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
        (False, ((None, (None, None)), (None, None))),
        (False, ((None, None), ((None, None), None))),
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


@timeit('AVLTree::insert()')
def test_avltree_insert():
    tree_count = 0
    maxsize = 9
    for tree, count in gen_avltree_by_insert(maxsize):
        assert tree.count() == count \
            and is_avltree(tree) and is_bstree(tree), print_tree(tree)
        tree_count += 1
    print('tree_count', tree_count, 'maxsize', maxsize)


# TODO: test_avltree* is identical to test_rbtree*
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
