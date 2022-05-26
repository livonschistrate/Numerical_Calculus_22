import math
import random

import numpy as np


def f1(x): return x ** 2 - 12 * x + 30


def f2(x): return math.sin(x) - math.cos(x)


def f3(x): return 2 * (x ** 3) - 3 * x + 15


def get_coord():
    n = 5
    x0, xn = 1, 5

    x = [0 for _ in range(n + 1)]
    x[0], x[n] = x0, xn
    for i in range(1, n):
        x[i] = random.uniform(x[i - 1], x[n])
        if x[i] <= x[i - 1]:
            while x[i] <= x[i - 1]:
                x[i] = random.uniform(x[i - 1], x[n])
    print("x:", x)

    y = [0 for _ in range(n + 1)]
    for i in range(n + 1):
        y[i] = f1(x[i])
    print("y:", y)

    xb = random.uniform(x[0], x[n])
    while xb in x:
        xb = random.uniform(x[0], x[n])
    print("xb:", xb)

    return n, x, y, xb


def lagrange_interpolation(n, x, y, xb):
    l = [0 for _ in range(n+1)]
    l[0] = y[0]
    diff_x = 1

    aitken = [[] for _ in range(n)]
    for i in range(n):
        aitken[0].append((y[i + 1] - y[i]) / (x[i + 1] - x[i]))
    for i in range(1, len(aitken)):
        for j in range(len(aitken[i - 1]) - 1):
            aitken[i].append((aitken[i - 1][j + 1] - aitken[i - 1][j]) / (x[j + i + 1] - x[j]))

    for i in range(1, len(l)):
        coef_calc = 0
        diff_x *= (xb - x[i - 1])
        l[i] = l[i - 1] + aitken[i-1][0] * diff_x

        # for j in range(i):
        #     to_subtract = 0
        #     for k in range(i):
        #         to_subtract += aitken[k]
        #     aitken_now = (y[i] - y[i-1])/(x[i]-x[i-1])
        #     coef_calc += ((aitken_now - to_subtract) / x[i] - x[0])
        #
        # diff_x *= (x - x_l[i-1])
        # l[i] = l[i-1] + coef_calc * diff_x

    print("l:", l)
    return l


n, x, y, xb = get_coord()
l = lagrange_interpolation(n, x, y, xb)

print("\nl_n(xb):", l[len(l) - 1])
print("|l_n(xb) - f(xb)|:", abs(l[len(l) - 1] - f1(xb)))


def horner(a_l, x):
    a_l = a_l[::-1]
    r = 0
    for i in range(len(a_l)):
        r += a_l[i] * (x ** i)
    return r


def square_interpolation(n, x, y, xb):
    a, b = x[0], x[n]
    m = 5
    B = [[0 for _ in range(m + 1)] for _ in range(m + 1)]
    f = [0 for _ in range(m + 1)]

    for i in range(m + 1):

        for j in range(m + 1):
            for k in range(n + 1):
                B[i][j] = B[i][j] + (x[k] ** (i + j))

        for k in range(n + 1):
            f[i] = f[i] + y[k] * (x[k] ** i)

    a_l = np.linalg.solve(B, f)
    a_l = a_l[::-1]
    r = horner(a_l, xb)

    return r


p = square_interpolation(n, x, y, xb)
print("\np_m(xb):", p)
print("|p_m(xb) - f(xb)|:", abs(p - f1(xb)))
abs_diff = 0

for i in range(n + 1):
    abs_diff += abs(square_interpolation(n, x, y, x[i]) - y[i])
print("sum(|p_m(x_i) - y[i]|):", abs_diff)
