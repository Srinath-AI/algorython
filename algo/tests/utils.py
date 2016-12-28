import random
from collections import OrderedDict
from itertools import chain
from contextlib import contextmanager
from time import perf_counter
import functools

from algo.heap import heap_left, heap_right
from algo.tree.basetree import print_tree, BaseTree
from algo.tree.bstree import BSNode, is_bstree


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


def gen_sort_case(maxlen):
    for seq in asc_seq(maxlen):
        yield from perm_seq(seq)


def gen_special_sort_case(size):
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

    for case, kv in mat:
        cells = [case]
        for desc, value in kv:
            cells.append(fmt_time(value))
        table.append(cells)

    def print_table(row_list):
        def max_col_width(i):
            return max(len(row[i]) for row in row_list)

        col_width = [ max_col_width(i) for i in range(len(row_list[0])) ]
        lines = []
        for rowno, row in enumerate(row_list):
            just = str.rjust if rowno != 0 else str.ljust
            line = '│'.join(just(cell, col_width[i]) for i, cell in enumerate(row))
            lines.append('│' + line + '│')

            if rowno == 0:
                line = '┿'.join(just('', col_width[i], '━') for i in range(len(row)))
                lines.append('┝' + line + '┥')

        print('\n'.join(lines))
        print()

    print_table(table)


def print_histogram(pairs, width=80):
    block_chars = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]

    # TODO: handle fullwidth char
    max_label_len = len(str(max(pairs, key=lambda x: len(str(x[0])))[0]))

    def get_bar(percent, max_width):
        blocks = percent * max_width
        fullblocks = int(blocks)

        bar = fullblocks * block_chars[-1]
        if fullblocks != blocks:
            halfblock_idx = int((blocks - fullblocks) * len(block_chars))
            bar += block_chars[halfblock_idx]

        return bar

    for label, value in pairs:
        print(str(label).rjust(max_label_len), end='')
        print(get_bar(value, width - max_label_len))


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


def run_bstree_insert_test(maxsize, gen_bstree, verifier, desc):
    with timed_test(desc) as get_duration:
        tree_count = 0
        for tree, count in gen_bstree(maxsize):
            assert tree.count() == count \
                   and verifier(tree) and is_bstree(tree), print_tree(tree)
            tree_count += 1

    case_per_sec = tree_count / get_duration()
    print('maxsize: {maxsize}, cases: {tree_count}, case_per_sec: {case_per_sec:.1f}'
          .format_map(locals()))


def run_bstree_insert_test_large(case_size, tree_type, verifier, desc):
    check_inteval = case_size // 100
    cases = gen_special_sort_case(case_size)

    with timed_test(desc):
        for case_name, arr in cases.items():
            tree = tree_type()
            for i, x in enumerate(arr):
                tree.insert(x)
                if i % check_inteval == 0:
                    assert verifier(tree), (x, print_tree(tree))


def run_bstree_remove_test(maxsize, gen_bstree, verifier, desc):
    def removed_one(arr, el):
        arr = arr.copy()
        arr.remove(el)
        return arr

    def print_failing(before, removing, after):
        print('before')
        print_tree(before)
        print('removing', removing)
        print_tree(after)
        print()

    def test_remove(t):
        flatten = list(t.data_iter())
        for to_remove in sorted(set(flatten)):
            test_tree = t.deepcopy()
            try:
                removed_node = test_tree.remove(to_remove)
            except Exception:
                print_failing(t, to_remove, test_tree)
                raise

            assert removed_node.data == to_remove \
                   and list(test_tree.data_iter()) == removed_one(flatten, to_remove) \
                   and verifier(test_tree) \
                   and is_bstree(test_tree), print_failing(t, to_remove, test_tree)

        test_tree = t.deepcopy()
        assert test_tree.remove(min(flatten, default=0) - 1) is None
        assert test_tree.remove(max(flatten, default=0) + 1) is None

    with timed_test(desc) as get_duration:
        tree_count = 0
        for tree, count in gen_bstree(maxsize):
            test_remove(tree)
            tree_count += 1

    case_per_sec = tree_count / get_duration()
    print('maxsize: {maxsize}, cases: {tree_count}, case_per_sec: {case_per_sec:.1f}'
          .format_map(locals()))


def run_bstree_remove_test_large(size, tree_type, verifier, desc):
    arr = [ random.randrange(size * 0.9) for _ in range(size) ]
    sorted_arr = sorted(arr)

    tree = tree_type()  # type: BaseTree
    for x in arr:
        tree.insert(x)

    random.shuffle(arr)
    to_remove = arr[:size // 3]

    for x in set(to_remove):
        test_tree = tree.deepcopy()
        assert test_tree.remove(x).data == x
        arr_removed = sorted_arr.copy()
        arr_removed.remove(x)
        assert list(test_tree.data_iter()) == arr_removed


def run_bstree_insert_remove_mix(size, tree_type, verifier, desc):
    arr = [ random.randrange(size * 0.9) for _ in range(size) ]
    inserted = []

    tree = tree_type()  # type: BaseTree

    def remove_one():
        remove_idx = random.randrange(len(inserted))
        inserted[-1], inserted[remove_idx] = inserted[remove_idx], inserted[-1]
        to_remove = inserted.pop()
        removed_node = tree.remove(to_remove)
        assert removed_node.data == to_remove
        assert verifier(tree)

    # grow
    for i, x in enumerate(arr):
        inserted.append(x)
        tree.insert(x)
        assert verifier(tree)
        if i % 2 == 0:
            remove_one()

    # shrink
    random.shuffle(arr)
    rand_gen = iter(arr)
    while inserted:
        remove_one()
        tree.insert(next(rand_gen))
        assert verifier(tree)
        remove_one()


def check_repr_svg(obj):
    def strip_space(s):
        return ''.join(ch for ch in s if not ch.isspace())

    svg = obj._repr_svg_()
    assert strip_space(svg).startswith(strip_space('''
        <?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
         "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        <!-- Generated by graphviz'''))
