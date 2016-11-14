
# BEGIN bisect

# def bisect_find_naive(arr, elem, key=None):
#     if len(arr) == 0:
#         return None
#
#     key = key or (lambda x: x)
#     elem = key(elem)
#
#     left, right = 0, len(arr) - 1
#     while left + 1 < right:
#         mid = (left + right) // 2
#         if key(arr[mid]) < elem:
#             left = mid
#         elif key(arr[mid]) > elem:
#             right = mid
#         else:
#             return mid
#
#     if key(arr[left]) == elem:
#         return left
#     elif key(arr[right]) == elem:
#         return right
#     else:
#         return None


def bisect_find(arr, elem, key=None):
    key = key or (lambda x: x)
    elem = key(elem)

    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if key(arr[mid]) < elem:
            left = mid + 1
        elif key(arr[mid]) > elem:
            right = mid - 1
        else:
            return mid
    else:
        return None

# END bisect
