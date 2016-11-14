from time import perf_counter

from algo.tests.utils import gen_case, get_func_name
from algo.heap import *


def test_heap_make():
    t1 = perf_counter()
    for seq in gen_case(7):
        copy = seq.copy()
        heap_make(copy)
        assert heap_verify(copy)

    duration = perf_counter() - t1
    print('heap_make() passed test in', duration, 's')


def test_heap_push():
    t1 = perf_counter()
    for seq in gen_case(7):
        if len(seq) == 0:
            continue

        heap = seq.copy()
        heap_make(heap)

        to_push = list(range(heap[0] + 1))
        to_push.extend([ (n + 0.5) for n in to_push ])
        to_push.append(-1)

        for n in to_push:
            testbed = heap.copy()
            heap_push(testbed, n)
            assert heap_verify(testbed)

    duration = perf_counter() - t1
    print('heap_push() passed test in', duration, 's')


def test_heap_pop():
    t1 = perf_counter()
    for seq in gen_case(7):
        if len(seq) == 0:
            continue

        heap = seq.copy()
        heap_make(heap)
        heap_pop(heap)
        heap.pop()
        assert heap_verify(heap)

    duration = perf_counter() - t1
    print('heap_pop() passed test in', duration, 's')


def test_topk():
    for topk in (topk_by_bigheap, topk_by_smallheap):
        t1 = perf_counter()
        for seq in gen_case(7):
            sorted_input = sorted(seq)
            for k in range(len(seq)):
                copy = seq.copy()
                kseq = topk(copy, k)
                assert sorted(kseq) == sorted_input[len(seq) - k:], \
                    'topk({copy}, {k}) -> {kseq}'.format_map(vars())

        duration = perf_counter() - t1
        print(get_func_name(topk), 'passed test in', duration, 's')


if __name__ == '__main__':
    test_heap_make()
    test_heap_push()
    test_heap_pop()
    test_topk()
