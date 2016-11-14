import functools


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
