import statistics

from algo.tests.test_select import all_select_funcs
from algo.tests.utils import gen_special_sort_case, get_func_name, timed_test, print_matrix


def test_nth_small_perf():
    matrix = []
    cases = gen_special_sort_case(2000)

    for entry in all_select_funcs:
        func = entry['func']
        func_name = entry.get('name', get_func_name(func))
        if entry.get('is_random', False):
            times = 10
        else:
            times = 2

        matrix.append([func_name, []])
        print('BEGIN', func_name)

        for case, arr in cases.items():
            durations = []
            for n in range(times):
                desc = '{func_name}(_{case}_) #{n}'.format_map(locals())
                with timed_test(desc, 'performance') as get_duration:
                    func(arr.copy(), len(arr) // 3)
                durations.append(get_duration())

            matrix[-1][1].append((case, statistics.mean(durations)))

        print('END', func_name)
        print()

    print_matrix(matrix)
