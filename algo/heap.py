from algo.utils import ReversedKey


def heap_parent(index):
    return (index + 1) // 2 - 1


def heap_left(index):
    return index * 2 + 1


def heap_right(index):
    return index * 2 + 2


def heap_adjust_top(arr, top, end, key):
    while True:
        child_indexes = [ func(top)
                          for func in (heap_left, heap_right)
                          if func(top) < end ]
        max_child_idx = max(child_indexes, key=lambda x: key(arr[x]), default=None)
        if max_child_idx is not None and key(arr[max_child_idx]) > key(arr[top]):
            arr[max_child_idx], arr[top] = arr[top], arr[max_child_idx]
            top = max_child_idx
        else:
            return


# def heap_make_naive(arr, key=None):
#     key = key or (lambda x: x)
#
#     for n in itertools.count():
#         if 2 ** n - 1 >= len(arr):
#             break
#
#     left = heap_parent(2 ** (n - 1) - 1)
#     right = heap_parent(len(arr) - 1)
#
#     while left >= 0:
#         for i in range(left, right + 1):
#             heap_adjust_top(arr, i, len(arr), key)
#         left = heap_parent(left)
#         right = 2 * left


def heap_make(arr, key=None):
    key = key or (lambda x: x)

    for i in range(heap_parent(len(arr) - 1), -1, -1):
        heap_adjust_top(arr, i, len(arr), key)


def heap_verify(arr, top=0, key=None):
    # TODO: non-recursive version
    key = key or (lambda x: x)
    child_indexes = [ func(top)
                      for func in (heap_left, heap_right)
                      if func(top) < len(arr) ]
    for child_idx in child_indexes:
        if key(arr[top]) < key(arr[child_idx]):
            return False
    else:
        return all(heap_verify(arr, child_idx, key) for child_idx in child_indexes)


def heap_pop(arr, end=None, key=None):
    if end is None:
        end = len(arr)
    assert 0 <= end <= len(arr)
    key = key or (lambda x: x)
    arr[0], arr[end - 1] = arr[end - 1], arr[0]
    heap_adjust_top(arr, 0, end - 1, key)


def heap_push(arr, elem, end=None, key=None):
    key = key or (lambda x: x)

    if end is None:
        end = len(arr)
    assert 0 <= end <= len(arr)
    if end == len(arr):
        arr.append(elem)
    else:
        arr[end] = elem

    up = heap_parent(end)
    cur = end
    while up >= 0 and key(arr[up]) < key(elem):
        arr[cur] = arr[up]
        cur = up
        up = heap_parent(up)
    arr[cur] = elem


# BEGIN top k

def topk_by_bigheap(arr, k, key=None):
    # O(n) + O(k*log(n))
    assert 0 <= k <= len(arr)

    heap_make(arr, key=key)
    for i in range(k):
        end = len(arr) - i  # TODO: limit the depth of heap to k
        heap_pop(arr, end, key=key)

    return arr[len(arr) - k:]


def topk_by_smallheap(arr, k, key=None):
    # O(n*log(k))
    assert 0 <= k <= len(arr)
    key = key or (lambda x: x)
    rkey = lambda x: ReversedKey(key(x))

    ans = []
    for elem in arr:
        heap_push(ans, elem, key=rkey)
        if len(ans) > k:
            heap_pop(ans, key=rkey)
            ans.pop()

    return ans

# END top k
