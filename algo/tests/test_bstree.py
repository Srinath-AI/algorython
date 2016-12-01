from collections import Counter
from functools import partial

from algo.tests.utils import timed_test, get_func_name, timeit
from algo.tests.test_tree import gen_bst
from algo.tree.basetree import BaseTree, middle_iter, middle_iter_bystack, middle_iter_sm
from algo.tree.bstree import BSTree, is_bstree


def test_is_bstree():
    for iterator in (middle_iter, middle_iter_bystack, middle_iter_sm):
        is_bstree_func = partial(is_bstree, iterator=iterator)

        with timed_test('is_bstree(*, iterator={})'.format(get_func_name(iterator))):
            for bst in gen_bst(4):
                assert is_bstree_func(BSTree(bst))

            not_bst = (
                [0, 1, 2],
                [0, 1],
                [0, -1, 2, -2, 1]
            )
            for heap in not_bst:
                tree = BaseTree.from_heap(heap)
                assert not is_bstree_func(tree)


@timeit('BSTree::find_*()')
def test_bst_find():
    for root in gen_bst(4):
        tree = BSTree(root)
        counter = Counter(n.data for n in tree.node_iter())

        if not counter:
            assert list(tree.find_all(0)) == []

        for key, count in counter.items():
            nodes = list(tree.find_all(key))
            assert len(nodes) == count
            assert all(n.data == key for n in nodes)
            assert tree.find_first(key).data == key

        for non_exist in (min(tree.data_iter(), default=0) - 1,
                          max(tree.data_iter(), default=0) + 1):
            assert tree.find_first(non_exist) is None


@timeit('BSTree::insert()')
def test_bst_insert():
    for root in gen_bst(4):
        tree = BSTree(root)
        to_insert = sorted(set(tree.data_iter()))
        for i in range(len(to_insert) - 1):
            mid = (to_insert[i] + to_insert[i + 1]) / 2
            to_insert.append(mid)
        to_insert.append((min(to_insert)) - 1 if root else -1)
        to_insert.append((max(to_insert)) + 1 if root else +1)

        for num in to_insert:
            tree = BSTree(root.deepcopy() if root else root)
            count = tree.count()
            tree.insert(num)
            assert tree.count() == count + 1
            assert is_bstree(tree)


@timeit('BSTree::remove()')
def test_bst_remove():
    for root in gen_bst(4):
        tree = BSTree(root)
        to_remove = sorted(set(tree.data_iter()))

        not_exist = []
        for i in range(len(to_remove) - 1):
            mid = (to_remove[i] + to_remove[i + 1]) / 2
            not_exist.append(mid)
        not_exist.append((min(to_remove)) - 1 if root else -1)
        not_exist.append((max(to_remove)) + 1 if root else +1)

        count = tree.count()

        for num in to_remove:
            tree = BSTree(root.deepcopy())
            assert tree.remove(num).data == num
            assert tree.count() == count - 1
            assert is_bstree(tree)

        for num in not_exist:
            tree = BSTree(root.deepcopy() if root else root)
            assert not tree.remove(num)
            assert tree.count() == count


@timeit('BSTree::min() & BSTree::max()')
def test_bst_max_min():
    for root in gen_bst(4):
        tree = BSTree(root)
        if root:
            assert tree.min() is next(tree.node_iter())
            assert tree.max() is list(tree.node_iter())[-1]
        else:
            assert tree.min() is None
            assert tree.max() is None
