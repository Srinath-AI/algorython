from abc import abstractmethod

from collections import MutableSet as _MutableSet


class MutableSet(_MutableSet):
    def issubset(self, other):
        return self <= other

    def issuperset(self, other):
        return self >= other


class MutableMultiSet(MutableSet):
    @abstractmethod
    def discard_all(self, value):
        """Remove all element.  Do not raise an exception if absent."""
        while value in self:
            self.remove(value)

    @abstractmethod
    def remove_all(self, value):
        """Remove all element. If not a member, raise a KeyError."""
        self.remove(value)
        self.discard_all(value)
