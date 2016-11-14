import random

from algo.heap import heap_make, heap_pop
from algo.utils import ReversedKey

# TODO: hybrid sort


def get_sort_key(**kwargs):
    key = kwargs.get('key') or (lambda x: x)
    nkey = (lambda x: ReversedKey(key(x))) if kwargs.get('reverse', False) else key
    return nkey


# BEGIN quick sort

def qsort_part_tail(arr, start, stop, key):
    assert start <= stop
    ref = key(arr[stop])
    p2 = start
    for remain in range(start, stop):
        if key(arr[remain]) < ref:
            arr[p2], arr[remain] = arr[remain], arr[p2]
            p2 += 1

    arr[p2], arr[stop] = arr[stop], arr[p2]
    return p2


def qsort_part_head(arr, start, stop, key):
    assert start <= stop
    ref = key(arr[start])
    p2 = start + 1
    for remain in range(start + 1, stop + 1):
        if key(arr[remain]) < ref:
            arr[p2], arr[remain] = arr[remain], arr[p2]
            p2 += 1

    p2 -= 1
    arr[p2], arr[start] = arr[start], arr[p2]
    return p2


def qsort_part_random(arr, start, stop, key):
    key_idx = random.randint(start, stop)
    arr[stop], arr[key_idx] = arr[key_idx], arr[stop]
    return qsort_part_tail(arr, start, stop, key)


def qsort_part_hoare_like(arr, start, stop, key):
    ref = key(arr[stop])
    i, j = start, stop - 1
    while True:
        while key(arr[i]) < ref:
            i += 1
        while i <= j and not (key(arr[j]) < ref):
            j -= 1

        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
        else:
            arr[i], arr[stop] = arr[stop], arr[i]
            return i


def qsort_part3_alt(arr, start, stop, key):
    # this is much slower than qsort_part3
    ref = key(arr[start])
    p1 = start
    p2 = start + 1

    for remain in range(start + 1, stop + 1):
        cur = key(arr[remain])
        if cur <= ref:
            arr[p2], arr[remain] = arr[remain], arr[p2]
            p2 += 1
        if cur < ref:
            arr[p2 - 1], arr[p1] = arr[p1], arr[p2 - 1]
            p1 += 1

    return p1, p2


def qsort_part3(arr, start, stop, key):
    ref = key(arr[start])
    p1 = start
    p2 = stop

    cur = start + 1
    while cur <= p2:
        el = key(arr[cur])
        if el < ref:
            arr[p1], arr[cur] = arr[cur], arr[p1]
            p1 += 1
            cur += 1
        elif el > ref:
            arr[p2], arr[cur] = arr[cur], arr[p2]
            p2 -= 1
        else:
            cur += 1

    return p1, p2 + 1


def qsort_part3_random(arr, start, stop, key):
    key_idx = random.randint(start, stop)
    arr[start], arr[key_idx] = arr[key_idx], arr[start]
    return qsort_part3(arr, start, stop, key)


def qsort(arr, key=None, reverse=False, part_func=qsort_part_tail):
    if len(arr) <= 1:
        return

    key = get_sort_key(key=key, reverse=reverse)

    stack = [(0, len(arr) - 1)]
    while stack:
        start, stop = stack.pop()
        p2 = part_func(arr, start, stop, key)

        if p2 - 1 > start:
            stack.append((start, p2 - 1))
        if stop > p2 + 1:
            stack.append((p2 + 1, stop))


def qsort3(arr, key=None, reverse=False, part_func=qsort_part3):
    if len(arr) <= 1:
        return

    key = get_sort_key(key=key, reverse=reverse)

    stack = [(0, len(arr) - 1)]
    while stack:
        start, stop = stack.pop()
        p1, p2 = part_func(arr, start, stop, key)

        if p1 - 1 > start:
            stack.append((start, p1 - 1))
        if p2 < stop:
            stack.append((p2, stop))

# END quick sort


# BEGIN heap sort

def heap_sort(arr, reverse=False, key=None):
    key = get_sort_key(key=key, reverse=reverse)
    heap_make(arr, key)
    for end in range(len(arr), 1, -1):
        heap_pop(arr, end, key)

# END heap sort


# BEGIN merge sort

def merge_sort(arr, reverse=False, key=None):
    key = get_sort_key(key=key, reverse=reverse)

    def merge_sort_rec(begin, end):
        if end - begin <= 1:
            return

        mid = (begin + end) // 2
        merge_sort_rec(begin, mid)
        merge_sort_rec(mid, end)

        left = arr[begin:mid]
        left_idx = 0
        right_idx = mid
        head = begin

        def use_left():
            if left_idx == len(left):
                return False
            elif right_idx == end:
                return True
            else:
                return key(left[left_idx]) <= key(arr[right_idx])

        for _ in range(end - begin):
            if use_left():
                arr[head] = left[left_idx]
                left_idx += 1
            else:
                arr[head] = arr[right_idx]
                right_idx += 1
            head += 1

    merge_sort_rec(0, len(arr))

# END merge sort


# BEGIN bucket sort

def bucket_sort(arr, bucket_size=16, min_buckets=4, reverse=False, key=None):
    if len(arr) == 0:
        return

    key = get_sort_key(reverse=reverse, key=key)

    bucket_num = len(arr) // bucket_size
    bucket_num = max(bucket_num, min_buckets)
    buckets = [ [] for _ in range(bucket_num) ]

    low, high = min(arr, key=key), max(arr, key=key)
    inteval = abs(key(high) - key(low)) / bucket_num
    if inteval == 0:
        return

    for elem in arr:
        idx = int(abs(key(elem) - key(low)) // inteval)
        idx = min(bucket_num - 1, idx)  # float division may be slightly larger than upper limit
        buckets[idx].append(elem)

    index = 0
    for buck in buckets:
        # buck.sort(key=key)
        merge_sort(buck, key=key)   # stable
        # qsort3(buck, key=key, part_func=qsort_part3_random)
        for elem in buck:
            arr[index] = elem
            index += 1

# END bucket sort
