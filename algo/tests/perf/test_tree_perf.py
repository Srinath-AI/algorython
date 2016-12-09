from collections import defaultdict
from functools import reduce
import statistics

from algo.tree import *
from algo.tests.utils import gen_special_sort_case, timed_test, print_matrix


all_trees = (
    dict(tree=RBTree),
    dict(tree=AVLTree),
    dict(tree=Treap, is_random=True),
    dict(tree=RSTree, is_random=True),
)


def measure_nil_depth(tree):
    def run(node, depth):
        if node is None:
            yield depth
        else:
            yield from run(node.left, depth + 1)
            yield from run(node.right, depth + 1)

    dist = defaultdict(int)
    for depth in run(tree.root, 0):
        dist[depth] += 1

    return dist


def get_stats_from_nil_depth(dist):
    sorted_dist = sorted(dist.items(), key=lambda x: x[0])

    def list_cat(a, b):
        a.extend(b)
        return a

    expanded = reduce(list_cat, ([d] * c for d, c in sorted_dist), [])
    # TODO: use MedianStream to get median
    median = statistics.median(expanded)
    min_max = expanded[0], expanded[-1]
    mean = statistics.mean(expanded)
    stdev = statistics.pstdev(expanded, mu=mean)

    return dict(median=median, min_max=min_max, mean=mean, stdev=stdev)


def average_depth_stats(stats):
    ans = dict()
    for attr in ('median', 'mean', 'stdev'):
        ans[attr] = statistics.mean(x[attr] for x in stats)
    ans['min_max'] = tuple(statistics.mean(x['min_max'][idx] for x in stats) for idx in (0, 1))

    return ans


def test_insert():
    cases = gen_special_sort_case(2000)
    matrix = []
    for entry in all_trees:
        tree_type = entry['tree']
        tree_name = tree_type.__name__
        if entry.get('is_random', False):
            times = 5
        else:
            times = 3
        matrix.append([tree_name, []])

        for case_name, arr in cases.items():
            durations = []
            for n in range(times):
                tree = tree_type()
                with timed_test('{tree_name}, _{case_name}_, #{n}'.format_map(vars()), 'performance') \
                        as get_duration:
                    for x in arr:
                        tree.insert(x)
                durations.append(get_duration())
            matrix[-1][1].append((case_name, statistics.mean(durations)))
        print()

    print_matrix(matrix)


def test_depth_distribution():
    pass
