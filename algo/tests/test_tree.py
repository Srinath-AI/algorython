from time import perf_counter
from collections import Counter
from functools import partial
from itertools import chain

from algo.tree import *
from algo.heap import heap_parent
from algo.tests.utils import get_func_name


def gen_tree_shape(level):
    # %time list(map(list, gen_tree_shape(5)))
    # Wall time: 2.87 s

    size = 2 ** level - 1
    heap = [False] * size

    def g(start):
        if start >= size:
            raise StopIteration

        parent = heap_parent(start)
        if parent < 0 or heap[parent]:
            heap[start] = True
            yield heap
            yield from g(start + 1)
            heap[start] = False

        next_start = start + 1
        # while next_start < size and not heap[heap_parent(next_start)]:
        #     next_start += 1
        yield from g(next_start)

    yield heap
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
    for iterator in (middle_iter, middle_iter_bystack):
        t1 = perf_counter()
        for root in gen_bst(4):
            count = BSTree(root).count()
            expanded = list(iterator(root))
            assert len(expanded) == count
            assert sorted(expanded, key=lambda n: n.data) == expanded, \
                '{expanded}'.format_map(vars())

        duration = perf_counter() - t1
        print(get_func_name(iterator), 'passed test in', duration, 's.')


def test_is_bstree():
    for iterator in (middle_iter, middle_iter_bystack):
        is_bstree_func = partial(is_bstree, iterator=iterator)

        t1 = perf_counter()
        for bst in gen_bst(4):
            assert is_bstree_func(bst)

        not_bst = (
            [0, 1, 2],
            [0, 1],
            [0, -1, 2, -2, 1]
        )
        for heap in not_bst:
            tree = BaseTree.from_heap(heap)
            assert not is_bstree_func(tree.root)

        duration = perf_counter() - t1
        print('is_bstree() with', get_func_name(iterator), 'passed test in', duration, 's.')


def test_bst_find():
    t1 = perf_counter()
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

    duration = perf_counter() - t1
    print('BSTree::find_*() passed test in', duration, 's.')


def test_bst_insert():
    t1 = perf_counter()
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
            tree.insert(BSNode(num))
            assert tree.count() == count + 1
            assert is_bstree(tree.root)

    duration = perf_counter() - t1
    print('BSTree::insert() passed test in', duration, 's.')


def test_bst_remove():
    t1 = perf_counter()
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
            assert tree.remove_first(num)
            assert tree.count() == count - 1
            assert is_bstree(tree.root)

        for num in not_exist:
            tree = BSTree(root.deepcopy() if root else root)
            assert not tree.remove_first(num)
            assert tree.count() == count

    duration = perf_counter() - t1
    print('BSTree::remove_first() passed test in', duration, 's.')


def test_bst_remove_alt():
    orgin = BSNode.remove_self
    BSNode.remove_self = BSNode.remove_self_alt
    print('!!! use alternative implementation of node removal. !!!')
    test_bst_remove()
    BSNode.remove_self = orgin


def test_bst_max_min():
    t1 = perf_counter()
    for root in gen_bst(4):
        tree = BSTree(root)
        if root:
            assert tree.min() is next(tree.node_iter())
            assert tree.max() is list(tree.node_iter())[-1]
        else:
            assert tree.min() is None
            assert tree.max() is None

    duration = perf_counter() - t1
    print('BSTree::min() & BSTree::max() passed test in', duration, 's.')


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
        assert is_rbtree(tree.root) is ans


def test_pretty_tree():
    R, B = RBNode.RED, RBNode.BLACK
    tree = rbtree_from_nested_list([B, B, [B, R, R]])
    ans = '''
       ■1
   ┌───┴───────┐
   ■0          ■3
 ┌─┴─┐     ┌───┴───┐
NIL NIL    □2      □4
         ┌─┴─┐   ┌─┴─┐
        NIL NIL NIL NIL'''

    def process(string):
        return [ line.rstrip() for line in string.splitlines() if line.strip() ]

    output = pretty_tree(tree.root)
    assert process(output) == process(ans)


def test_rbtree_insert():
    max_len = 7
    nums = []

    def recur(tree, count):
        nonlocal nums

        if not nums:
            new_nums = uniq_nums = [0]
        else:
            uniq_nums = sorted(set(nums))
            new_nums = [ (uniq_nums[i] + uniq_nums[i + 1]) / 2 for i in range(len(uniq_nums) - 1) ]
            new_nums.extend([min(nums) - 1, max(nums) + 1])

        for num in chain(new_nums, uniq_nums):
            nums.append(num)

            t = tree.deepcopy()
            t.insert_data(num)
            assert t.count() == count + 1
            assert is_rbtree(t.root)
            assert is_bstree(t.root)
            if len(nums) < max_len:
                recur(t, count + 1)

            nums.pop()

    t1 = perf_counter()
    recur(RBTree(), 0)
    duration = perf_counter() - t1

    print('RBTree::insert_data() passed test in', duration, 's.')


if __name__ == '__main__':
    test_middle_iter()
    test_is_bstree()
    test_bst_find()
    test_bst_insert()
    test_bst_remove()
    test_bst_remove_alt()
    test_bst_max_min()

    test_is_rbtree()
    test_pretty_tree()
    test_rbtree_insert()
