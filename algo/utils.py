import functools
import operator


class ComparableBaseMeta(type):
    def __new__(mcs, name, bases, namespace):
        klass = super().__new__(mcs, name, bases, namespace)
        for op_name in ('eq', 'ne', 'lt', 'gt', 'le', 'ge', 'sub'): # __sub__ may be used for comparison
            method_name = '__{}__'.format(op_name)

            def create_method(op_name):
                @functools.wraps(getattr(int, method_name))
                def method(self, other):
                    return mcs.compare(op_name, self, other)
                return method

            setattr(klass, method_name, create_method(op_name))

        return klass

    @staticmethod
    def compare(op_name, a, b):
        return NotImplemented


class ReversedKeyMeta(ComparableBaseMeta):

    @staticmethod
    def compare(op_name, a, b):
        method_name = '__{}__'.format(op_name)
        return getattr(b.value, method_name)(a.value)


class ReversedKey(metaclass=ReversedKeyMeta):
    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value


class WrappedDataMeta(ComparableBaseMeta):

    @staticmethod
    def compare(op_name, a, b):
        ops = getattr(operator, op_name)
        return ops(a.keyed, b.keyed)


class WrappedData(metaclass=WrappedDataMeta):
    __slots__ = ('data', 'keyed')

    def __init__(self, data, key):
        self.data = data
        self.keyed = key(data)
