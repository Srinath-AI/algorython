from algo.tests.test_sort import sort_funcs
from algo.tests.utils import gen_special_sort_case, get_func_name, timed_test, print_matrix


def test_sort_perf():
    matrix = []
    cases = gen_special_sort_case(2000)

    for entry in sort_funcs:
        func = entry['func']
        desc = entry.get('name', get_func_name(func))
        func_name = get_func_name(func)
        kwargs = getattr(func, 'keywords', {})
        if entry.get('skip_large', False):
            print(desc, 'skipping large testcase.')
            continue

        matrix.append([desc, []])
        print('BEGIN {}'.format(desc))

        for case, arr in cases.items():
            try:
                with timed_test('{desc}(_{case}_)'.format_map(locals()), 'performance') as get_duration:
                    func(arr.copy())
            except:
                print(desc, arr)
                raise
            else:
                matrix[-1][1].append((case, get_duration()))

        print('END {}'.format(desc))
        print()

    print_matrix(matrix)
