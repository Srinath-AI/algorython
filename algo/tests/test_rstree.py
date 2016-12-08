from algo.tests.utils import gen_bstree_by_insert, run_bstree_insert_test, run_bstree_remove_test
from algo.tree.rstree import RSNode, RSTree, is_rstree


def gen_rstree_by_insert(maxlen):
    yield from gen_bstree_by_insert(maxlen, RSTree, lambda node: None)


def test_rstree_insert():
    run_bstree_insert_test(7, gen_rstree_by_insert, is_rstree, 'RSTree::insert()')


def test_rstree_remove():
    run_bstree_remove_test(7, gen_rstree_by_insert, is_rstree, 'RSTree::remove()')
