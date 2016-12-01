from algo.tests.utils import get_func_name, timed_test
from algo.tree.basetree import *
from algo.tree.bstree import *


def gen_tree_shape(max_level):
    # %time list(map(list, gen_tree_shape(5)))
    # Wall time: 1.5-1.8 s

    size = 2 ** max_level - 1
    heap = [False] * size

    def g(root):
        yield heap
        if root > size:
            return

        heap[root] = True

        left, right = heap_left(root), heap_right(root)
        if right < size:
            for _ in g(left):
                yield from g(right)
        elif left < size:
            yield from g(left)
        else:
            yield heap

        heap[root] = False

    yield from g(0)


def gen_tree(level, node_type=BSNode):
    def tree_from_shape(shape, root=0):
        if not shape[root]:
            return None
        else:
            node = node_type(None)
            if heap_left(root) < len(shape):
                node.left = tree_from_shape(shape, heap_left(root))
            if heap_right(root) < len(shape):
                node.right = tree_from_shape(shape, heap_right(root))

            return node

    for shape in gen_tree_shape(level):
        yield tree_from_shape(shape)


def gen_bst_from_tree(root, data=0, lo=None, hi=None):
    if root is None:
        yield root
        raise StopIteration

    root.data = data

    def gen_right():
        if root.right is not None:
            if root.right is not None and root.right.left is None:
                for _ in gen_bst_from_tree(root.right, data, lo=data, hi=hi):
                    yield root
            delta = 1 if hi is None else (hi - data) / 2
            for _ in gen_bst_from_tree(root.right, data + delta, lo=data, hi=hi):
                yield root
        else:
            yield root

    delta = -1 if lo is None else (lo - data) / 2
    for _ in gen_bst_from_tree(root.left, data + delta, hi=data, lo=lo):
        yield from gen_right()


def gen_bst(level):
    for t in gen_tree(level):
        yield from gen_bst_from_tree(t)


def test_middle_iter():
    for iterator in (middle_iter, middle_iter_bystack, middle_iter_sm):
        with timed_test(get_func_name(iterator)):
            for root in gen_bst(4):
                count = BSTree(root).count()
                expanded = list(iterator(root))
                expanded_sorted = sorted(expanded, key=lambda n: n.data)
                assert len(expanded) == count \
                    and expanded_sorted == expanded == list(middle_iter(root)), \
                    ('{expanded}'.format_map(vars()), print_tree(BSTree(root)))
