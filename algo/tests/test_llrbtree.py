from algo.tests.utils import (
    gen_bstree_by_insert, run_bstree_insert_test, run_bstree_insert_test_large,
    run_bstree_remove_test, run_bstree_remove_test_large, run_bstree_insert_remove_mix,
)
from algo.tests.test_rbtree import rbtree_from_nested_list
from algo.tree.llrbtree import RBNode, LLRBTree, is_llrbtree


def test_is_llrbtree():
    R, B = RBNode.RED, RBNode.BLACK
    cases = (
        (True,  None),
        (True,  (B, None, None)),
        (False, (R, None, None)),
        (True,  (B,
                    R,
                    R,)),
        (True,  (B,
                    (R,
                        B,
                        B),
                    B,)),
        (False, (B,
                    B,
                    (R,
                        B,
                        B),)),
    )

    for ans, ques in cases:
        tree = rbtree_from_nested_list(ques)
        assert is_llrbtree(tree) is ans


def gen_llrbtree_by_insert(max_len):
    yield from gen_bstree_by_insert(max_len, LLRBTree, lambda node: node.color)


def test_llrbtree_insert():
    run_bstree_insert_test(8, gen_llrbtree_by_insert, is_llrbtree, 'LLRBTree::insert()')


def test_llrbtree_insert_large():
    run_bstree_insert_test_large(2000, LLRBTree, is_llrbtree, 'LLRBTree::insert() large case')


def test_llrbtree_remove():
    run_bstree_remove_test(8, gen_llrbtree_by_insert, is_llrbtree, 'LLRBTree::remove()')


def test_llrbtree_remove_large():
    run_bstree_remove_test_large(1000, LLRBTree, is_llrbtree, 'LLRBTree::remove() large case')


def test_llrbtree_remove_insert_mix():
    run_bstree_insert_remove_mix(1000, LLRBTree, is_llrbtree, 'LLRBTree insertion & removal')
