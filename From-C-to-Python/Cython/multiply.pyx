from itertools import tee

def mul(a, b):
    if len(a) > 100 or len(b) > 100 or len(a) < 0 or len(b) < 0:
        raise ValueError('Matrix more than 100/less than 0')
    if len(a[0]) != len(b):
        raise ValueError('rows of first not equal cols of second!')
    if False not in [isinstance(i, int) for i in a] and False not in [isinstance(i, int) for i in b]:
        raise ValueError('Values must be integers!')
    b_iter = tee(zip(*b), len(a))
    return [
        [
            sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
            for col_b in b_iter[i]
        ] for i, row_a in enumerate(a)
    ]
