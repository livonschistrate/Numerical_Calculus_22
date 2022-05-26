import copy
import random
import numpy as np
import examples

epsilon = 10 ** (-6)


def generate_rand(n, p):
    a = []
    row = []
    for line in range(n):
        for col in range(p):
            row.append(random.randrange(0, 20))
        a.append(row)
        row = []

    return a


def generate_lambda(n, a):
    lamda = [[0]*n for _ in range(n)]
    for i in range(n):
        lamda[i][i] = a[i][i]
    return lamda


def max_value_index(n, a):
    maximum, p_max, q_max = 0, 0, 0
    for i in range(n):
        for j in range(n):
            if i != j and abs(a[i][j]) > maximum:
                maximum = abs(a[i][j])
                p_max, q_max = i, j
    return p_max, q_max


def max_value_theta(p, q, a):
    alpha = (a[p][p] - a[q][q]) / (2 * a[p][q])
    if alpha >= 0:
        t = -alpha + ((alpha ** 2) + 1) ** (1 / 2)
    else:
        t = -alpha - ((alpha ** 2) + 1) ** (1 / 2)
    c = 1 / ((1 + (t ** 2)) ** (1 / 2))
    s = t / ((1 + (t ** 2)) ** (1 / 2))

    return c, s, t


def check_diagonal_matrix(n, a):
    for i in range(n):
        for j in range(n):
            if i != j and a[i][j] != 0:
                return False
    return True


def calculate_b(n, p, q, c, s, t, a):
    b = [[0 for _ in range(n)] for _ in range(n)]
    b = copy.deepcopy(a)
    for j in range(n):
        if j != p and j != q:
            b[p][j] = b[j][p] = c * a[p][j] + s * a[q][j]
            b[q][j] = b[j][q] = -s * a[p][j] + c * a[q][j]
    b[p][p] = a[p][p] + t * a[p][q]
    b[q][q] = a[q][q] - t * a[p][q]
    b[p][q] = b[q][p] = 0
    return b


def calculate_u(n, p, q, c, s, u):
    v = [[0 for _ in range(n)] for _ in range(n)]
    v = copy.deepcopy(u)
    for i in range(n):
        v[i][p] = c * u[i][p] + s * u[i][q]
        v[i][q] = -s * u[i][p] + c * u[i][q]
    return v


def calculate_r(n, p, q, c, s):
    r = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j and i != p and i != q:
                r[i][j] = 1
            elif i == j and (i == p or i == q):
                r[i][j] = c
            elif i == p and j == q:
                r[i][j] = s
            elif i == q and j == p:
                r[i][j] = -s
            else:
                r[i][j] = 0
    return np.array(r)


def jacobi(n, a):
    k = 0
    # a = np.array(a)
    u = np.identity(n)
    p_max, q_max = max_value_index(n, a)
    c, s, t = max_value_theta(p_max, q_max, a)

    while abs(a[p_max][q_max]) > epsilon and k <= 1000:
        a = calculate_b(n, p_max, q_max, c, s, t, a)
        u = calculate_u(n, p_max, q_max, c, s, u)
        p_max, q_max = max_value_index(n, a)
        if abs(a[p_max][q_max]) > epsilon:
            c, s, t = max_value_theta(p_max, q_max, a)
            k += 1

    print("Functia Jacobi implementata are", k, "iteratii.")
    return a, u


def jacobi2(n, a):
    k = 0
    # a = np.array(a)
    u = np.identity(n)
    p_max, q_max = max_value_index(n, a)
    c, s, t = max_value_theta(p_max, q_max, a)

    while abs(a[p_max][q_max]) > epsilon and k <= 1000:
        r = calculate_r(n, p_max, q_max, c, s)
        a = np.dot(np.dot(r, a), np.transpose(r))
        u = np.dot(u, np.transpose(r))
        p_max, q_max = max_value_index(n, a)
        if abs(a[p_max][q_max]) > epsilon:
            c, s, t = max_value_theta(p_max, q_max, a)
        k += 1

    print("Functia Jacobi implementata are", k, "iteratii.")
    return a, u


