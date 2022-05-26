import copy
import time
import numpy as np

epsilon = 10 ** (-2)


def create_economic(file):
    with open(file) as fd:
        lines = fd.readlines()

    n = int(lines[0])
    m = [[] for _ in range(n)]

    for line in range(2, len(lines) - 1):
        collected = lines[line].split(',')
        value = float(collected[0])
        i = int(collected[1])
        j = int(collected[2].strip())
        insert = [value, j]
        m[i].append(insert)
    fd.close()

    for line in range(len(m)):
        sum = 0
        for col in range(len(m[line])):
            if line == m[line][col][1]:
                sum += m[line][col][0]
        for col in range(len(m[line])):
            if line == m[line][col][1]:
                m[line][col][0] = sum
    return m


def restructure_economic(a):
    new_a = [[] for _ in range(len(a))]
    start = time.time()
    for line in range(len(a)):
        for val_col in range(len(a[line])):
            col_matrix = a[line][val_col][1]
            value = a[line][val_col][0]
            new_a[line].append([value, col_matrix])
            if col_matrix != line:
                new_a[col_matrix].append([value, line])
    end = time.time()
    print("Restructurarea matricei economice: ", end - start)
    return new_a


def create_free(file):
    with open(file) as fd:
        m = fd.readlines()
    m = m[:-1]
    fd.close()
    for index in range(len(m)):
        m[index] = float(m[index].strip())
    return m


a1 = create_economic('a_1.txt')
a2 = create_economic('a_2.txt')
a3 = create_economic('a_3.txt')
a4 = create_economic('a_4.txt')
a5 = create_economic('a_5.txt')
b1 = create_free('b_1.txt')
b2 = create_free('b_2.txt')
b3 = create_free('b_3.txt')
b4 = create_free('b_4.txt')
b5 = create_free('b_5.txt')

a_test = create_economic('a_test.txt')
b_test = create_free('b_test.txt')


def jacobi_ab(a, b):
    x_c = [0 for i in range(len(a))]
    k = 0
    diagonal = [0 for i in range(len(a))]
    if len(a) != len(b):
        print("Matricea si vectorul liber nu sunt de aceeasi lungime.\n")
        exit()

    start = time.time()
    new_a = restructure_economic(a)

    while True:
        x_p = copy.deepcopy(x_c)
        for line in range(len(new_a)):
            s = b[line]
            for val_col in range(len(new_a[line])):
                col_matrix = new_a[line][val_col][1]
                value = new_a[line][val_col][0]
                if col_matrix == line:
                    diagonal[line] = value
                else:
                    s = s - x_p[col_matrix] * value

            # b[line] = b[line] / diagonal[line]
            x_c[line] = s / diagonal[line]

        delta = np.linalg.norm(np.array(x_c) - np.array(x_p))
        print("k =", k, ": delta =", delta)
        k += 1
        if delta < epsilon or delta > 10 ** 8 or k > 10000:
            break

    end = time.time()
    print("Timpul de rulare: ", end - start)
    print("Valori:", x_c[:10])

    if delta < epsilon:
        return x_c
    else:
        print("divergenta")


def verify_solution(a, jacobi, b):
    new_solution = [0 for _ in range(len(a))]
    new_a = restructure_economic(a)
    for line in range(len(new_a)):
        for val_col in range(len(new_a[line])):
            col_matrix = new_a[line][val_col][1]
            value = new_a[line][val_col][0]
            new_solution[line] += value * jacobi[col_matrix]
    # new_solution[index].append([new_value, index])

    new_new_solution = np.linalg.norm(np.array(new_solution) - np.array(b), np.inf)

    print("Norma obtinuta:", new_new_solution)


print("---matricea de test---")
jacobi_testing = jacobi_ab(a_test, b_test)

print("---matricea 1---")
jacobi_1 = jacobi_ab(a1, b1)
verify_solution(a1, jacobi_1, b1)

print("---matricea 2---")
jacobi_2 = jacobi_ab(a2, b2)
verify_solution(a2, jacobi_2, b2)

print("---matricea 3---")
jacobi_3 = jacobi_ab(a3, b3)
verify_solution(a3, jacobi_3, b3)

print("---matricea 4---")
jacobi_4 = jacobi_ab(a4, b4)
verify_solution(a4, jacobi_4, b4)

print("---matricea 5---")
jacobi_5 = jacobi_ab(a5, b5)
# verify_solution(a5, jacobi_5, b5)

print("end")
