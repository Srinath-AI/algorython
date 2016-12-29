import unittest
import pytest
from collections import defaultdict
from functools import partial

from algo.container.treeset import TreeSet, MultiTreeSet
from algo.container.abc import MutableSet, MutableMultiSet
from algo.skiplist import SkipList


class BaseTest:
    set_type = None

    def list_equiv(self, iterable):
        raise NotImplementedError

    def test_from_iterable(self):
        def run(iterable):
            ref = self.list_equiv(iterable)
            ts = self.set_type(iterable)
            assert list(ts) == ref

        run({1, 2, 3})
        run([1, 2, 3, 2])
        run(self.set_type([1, 2, 2, 3]))

    def test_contains(self):
        def run(seq):
            ts = self.set_type(seq)
            seq = self.list_equiv(seq)
            for a, b in zip(seq, seq[1:]):
                if a != b:
                    assert (a + b) / 2 not in ts
                    assert a in ts
                    assert b in ts

            assert min(seq, default=0) - 1 not in ts
            assert max(seq, default=0) + 1 not in ts

        run([2, 3, 4, 3])
        run([])

    def test_isdisjoint(self):
        def run(col1, col2):
            tree1, tree2 = self.set_type(col1), self.set_type(col2)
            ans = set(col1).isdisjoint(set(col2))
            assert tree1.isdisjoint(tree2) is ans
            assert tree2.isdisjoint(tree1) is ans
            assert tree1.isdisjoint(set(col2)) is ans
            assert tree2.isdisjoint(set(col1)) is ans

        run([], [])
        run([], [1])
        run([1, 2], [3, 4])
        run([1, 3], [2, 4])
        run([1, 2, 3, 4, 5], [4, 5, 6])
        run([1, 3, 5, 7], [2, 4, 6])

        ts = self.set_type()
        assert ts.isdisjoint(ts)
        ts.add(1)
        assert not ts.isdisjoint(ts)

    def test_subset(self):
        def counted(lst):
            d = defaultdict(int)
            for x in lst:
                d[x] += 1
            return d

        def list_issubsetof(list1, list2):
            c1, c2 = counted(list1), counted(list2)
            for x, c in c1.items():
                if c > c2[x]:
                    return False
            return True

        def list_issupersetof(list1, list2):
            return list_issubsetof(list2, list1)

        assert list_issubsetof([1, 2], [1, 2, 2])
        assert not list_issubsetof([2, 2, 2], [1, 2, 2])

        def run(col1, col2):
            tree1, tree2 = self.set_type(col1), self.set_type(col2)
            list1, list2 = self.list_equiv(tree1), self.list_equiv(tree2)
            assert tree1.issubset(tree2) is list_issubsetof(list1, list2)
            assert tree2.issubset(tree1) is list_issubsetof(list2, list1)
            assert tree1.issuperset(tree2) is list_issupersetof(list1, list2)
            assert tree2.issuperset(tree1) is list_issupersetof(list2, list1)

        run([], [])
        run([], [1])
        run([1, 2], [1])
        run([1, 2], [1, 2])
        run([1, 2, 2], [2, 2, 2])
        run([1, 2], [3])
        run([1, 3], [2, 4])
        run([1, 2], [1, 3])

        ts = self.set_type([1, 2, 2])
        assert ts.issubset(ts)
        assert ts.issuperset(ts)

    def test_eq(self):
        def run(col1, col2):
            ts1, ts2 = self.set_type(col1), self.set_type(col2)
            list1, list2 = self.list_equiv(col1), self.list_equiv(col2)
            assert (ts1 == ts2) is (ts2 == ts1) is (list1 == list2)

        run([], [])
        run([], [1])
        run([1], [1])
        run([1, 2], [1, 2, 3])
        run([1, 2, 2], [1, 2])
        run([1, 2, 2, 3], [1, 2, 2, 3])
        run([1, 2, 2, 3], [1, 2, 3, 3])

    def test_add(self):
        def run(seq):
            ts = self.set_type()
            for i, x in enumerate(seq):
                ts.add(x)
                ref = self.list_equiv(seq[:(i + 1)])
                assert list(ts) == ref

        run([])
        run([3, 2, 1])
        run([1, 2, 2, 3])
        run([1, 2, 3, 4, 2])

    def test_discard_remove(self):
        def run(col):
            for i in range(len(col)):
                subcol = sorted(col[:(i + 1)])
                for elem in subcol:
                    for to_remove in (elem, elem + 0.5):
                        ref = self.list_equiv(subcol)
                        try:
                            ref.remove(to_remove)
                        except ValueError:
                            exist = False
                        else:
                            exist = True

                        # discard
                        ts = self.set_type(subcol)
                        ts.discard(to_remove)
                        assert list(ts) == ref

                        # remove
                        ts = self.set_type(subcol)
                        if exist:
                            ts.remove(to_remove)
                            assert list(ts) == ref
                        else:
                            with pytest.raises(KeyError) as exc_info:
                                ts.remove(to_remove)
                            assert exc_info.value.args == (to_remove,)

        run([])
        run([1])
        run([1, 2, 2, 3])

    def test_clear(self):
        for col in [[1, 2, 3], []]:
            ts = self.set_type(col)
            ts.clear()
            assert len(ts) == 0 and list(ts) == []


class TestTreeSet(BaseTest, unittest.TestCase):
    set_type = TreeSet

    def list_equiv(self, iterable):
        return sorted(set(iterable))

    def test_abc(self):
        assert issubclass(self.set_type, MutableSet)


class TestMultiTreeSet(BaseTest, unittest.TestCase):
    set_type = MultiTreeSet

    def list_equiv(self, iterable):
        return sorted(iterable)

    def test_abc(self):
        assert issubclass(self.set_type, MutableMultiSet)

    def test_discard_all(self):
        def list_removed_all(lst, elem):
            lst = list(lst)
            while True:
                try:
                    lst.remove(elem)
                except ValueError:
                    return lst

        def run(col):
            lst = self.list_equiv(col)
            for el in set(lst):
                for elem in (el, el + 0.5):
                    ts = self.set_type(col)
                    ts.discard_all(elem)
                    ref = list_removed_all(lst, elem)
                    assert list(ts) == ref

                    if elem not in lst:
                        with pytest.raises(KeyError) as exc_info:
                            ts.remove_all(elem)
                        assert exc_info.value.args == (elem,)
                    else:
                        ts = self.set_type(col)
                        ts.remove_all(elem)
                        assert list(ts) == ref

        run([1])
        run([1, 1, 2, 3, 3, 3])


class TestTreeSetWithSkipList(TestTreeSet):
    set_type = partial(TreeSet, tree_type=SkipList)

    def test_abc(self):
        # not needed
        pass


class TestMultiTreeSetWithSkipList(TestMultiTreeSet):
    set_type = partial(MultiTreeSet, tree_type=SkipList)

    def test_abc(self):
        pass