aj_1, uj_1 = jacobi(len(examples.a1), examples.a1)
aj2_1, uj2_1 = jacobi2(len(examples.a1), examples.a1)
ul_1, al_1 = np.linalg.eig(examples.a1)

afinal_1 = np.dot(np.dot(np.transpose(uj_1), examples.a1), uj_1)
afinal2_1 = np.dot(np.dot(np.transpose(uj2_1), examples.a1), uj2_1)


print("Functia implementata:")
print(aj_1)
print(uj_1)
print('\n')
print(aj2_1)
print(uj2_1)
print("\nBiblioteca np.linalg.eig:")
print(al_1)
print(ul_1)
print("\nMatrici finale:")
print(afinal_1)
print(afinal2_1)
print("\nNorme obtinute:")
print(np.linalg.norm(np.dot(examples.a1, uj_1) - np.dot(uj_1, aj_1)))
print(np.linalg.norm(np.dot(examples.a1, uj2_1) - np.dot(uj2_1, aj2_1)))


print('\n')
a_randj = generate_rand(6, 6)
ar1, ur1 = jacobi(6, a_randj)
ar2, ur2 = jacobi2(6, a_randj)
lr1 = generate_lambda(6, a_randj)
afinal_1 = np.dot(np.dot(np.transpose(ur1), a_randj), ur1)
afinal2_1 = np.dot(np.dot(np.transpose(ur2), a_randj), ur2)

print("Functia implementata:")
print(ar1)
print(ur1)
print('\n')
print(ar2)
print(ur2)
print("\nMatrici finale:")
print(afinal_1)
print(afinal2_1)
print("\nNorme obtinute:")
print(np.linalg.norm(np.dot(a_randj, ur1) - np.dot(ur1, lr1)))
print(np.linalg.norm(np.dot(a_randj, ur2) - np.dot(ur2, lr1)))


def svd(p, n, a):
    u, s, v = np.linalg.svd(a)
    print("Valorile singulare:", s)

    rang, min_sing, max_sing = 0, np.inf, 0
    for i in range(len(s)):
        if s[i] > 0:
            rang += 1
            if s[i] < min_sing:
                min_sing = s[i]
            if s[i] > max_sing:
                max_sing = s[i]
    print("Rang:", rang)
    print("Rang folosind biblioteca:", np.linalg.matrix_rank(a))
    print("Numarul de conditionare:", max_sing / min_sing)
    print("Numarul de conditionare folosind biblioteca:", np.linalg.cond(a))

    si = [[0 for _ in range(n)] for _ in range(p)]
    for i in range(rang):
        si[i][i] = 1 / s[i]
    a_psi = np.dot(np.dot(np.transpose(v), si), np.transpose(u))
    print("Pseudo-inversa matricei A:", a_psi)
    print("Pseudo-inversa folosind biblioteca:", np.linalg.pinv(a))

    a_tr = np.transpose(a)
    inm = np.dot(a_tr, a)
    inmv = np.linalg.inv(np.array(inm))
    a_sq = np.dot(inmv, a_tr)
    print("Pseudo-inversa in sensul celor mai mici patrate:", a_sq)
    # a_sq_b = np.dot(np.linalg.inv(np.dot(np.linalg.pinv(a), a)), np.linalg.pinv(a))
    # print("Pseudo-inversa in sensul celor mai mici patrate fol. biblioteca:", a_sq_b)

    norm_pinv = np.linalg.norm(a_psi - a_sq)
    # norm_pinv_b = np.linalg.norm(np.linalg.pinv(a) - a_sq_b)
    print("Norma obtinuta:", norm_pinv)
    # print("Norma obtinuta din biblioteca:", norm_pinv_b)


# svd(len(examples.a4[0]), len(examples.a4), examples.a4)

a_rand = generate_rand(5, 6)
svd(6, 5, a_rand)
