from algo.tests.utils import (
    gen_bstree_by_insert, run_bstree_insert_test, run_bstree_insert_test_large,
    run_bstree_remove_test, run_bstree_remove_test_large,
)
from algo.tree.rbtree import RBTree, RBNode, is_rbtree


def rbtree_from_nested_list(seq):
    serial = 0

    def create_root(seq):
        nonlocal serial

        if seq is None:
            return None
        if not isinstance(seq, (tuple, list)):
            seq = (seq,)
        assert 1 <= len(seq) <= 3

        color = seq[0]
        left = seq[1] if len(seq) >= 2 else None
        right = seq[2] if len(seq) == 3 else None

        node_left = create_root(left)
        node = RBNode(serial, color)
        serial += 1
        node.left = node_left
        node.right = create_root(right)
        return node

    root = create_root(seq)
    return RBTree(root)


def test_is_rbtree():
    R, B = RBNode.RED, RBNode.BLACK
    cases = (
        (True,  None),
        (True,  (B, None, None)),
        (False, (R, None, None)),
        (True,  (B,
                    R,
                    R,)),
        (True,  (B,
                    None,
                    R,)),
        (False, (B,
                    B,
                    None)),
        (True,  (B,
                    B,
                    B)),
        (False, (B,
                    (R,
                        B),
                    (R,
                        B),)),
        (False, (B,
                    (R,
                        R,
                        R),
                    R,)),
        (True,  (B,
                    B,
                    (R,
                        B,
                        B),)),
    )

    for ans, ques in cases:
        tree = rbtree_from_nested_list(ques)
        assert is_rbtree(tree) is ans


def gen_rbtree_by_insert(max_len):
    yield from gen_bstree_by_insert(max_len, RBTree, lambda node: node.color)


def test_rbtree_insert():
    run_bstree_insert_test(8, gen_rbtree_by_insert, is_rbtree, 'RBTree::insert()')


def test_rbtree_insert_large():
    run_bstree_insert_test_large(2000, RBTree, is_rbtree, 'RBTree::insert() large case')


def test_rbtree_remove():
    run_bstree_remove_test(8, gen_rbtree_by_insert, is_rbtree, 'RBTree::remove()')


def test_rbtree_remove_large():
    run_bstree_remove_test_large(1000, RBTree, is_rbtree, 'RBTree::remove() large case')
