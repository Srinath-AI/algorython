from abc import abstractmethod

from algo.container.abc import MutableMultiSet, MutableSet
from algo.tree import RBTree


class BaseTreeSet:
    def __init__(self, iterable=None, *, tree_type=RBTree):
        self._tree = tree_type()
        self._size = 0
        if iterable is not None:
            self._bulk_add(iterable)

    def _bulk_add(self, iterable):
        if (isinstance(iterable, self.__class__)
                and iterable._tree.__class__ is self._tree.__class__):
            self._tree = iterable._tree.deepcopy()
            self._size = len(iterable)
        else:
            for value in iterable:
                self.add(value)

    @abstractmethod
    def add(self, value):
        raise NotImplementedError

    def __len__(self):
        return self._size

    def __iter__(self):
        return self._tree.data_iter()

    def __contains__(self, item):
        return self._tree.find(item) is not None

    def __le__(self, other):
        """Alias to issubset()"""
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self is other:
            return True

        other_iter = iter(other)
        other_value = None
        for value in self:
            while True:
                assert other_value is None or other_value < value
                try:
                    other_value = next(other_iter)
                except StopIteration:
                    return False

                if other_value > value:
                    # value in self not found in other
                    return False
                elif other_value == value:
                    other_value = None
                    break
        return True

    def __ge__(self, other):
        """Alias to issuperset()"""
        return other <= self

    def __eq__(self, other):
        if not isinstance(other, BaseTreeSet):
            return NotImplemented
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def isdisjoint(self, other):
        if self is other:
            return len(self) == 0
        elif isinstance(other, BaseTreeSet):
            if len(self) == 0 or len(other) == 0:
                return True
            return self._tree.isdisjoint(other._tree)
        else:
            return MutableSet.isdisjoint(self, other)

    def discard(self, value):
        node = self._tree.remove(value)
        if node is not None:
            self._size -= 1

    # not necessary
    def remove(self, value):
        node = self._tree.remove(value)
        if node is None:
            raise KeyError(value)
        else:
            self._size -= 1

    def clear(self):
        self._tree.clear()
        self._size = 0


class MultiTreeSet(BaseTreeSet, MutableMultiSet):
    def add(self, value):
        self._tree.insert(value)
        self._size += 1

    # not necessary
    def discard_all(self, value):
        while True:
            node = self._tree.remove(value)
            if node is None:
                break
            else:
                self._size -= 1

    def remove_all(self, value):
        self.remove(value)
        self.discard_all(value)


class TreeSet(BaseTreeSet, MutableSet):
    def add(self, value):
        if value not in self:
            self._tree.insert(value)
            self._size += 1
