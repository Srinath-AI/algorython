from collections import defaultdict
from functools import reduce
import statistics
import random

from algo.tests.utils import gen_special_sort_case, timed_test, print_matrix, print_histogram
from algo.tests.tree.test_tree import all_trees


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


def get_percentage_dist(dists):
    collected = dict()
    for depth_count in dists:
        collected.update(depth_count)

    count = sum(c for d, c in collected.items())
    for d, c in collected.items():
        collected[d] /= count

    return collected


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
                with timed_test(
                        '{tree_name}, _{case_name}_, #{n}'.format_map(vars()),
                        'performance') as get_duration:
                    for x in arr:
                        tree.insert(x)
                durations.append(get_duration())
            matrix[-1][1].append((case_name, statistics.mean(durations)))
        print()

    print_matrix(matrix)


def test_remove():
    rand_case = gen_special_sort_case(2000)['rand']

    sorted_case = sorted(rand_case)
    shuffled_case = rand_case.copy()
    random.shuffle(shuffled_case)

    remove_orders = dict(
        ascending=sorted_case,
        descending=list(reversed(sorted_case)),
        origin=rand_case,
        random=shuffled_case
    )

    matrix = []
    for entry in all_trees:
        tree_type = entry['tree']
        tree_name = tree_type.__name__
        if entry.get('is_random', False):
            times = 5
        else:
            times = 3
        matrix.append([tree_name, []])

        tree = tree_type()
        for x in rand_case:
            tree.insert(x)

        for case_name, arr in remove_orders.items():
            durations = []
            for n in range(times):
                test_tree = tree.deepcopy()
                with timed_test(
                        '{tree_name}, {case_name}, #{n}'.format_map(vars()),
                        'performance') as get_duration:
                    for x in arr:
                        test_tree.remove(x)
                assert test_tree.root is None
                durations.append(get_duration())
            matrix[-1][1].append((case_name, statistics.mean(durations)))
        print()

    print_matrix(matrix)


def test_depth_distribution_by_insert():
    cases = gen_special_sort_case(2000)

    for entry in all_trees:
        tree_type = entry['tree']
        tree_name = tree_type.__name__
        if entry.get('is_random', False):
            times = 5
        else:
            times = 3

        for case_name, arr in cases.items():
            dists = []
            for n in range(times):
                tree = tree_type()
                for x in arr:
                    tree.insert(x)

                dists.append(measure_nil_depth(tree))

            stats = list(map(get_stats_from_nil_depth, dists))
            mean_stats = average_depth_stats(stats)
            dist = get_percentage_dist(dists)
            print(tree_name, case_name, mean_stats)

            min_depth, max_depth = min(dist.keys()), max(dist.keys())
            for d in range(min_depth, max_depth + 1):
                if d not in dist:
                    dist[d] = 0

            pairs = list(dist.items())
            pairs.sort(key=lambda p: p[0])

            print_histogram(pairs)
            print()
