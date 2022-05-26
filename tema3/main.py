import numpy as np

epsilon = 10 ** (-6)


def create_matrix(file):
    with open(file) as fd:
        lines = fd.readlines()

    m = np.zeros((int(lines[0]), int(lines[0])))

    for line in range(2, len(lines) - 1):
        collected = lines[line].split(',')
        value = float(collected[0])
        i = int(collected[1])
        j = int(collected[2].strip())
        m[i][j] = m[j][i] = value
    fd.close()
    return m


testing = create_matrix('a_test.txt')
a = create_matrix('a.txt')
b = create_matrix('b.txt')
a_plus_b = create_matrix('a_plus_b.txt')
a_ori_a = create_matrix('a_ori_a.txt')


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


econ_testing = create_economic('a_test.txt')
econ_a = create_economic('a.txt')
econ_b = create_economic('b.txt')
econ_a_plus_b = create_economic('a_plus_b.txt')
econ_a_ori_a = create_economic('a_ori_a.txt')


def __econ_a_plus_b__(a, b):
    c = [[] for _ in range(len(a))]
    for line in range(len(c)):
        a_line = a[line]
        b_line = b[line]
        if line == 0:
            a_line_col = a_line[line]
            b_line_col = b_line[line]
            sum = a_line_col[0] + b_line_col[0]
            c[line].append([sum, line])
            continue
        a_checked = []
        for index in range(0, len(a_line)):
            sum_of_ab = a_line + b_line
            sum = 0
            a_line_col = a_line[index]
            for index_b in range(0, len(b_line)):
                if a_line_col[1] == b_line[index_b][1] and (a_line_col[0] != 0 and b_line[index_b][0] != 0):
                    sum = a_line_col[0] + b_line[index_b][0]
                    break
            if sum != 0:
                c[line].append([sum, a_line_col[1]])
                a_checked.append(a_line_col[1])
            else:
                c[line].append(a_line_col)
                a_checked.append(a_line_col[1])
        for index_b in range(0, len(b_line)):
            if b_line[index_b][1] not in a_checked:
                c[line].append(b_line[index_b])
        for index_a in range(0, len(a_line)):
            if a_line[index_a][1] not in a_checked:
                c[line].append(a_line[index_a])
    return c


econ_c = __econ_a_plus_b__(econ_a, econ_b)
# print(econ_c)

sum_is_okay = True
for line in range(len(econ_c)):
    c_line = econ_c[line]
    ab_line = econ_a_plus_b[line]
    for index_c in range(len(c_line)):
        for index_ab in range(len(ab_line)):
            if c_line[index_c][1] == ab_line[index_ab][1] and abs(c_line[index_c][0] - ab_line[index_ab][0]) > epsilon:
                print("Suma matricelor nu rezulta cea din fisier: ", line, index_c)
                sum_is_okay = False
                break

print("Suma obtinuta e acceasi cu cea din fisier? ->", sum_is_okay)


