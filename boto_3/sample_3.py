def square(list_1):
    sq = list(zip(list_1, list(map(lambda x: x**2, list_1))))
    return sq


num = [1, 2, 3, 4, 5]
z = zip(*square(num))
for i in z:
    for j in i:
        print(j)