import random
from collections import OrderedDict
from itertools import chain
from contextlib import contextmanager
from time import perf_counter
import functools

from algo.heap import heap_left, heap_right
from algo.tree.bstree import BSNode


def asc_seq(maxlen):
    # %timeit -n 1000 list(map(list, asc_seq(10)))
    # 1000 loops, best of 3: 3.04 ms per loop
    assert maxlen >= 0

    def g(seq):
        yield seq
        if len(seq) < maxlen:
            g1 = g(seq + [seq[-1]])
            g2 = g(seq + [seq[-1] + 1])
            while True:
                try:
                    yield next(g1)
                    yield next(g2)
                except StopIteration:
                    break

    yield []
    if maxlen > 0:
        yield from g([0])


def asc_seq_alt(maxlen):
    # %timeit -n 1000 list(map(list, asc_seq_alt(10)))
    # 1000 loops, best of 3: 1.71 ms per loop
    assert maxlen >= 0

    def g(seq):
        yield seq
        if len(seq) < maxlen:
            seq.append(seq[-1])
            yield from g(seq)

            seq[-1] += 1
            yield from g(seq)
            seq.pop()

    yield []
    if maxlen > 0:
        yield from g([0])


def group_asc_seq(seq):
    ans = []
    cur = -1
    count = None
    for n in chain(seq, [-2]):
        if n != cur:
            ans.append(count)
            cur = n
            count = 1
        else:
            count += 1

    return ans[1:]


def perm2(grp1, grp2, cls1=True, cls2=False):
    buf = []

    def g(grp1, grp2):
        if grp1 == 0:
            buf.extend([cls2] * grp2)
            yield buf
            del buf[-grp2:]
        elif grp2 == 0:
            buf.extend([cls1] * grp1)
            yield buf
            del buf[-grp1:]
        else:
            buf.append(cls1)
            yield from g(grp1 - 1, grp2)
            buf.pop()

            buf.append(cls2)
            yield from g(grp1, grp2 - 1)
            buf.pop()

    yield from g(grp1, grp2)


def fill(buf, elem, pattern):
    cur = 0
    for p in pattern:
        while buf[cur] is not None:
            cur += 1
        if p:
            buf[cur] = elem
        cur += 1


def unfill(buf, elem):
    for i in range(len(buf)):
        if buf[i] == elem:
            buf[i] = None


def perm_seq(seq):
    group = group_asc_seq(seq)
    total = sum(group)
    buf = [None] * total

    def g(cur, remain):
        grp1 = group[cur]
        grp2 = remain - grp1
        for pattern in perm2(grp1, grp2):
            fill(buf, cur, pattern)
            if grp2 == 0:
                yield buf
            else:
                yield from g(cur + 1, grp2)
            unfill(buf, cur)

    if total == 0:
        yield []
    else:
        yield from g(0, total)


def gen_case(maxlen):
    for seq in asc_seq(maxlen):
        yield from perm_seq(seq)


def gen_special_case(size):
    ascending = list(range(size))
    descending = list(reversed(ascending))

    rand = ascending.copy()
    random.shuffle(rand)

    dup = [0] * size

    ascending_hole = list(range(-0xfffffff, -0xfffffff + (size // 2)))
    ascending_hole.extend(list(range(0, size - (size // 2))))
    assert len(ascending_hole) == size

    ascending_shuf3 = ascending.copy()
    for i in range(0, size, 3):
        sub = ascending_shuf3[i:(i + 3)]
        random.shuffle(sub)
        ascending_shuf3[i:(i + 3)] = sub
        del sub, i

    pattern = [False] * int(size * 0.99)
    pattern.extend([True] * (size - len(pattern)))
    random.shuffle(pattern)

    dup99 = dup.copy()
    ascending99 = ascending.copy()
    descending99 = descending.copy()
    for i, p in enumerate(pattern):
        if p:
            dup99[i] = random.randint(-10086, +10086)
            ascending99[i] = random.randint(-10086, +10086)
            descending99[i] = random.randint(-10086, +10086)
        del i, p

    del size, pattern
    return OrderedDict(sorted(locals().items()))


def get_func_name(func):
    try:
        return func.__name__
    except AttributeError:
        return get_func_name(func.func)


def fmt_time(s):
    if s >= 10:
        return '%.1f s' % s
    elif s >= 1:
        return '%.2f s' % s
    elif s >= 0.1:
        return '%.0f ms' % (s * 1000)
    elif s >= 0.01:
        return '%.1f ms' % (s * 1000)
    elif s >= 0.001:
        return '%.2f ms' % (s * 1000)
    else:
        return '%.3f ms' % (s * 1000)


def print_matrix(mat):
    head = ['']
    for desc, value in mat[0][1]:
        head.append(desc)
    table = [head]

    for row in mat:
        case, kv = row
        line = [case]
        for desc, value in kv:
            line.append(fmt_time(value))
        table.append(line)

    def print_table(table):
        def max_col_width(i):
            return max(len(row[i]) for row in table)

        col_width = [ max_col_width(i) for i in range(len(table[0])) ]
        lines = []
        for rowno, row in enumerate(table):
            just = str.rjust if rowno != 0 else str.ljust
            line = '│'.join(just(cell, col_width[i]) for i, cell in enumerate(row))
            lines.append('│' + line + '│')

            if rowno == 0:
                line = '┿'.join(just('', col_width[i], '━') for i in range(len(row)))
                lines.append('┝' + line + '┥')

        print('\n'.join(lines))
        print()

    print_table(table)


@contextmanager
def timed_test(name, test_name=''):
    def get_duration():
        return duration

    t1 = perf_counter()
    try:
        yield get_duration
    except Exception:
        print(name, 'failed', test_name, 'with an exception.')
        raise
    else:
        duration = perf_counter() - t1
        print(name, 'passed', test_name, 'test in', fmt_time(duration))


def timeit(name, test_name=''):
    assert isinstance(name, str)

    def decorator(f):
        @functools.wraps(f)
        def wrapped():
            with timed_test(name, test_name):
                f()

        return wrapped

    return decorator


def bstree_to_key(tree, extra_attr=lambda node: None):
    serial = 0
    prev = None

    def node_to_key(node):
        nonlocal serial, prev

        if node is None:
            return None

        left = node_to_key(node.left)
        if prev and node.data != prev.data:
            serial += 1
        prev = node
        return serial, extra_attr(node), left, node_to_key(node.right)

    return node_to_key(tree.root)


def gen_bstree_by_insert(max_len, tree_type, extra_attr):
    nums = []
    used = set()

    def recur(tree, count):
        nonlocal nums

        # exclude duplicated case
        key = bstree_to_key(tree, extra_attr)
        if key in used:
            return
        else:
            used.add(key)

        if not nums:
            new_nums = uniq_nums = [0]
        else:
            uniq_nums = sorted(set(nums))
            new_nums = [ (uniq_nums[i] + uniq_nums[i + 1]) / 2 for i in range(len(uniq_nums) - 1) ]
            new_nums.extend([min(nums) - 1, max(nums) + 1])

        for num in chain(new_nums, uniq_nums):
            nums.append(num)

            t = tree.deepcopy()
            t.insert(num)
            yield t, count
            if len(nums) < max_len:
                yield from recur(t, count + 1)

            nums.pop()

    yield from recur(tree_type(), 1)


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
