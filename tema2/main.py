import numpy as np
import math
import copy


def pivot_of(a, l):
    max = -math.inf
    checked = 0
    index, index_pivot = 0, -1
    for i in range(l):
        a = a[l:]
        checked += 1
    for element in a:
        if abs(element[l]) > max:
            max = abs(element[l])
            index_pivot = index
        index += 1
    return index_pivot + checked


def transpose(A):
    new_A = []
    for row in range(len(A[0])):
        new_row = []
        for col in range(len(A)):
            new_row.append(A[col][row])
        new_A.append(new_row)

    return new_A


def reverse_substitution(a, b, n):
    x = np.zeros(n)
    for i in reversed(range(n)):
        sum = 0
        for j in range(i + 1, n):
            sum += a[i][j] * x[j]
        x[i] = (b[i] - sum) / a[i][i]
    return x


# n = int(input('Dimensiunea sistemului (n): '))
epsilon = 10**(-6)  # float(input('Precizia calculelor (epsilon):'))
a = []  # np.empty([n,n],float)
b = []  # np.empty([n],float)
l_i = 0

with open('m3.txt') as f:
    lines = [[float(num) for num in line.split(' ')] for line in f]
    print(lines)

full_matrix = lines[1:]
n = int(lines[0][0])
for i in range(1, len(lines)):
    b.extend(lines[i][-1:])
    lines[i] = lines[i][:-1]
for i in range(1, len(lines)):
    a.append(lines[i])



print("Matricea A:")
print(np.asmatrix(a))
print("Vectorul b:")
print(b)
print("Matricea extinsa [A,b]:")
print(np.asmatrix(full_matrix))




while l_i < n - 1 and (full_matrix[l_i][l_i] < -epsilon or full_matrix[l_i][l_i] > epsilon):
    pivot = pivot_of(full_matrix, l_i)
    full_matrix[l_i], full_matrix[pivot] = full_matrix[pivot], full_matrix[l_i]

    for i in range(l_i + 1, n):
        f = full_matrix[i][l_i] / full_matrix[l_i][l_i]
        for j in range(l_i, n + 1):
            full_matrix[i][j] = full_matrix[i][j] - f * full_matrix[l_i][j]

    l_i += 1

print("Matricea [A,b] dupa rularea algoritmului Gauss este:")
print(np.asmatrix(full_matrix))

if -epsilon <= full_matrix[l_i][l_i] <= epsilon:
    print('Matricea data este singulara')
    exit()
else:
    print('Matricea data este nesingulara')

    f_copy = copy.deepcopy(full_matrix)
    a_g = []
    b_g = []
    for i in range(n):
        for j in range(n):
            a_g.append(f_copy[i][j])
        j += 1
        b_g.append(f_copy[i][j])

    a_g = np.reshape(a_g, (n, n))
    # x_g = np.zeros(n)

    x_g = reverse_substitution(a_g, b_g, n)

    # for i in reversed(range(n)):
    #     sum = 0
    #     for j in (range(i + 1, n)):
    #         sum += a_g[i][j] * x_g[j]
    #     x_g[i] = (b_g[i] - sum) / a_g[i][i]

    print('\nPrin metoda substitutiei inverse, obtinem:')
    print(x_g)

    c = np.dot(a_g, x_g) - b_g

    print("\nMatricea obtinuta este:")
    print(c)

    y = np.linalg.norm(c, 2)

    print("Norma euclidiana a acestei matrici este: ")
    print(y)

    x_bibl = np.linalg.solve(a_g, b_g)
    print("\nSolutia sistemului Ax=b, rezolvat de bibl. Numpy.Linalg:")
    print(x_bibl)

    a_bibl = np.linalg.inv(a)
    print("Inversa matricei A, rezolvat de bibl. Numpy.Linalg:")
    print(a_bibl)

    norm_1 = np.linalg.norm(x_g - x_bibl, 2)
    print("Prima norma:")
    print(norm_1)

    c = x_g - np.dot(a_bibl, b)
    norm_2 = np.linalg.norm(c, 2)
    print("A doua norma:")
    print(norm_2)



    # Inversa matricei A rezolvata fara a folosi libraria

    new_a = copy.deepcopy(a)
    identity = [[0 for x in range(n)] for y in range(n)]
    for i in range(0, n):
        identity[i][i] = 1
    for line in range(n):
        new_a[line].extend(identity[line])
    l_i = 0

    print("\nMatricea [A, I%2d]:" % n)
    print(np.asmatrix(new_a))

    while l_i < n - 1 and (new_a[l_i][l_i] < -epsilon or new_a[l_i][l_i] > epsilon):
        pivot = pivot_of(new_a, l_i)
        new_a[l_i], new_a[pivot] = new_a[pivot], new_a[l_i]

        for i in range(l_i + 1, n):
            f = new_a[i][l_i] / new_a[l_i][l_i]
            for j in range(l_i, len(new_a[0])):
                new_a[i][j] = new_a[i][j] - f * new_a[l_i][j]

        l_i += 1

    coef = []
    eq_list = []
    ai_g = []
    for j in range(n):
        coef.append(new_a[j][:n])
        eq_list.append(new_a[j][n:])

    eq_list = transpose(eq_list)
    x_i = 0

    for i in reversed(range(n)):
        ai_g.append(eq_list[i][n - 1] / coef[n - 1][n - 1])
        for j in reversed(coef[:n - 1]):
            sum = 0
            clist = j[::-1]
            for k in range(len(clist)):
                if k + x_i < len(ai_g):
                    sum += clist[k] * ai_g[k + x_i]
                else:
                    break
            ai_g.append((eq_list[i][n - 1 - k] - sum) / clist[k])
        x_i += n

    ai_g.reverse()

    ai_g = np.reshape(ai_g, (n, n))
    ai_g = np.transpose(ai_g)
    print("Inversa matricei A obtinuta cu alg. Gauss este:")
    print(ai_g)

    c = ai_g - a_bibl
    norm_3 = np.linalg.norm(c,1)
    print("A treia norma:")
    print(norm_3)
