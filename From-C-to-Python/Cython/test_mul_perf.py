from itertools import tee
from random import choices
from time import monotonic
from multiply import mul


def mul_python(a, b):
    b_iter = tee(zip(*b), len(a))
    return [
        [
            sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
            for col_b in b_iter[i]
        ] for i, row_a in enumerate(a)
    ]


def create_random_matrix(rows, collumns):
    return [choices(range(0, 1000), k=collumns) for _ in range(rows)]


def test(first, second):
    print(f'TEST Matrix[{len(first)},{len(second)}]')
    first = create_random_matrix(1, 1)
    second = create_random_matrix(1, 1)
    start = monotonic()
    mul_python(first, second)
    finish = monotonic()
    print(f'Speed Python function: {finish - start} seconds')
    start = monotonic()
    mul(first, second)
    finish = monotonic()
    print(f'Speed Cython function: {finish - start} seconds')


if __name__ == '__main__':
    test(create_random_matrix(3, 3), create_random_matrix(3, 3))
    test(create_random_matrix(5, 5), create_random_matrix(5, 5))
    test(create_random_matrix(10, 10), create_random_matrix(10, 10))
    test(create_random_matrix(50, 50), create_random_matrix(50, 50))
    test(create_random_matrix(100, 100), create_random_matrix(100, 100))
