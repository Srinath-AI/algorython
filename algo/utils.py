import functools
import operator


class ReversedKeyMeta(type):
    def __new__(mcs, name, bases, namespace):
        klass = super().__new__(mcs, name, bases, namespace)
        all_methods = (('eq', 'ne', 'lt', 'gt', 'le', 'ge',)     # comparison
                       + ('sub',))      # comparison by subtraction
        for method_name in all_methods:
            method_name = '__{}__'.format(method_name)

            def make_func(method_name):
                @functools.wraps(getattr(int, method_name))
                def func(self, other):
                    return getattr(other.value, method_name)(self.value)
                return func

            setattr(klass, method_name, make_func(method_name))

        return klass


class ReversedKey(metaclass=ReversedKeyMeta):
    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value


class WrappedDataMeta(type):
    def __new__(mcs, name, bases, namespace):
        klass = super().__new__(mcs, name, bases, namespace)
        for method_name in ('eq', 'ne', 'lt', 'gt', 'le', 'ge',):
            ops = getattr(operator, method_name)

            def make_func(ops):
                @functools.wraps(getattr(object, '__{}__'.format(method_name)))
                def func(self, other):
                    return ops(self.keyed, other.keyed)
                return func

            setattr(klass, '__{}__'.format(method_name), make_func(ops))

        return klass


class WrappedData(metaclass=WrappedDataMeta):
    __slots__ = ('data', 'keyed')

    def __init__(self, data, key):
        self.data = data
        self.keyed = key(data)
