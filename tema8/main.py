import random
import numpy as np

epsilon = 10 ** (-6)
h = 10 ** (-5)

c1 = [1 / 3, -2, 2, 3]
c3 = [1, -6, 13, -12, 4]
c4 = [1, -6, 11, 6]

# def f1(x): return 1 / 3 * (x ** 3) - 2 * (x ** 2) + 2 * x + 3
#
#
# def f2(x): return x ** 2 + math.sin(x)
#
#
# # def f2d1(x): return 2 * x + math.cos(x)
# #
# #
# # def f2d2(x): return 2 - math.sin(x)
#
#
# def g1(x, type_f): return (3 * f(type_f, x) - 4 * f(type_f, x - h) + f(type_f, x - 2 * h)) / 2 * h
#
#
# def g2(x, type_f): return (-f(type_f, x + 2 * h) + 8 * f(type_f, x + h) - 8 * f(type_f, x - h) + f(type_f, x - 2 * h)) / 12 * h
#
#
# def fsd(x, type_f): return (-f(type_f, x + 2 * h) + 16 * f(type_f, x + h) - 30 * f(type_f, x) + 16 * f(type_f, x - h) - f(type_f, x - 2 * h)) / 12 * (h**2)
#
#
# def f3(x): return x ** 4 - 6 * (x ** 3) + 13 * (x ** 2) - 12 * x + 4
#
#
# x1 = 2 + math.sqrt(2)
# x2 = -0.4501836112948
# x3 = random.randint(1, 3)
#
#
# p1 = np.poly1d(c1)
# p3 = np.poly1d(c3)
#
# p1d1 = np.polyder(p1, 1)
# p3d1 = np.polyder(p3, 1)
#
# pc1 = p1d1.r
# pc3 = p3d1.r
#
# p1d2 = np.polyder(p1, 2)
# p3d2 = np.polyder(p3, 2)
#
# pm1 = p1d2.r
# pm3 = p3d2.r

# pm = []
# for i in pm1:
#     pm.append(i) if i > 0 else True


# def f(type, x):
#     if type == 1:
#         return f1(x)
#     elif type == 2:
#         return f2(x)
#     elif type == 3:
#         return f3(x)
#     else:
#         return 0


c = c4
# f_type = 1

polynom = np.poly1d(c)
rad = []
for i in np.roots(c):
    rad.append(np.round(i, 8))

R = (abs(c[0]) + max(c)) / abs(c[0])

print("Radacinile functiei:", rad)

pd = np.polyder(polynom)

pc = pd.r
print("Punctele critice ale functiei:", pc)

pds = np.polyder(polynom, 2)
pmin = []
for i in pc:
    xs = pds(i)
    pmin.append(xs) if xs > 0 else False
print("Punctele minime ale functiei:", pmin)


def steff(x0):
    x = [x0]
    k = 0
    fk = pd(x[k])
    fk_plus = pd(x[k] + fk)
    delta_x = (fk ** 2) / (fk_plus - fk)
    x.append(x[k] - delta_x)
    k += 1

    while epsilon <= abs(delta_x) <= 10 ** 8 and k <= 100:
        if abs(fk_plus - fk) <= epsilon:
            print("\nsir convergent")
            isdiv = False
            return x, isdiv
        fk = pd(x[k])
        fk_plus = pd(x[k] + fk)
        delta_x = (fk ** 2) / (fk_plus - fk)
        x.append(x[k] - delta_x)
        k += 1

    if abs(delta_x) < epsilon:
        print("sir convergent\n")
        isdiv = False
    else:
        print("sir divergent\n")
        isdiv = True

    return x, isdiv


with open("output.txt", "w") as fd:
    for i in range(10):
        x0 = random.uniform(-R, R)
        while x0 in rad:
            x0 = random.uniform(-R, R)
        print("Incepem cu x0=", x0)
        xl, isdiv = steff(x0)
        fd.write("\nx0 =" + str(x0) + "\n")
        fd.write(str(xl[0]) + "\n")
        for i in range(len(xl) - 1):
            if abs(xl[i] - xl[i + 1]) > epsilon:
                fd.write(str(xl[i + 1]) + "\n")
        fd.write("sir divergent\n") if isdiv is True else fd.write("sir convergent\n")
