from algo.sort import qsort_part3_random, qsort_part_tail
from algo.utils import ReversedKey


# BEGIN select nth

def nth_small(arr, n, key=None, part_func=qsort_part3_random):
    assert len(arr) > 0
    assert 1 <= n <= len(arr)
    if len(arr) == 1:
        return arr[0]
    key = key or (lambda x: x)

    start, stop = 0, len(arr) - 1
    while True:
        p1, p2 = part_func(arr, start, stop, key)
        if p2 <= n - 1:
            start = p2
        elif p1 > n - 1:
            stop = p1 - 1
        else:
            return arr[n - 1]


def nth_small_tail(arr, n, key=None, part_func=qsort_part_tail):
    assert len(arr) > 0
    assert 1 <= n <= len(arr)
    if len(arr) == 1:
        return arr[0]
    key = key or (lambda x: x)

    start, stop = 0, len(arr) - 1
    while True:
        mid = part_func(arr, start, stop, key)
        if mid < n - 1:
            start = mid + 1
        elif mid > n - 1:
            stop = mid - 1
        else:
            return arr[n - 1]


def _nth_large_wrapper(small, name):
    def nth_large_func(arr, n, key=None, **kwargs):
        key = key or (lambda x: x)
        return small(arr, n, key=lambda x: ReversedKey(key(x)), **kwargs)

    nth_large_func.__name__ = name
    return nth_large_func


nth_large = _nth_large_wrapper(nth_small, 'nth_large')


# median of median of 5
def nth_small_mm(arr, n, key=None, group=5, _begin=None, _end=None):
    assert group >= 5 and group % 2 == 1

    if _begin is None:
        _begin = 0
    if _end is None:
        _end = len(arr)
    assert _end - _begin > 0
    assert 1 <= n <= _end - _begin

    key = key or (lambda x: x)

    # select minimum element
    if n == 1:
        min_idx = min(range(_begin, _end), key=lambda x: key(arr[x]))
        arr[_begin], arr[min_idx] = arr[min_idx], arr[_begin]
        return arr[_begin]

    def part():
        med_end = _begin
        for start in range(_begin, _end, group):
            # indexes for 5-sized group
            indexes = list(range(start, min(start + group, _end)))
            indexes.sort(key=lambda x: key(arr[x]))
            med_idx = indexes[(len(indexes) + 1) // 2 - 1]

            # move median to begin of array
            arr[med_idx], arr[med_end] = arr[med_end], arr[med_idx]
            med_end += 1

        sub_n = (med_end - _begin + 1) // 2
        assert sub_n >= 1, 'begin: {}, end: {}'.format(_begin, _end)

        nth_small_mm(arr, sub_n, key=key, group=group, _begin=_begin, _end=med_end)
        # swap median of median to end
        arr[_begin + sub_n - 1], arr[_end - 1] = arr[_end - 1], arr[_begin + sub_n - 1]
        return qsort_part3_random(arr, _begin, _end - 1, key=key)

    origin_begin = _begin
    while True:
        p1, p2 = part()
        if p2 - origin_begin <= n - 1:
            _begin = p2
        elif p1 - origin_begin > n - 1:
            _end = p1
        else:
            return arr[n - 1]


nth_large_mm = _nth_large_wrapper(nth_small_mm, 'nth_large_mm')

# END select nth