def __econ_a_ori_a__(a):
    c = [[] for _ in range(len(a))]
    full_matrix = []
    line_power = []

    for line in a:
        found = False
        for col in line:
             if col[1] == 0:
                line_power.append(col[0])
                found = True
                break
        if not found:
            line_power.append(0)
    full_matrix.append(line_power)

    for line in range(len(a)):
        a_line = a[line]
        to_multiply = []
        if line == 0:
            for next_line in a:
                for index in next_line:
                    if a_line[line][1] == index[1]:
                        to_multiply.append(index[0])
                        break
            arr_power = []
            for number in to_multiply:
                arr_power.append(number * number)
            c[line].append([sum(arr_power), line])
            continue
        a_checked = []
        to_multiply = []
        # for i in range(len(a)):
        #     line2 = a[i]
        #     found = False
        #     for col in line2:
        #         if col[1] == line:
        #             to_multiply.append(col[0])
        #             found = True
        #             break
        #     if not found:
        #         to_multiply.append(0)
        saved_lines = []
        saved_lines = [[] for _ in range(line+1)]

        # for index_a in range(0, len(a_line)):
        #     sum_of_aa = a_line + a_line
        #     sum_el = 0
        #     # to_multiply.append(a[line][index][0])
        #     saved_lines[line].append(a[line][index_a][0])
        #     a_line_col = a_line[index_a]
        #     to_multiply = []
        #     index_line = a_line_col[1]

        for index_b in range(0, len(a)):
            found = []
            cc = index_b
            i2 = a[index_b]
            for index_c in i2:
                i3 = index_c
                if index_c[1] <= line:
                    saved_lines[index_c[1]].append(index_c[0])
                    found.append(index_c[1])
            for index_d in range(0, line+1):
                if index_d not in found:
                    saved_lines[index_d].append(0)

        for col in a_line:
            saved_lines[line][col[1]] = col[0]
        line_power = saved_lines[line]

        full_matrix.append(line_power)

        for saved_line in range(len(full_matrix)):
            arr_power = []
            for number1, number2 in zip(full_matrix[saved_line], line_power):
                arr_power.append(number1 * number2)
            c[line].append([sum(arr_power), saved_line])

        #     for index_b in range(0, len(a)):
        #         found = False
        #         cc = index_b
        #         i1 = a_line_col
        #         i2 = a[index_b]
        #         for index_c in range(0, len(a[index_b])):
        #             i3 = a[index_b][index_c]
        #             if a_line_col[1] == a[index_b][index_c][1]:
        #                 to_multiply.append(a[index_b][index_c][0])
        #                 found = True
        #                 break
        #         if not found:
        #             to_multiply.append(0)
        #
        #     if a_line[index_a][1] == line:
        #         line_power = to_multiply
        #         arr_power = []
        #         for number1, number2 in zip(to_multiply, line_power):
        #             arr_power.append(number1 * number2)
        #         c[line].append([sum(arr_power), a_line[index_a][1]])
        #     else:
        #         saved_lines.append(to_multiply)
        #
        # for index_a in range(0, len(a_line)):
        #     to_multiply2 = []
        #     if index_a not in a_checked:
        #         for index_b in range(0, len(a)):
        #             found = False
        #             cc = index_b
        #             i1 = a_line[index_a]
        #             i2 = a[index_b]
        #             for index_c in range(0, len(a[index_b])):
        #                 i3 = a[index_b][index_c]
        #                 if index_a == a[index_b][index_c][1]:
        #                     to_multiply2.append(a[index_b][index_c][0])
        #                     found = True
        #                     break
        #             if not found:
        #                 to_multiply2.append(0)
        #     arr_power = []
        #     for number1, number2 in zip(line_power, to_multiply2):
        #         arr_power.append(number1 * number2)
        #     c[line].append([sum(arr_power), a_line[index_a][1]])

        # for index in range(0, len(a)):
        #     line1 = a[index]
        #     for index_n in range(len(line1)):
        #         if a_line[index][1] == line1[index_n][1]:
        #             to_multiply.append(index_n[0])
        #             break
        #
        # if a_line[index][1] == line:
        #     line_power = to_multiply
        # arr_power = []
        # for number1, number2 in zip(to_multiply, line_power):
        #     arr_power.append(number1 * number2)
        # c[line].append([sum(arr_power), a_line[index][1]])

    for line in range(len(c)):
        for col in range(0, line):
            if c[line][col][0] == 0:
                c[line].pop(col)
    return c


econ_testing_multiply = __econ_a_ori_a__(econ_testing)
econ_d = __econ_a_ori_a__(econ_a)

prod_is_okay = True
for line in range(len(econ_d)):
    d_line = econ_c[line]
    aa_line = econ_a_ori_a[line]
    for index_d in range(len(d_line)):
        for index_aa in range(len(aa_line)):
            if d_line[index_d][1] == aa_line[index_aa][1] and abs(d_line[index_d][0] - aa_line[index_aa][0]) > epsilon:
                print("Produsul A^2 nu rezulta cea din fisier: ", line, index_d)
                prod_is_okay = False
                break

print("Produsul obtinut e acelasi cu cel din fisier? ->", prod_is_okay)
