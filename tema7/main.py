import math
import random

import numpy as np

epsilon = 10 ** (-6)
c1 = [1, -6, 11, -6]
c2 = [42, -55, -42, 49, -6]
c3 = [8, -38, 49, -22, 3]
c4 = [1, -6, 13, -12, 4]


def horner(c, x):
    c = c[::-1]
    r = 0
    for i in range(len(c)):
        r += c[i] * (x ** i)
    return r


c = c1

polynom = np.poly1d(c)
print("Testing polynom...", polynom(0.5))
print("Testing using Horner...", horner(c, 0.5))
print("Radacinile polinomului:", polynom.roots)

rad = []
for i in np.roots(c):
    rad.append(round(i, 8))

# r = min(polynom.r)
# R = max(polynom.r)
#
# print("\nAvem intervalul [", r, R, "]")

R = (abs(c[0]) + abs(max(c))) / abs(c[0])

print("\nAvem intervalul [", -R, R, "]\n")


def ghan(x0):
    x = []
    k = 0
    x.append(x0)

    print("----- k = {:d} -----".format(k))
    hx = horner(c, x[k])
    print("P(x_k) =", hx)
    hx_plus = horner(c, x[k] + hx)
    print("P(x_k + P(x_k)) =", hx_plus)
    hx_minus = horner(c, x[k] - hx)
    print("P(x_k - P(x_k)) =", hx_minus)

    y = x[k] - (2 * (hx ** 2) / (hx_plus - hx_minus))
    hy = horner(c, y)
    print("P(y) =", hy)
    print("\n")
    delta_x = 2 * hx * (hx + hy) / (hx_plus - hx_minus)
    x.append(x[k] - delta_x)
    k += 1

    while epsilon <= abs(delta_x) <= 10 ** 8 and k <= 100:
        print("----- k = {:d} -----".format(k))
        if abs(hx) <= epsilon / 10:
            delta_x = 0
        else:
            hx = horner(c, x[k])
            hx_plus = horner(c, x[k] + hx)
            hx_minus = horner(c, x[k] - hx)

            y = x[k] - (2 * (hx ** 2) / (hx_plus - hx_minus))
            hy = horner(c, y)
            delta_x = 2 * hx * (hx + hy) / (hx_plus - hx_minus)

        print("P(x_k) =", hx)
        print("P(x_k + P(x_k)) =", hx_plus)
        print("P(x_k - P(x_k)) =", hx_minus)
        print("P(y) =", hy)
        print("")
        x.append(x[k] - delta_x)
        k += 1

    if abs(delta_x) < epsilon:
        print('sir convergent')
        isdiv = False
    else:
        print('sir divergent')
        isdiv = True

    return x, isdiv


with open("output.txt", 'w') as fd:
    for i in range(10):
        x0 = random.uniform(-R, R)
        while x0 in rad:
            x0 = random.uniform(-R, R)
        print("Incepem cu x0 =", x0)
        xl, isdiv = ghan(x0)
        fd.write("\nx0 =" + str(x0) + "\n")
        fd.write(str(xl[0]) + "\n")
        for i in range(len(xl) - 1):
            if abs(xl[i] - xl[i + 1]) > epsilon:
                fd.write(str(xl[i + 1]) + "\n")
        fd.write("sir divergent\n") if isdiv is True else fd.write("sir convergent\n")
