# -*- coding: utf-8 -*-
class It:
    def __init__(self, n):
        self.name = n
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.g = 0
        self.h = 0
        self.i = 0
        self.j = 0
        self.k = 0
        self.l = 0
        self.m = 0
        self.n = 0
        self.o = 0
        self.p = 0
        self.q = 0
        self.r = 0
        self.s = 0
        self.t = 0
        self.u = 0
        self.v = 0
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def get_v(self):
        return self.v

    def set_v(self, v1):
        self.v = v1


def add_num(self, p):
    if p == 'a':
        self.a += 1
    if p == 'b':
        self.b += 1
    if p == 'c':
        self.c += 1
    if p == 'd':
        self.d += 1
    if p == 'e':
        self.e += 1
    if p == 'f':
        self.f += 1
    if p == 'g':
        self.g += 1
    if p == 'h':
        self.h += 1
    if p == 'i':
        self.i += 1
    if p == 'j':
        self.j += 1
    if p == 'k':
        self.k += 1
    if p == 'l':
        self.l += 1
    if p == 'm':
        self.m += 1
    if p == 'n':
        self.n += 1
    if p == 'o':
        self.o += 1
    if p == 'p':
        self.p += 1
    if p == 'q':
        self.q += 1
    if p == 'r':
        self.r += 1
    if p == 's':
        self.s += 1
    if p == 't':
        self.t += 1
    if p == 'u':
        self.u += 1
    if p == 'v':
        self.v += 1
    if p == 'w':
        self.w += 1
    if p == 'x':
        self.x += 1
    if p == 'y':
        self.y += 1
    if p == 'z':
        self.z += 1


with open('PeopleDaily_Clean.txt', 'r+', encoding='utf-8') as fr:
    all_word = fr.read().split()
    word = []
    pos = []
    for i in all_word:
        word.append(i.split('/')[0])
        pos.append(i.split('/')[1])

# 发射矩阵
search = [0 for i in range(len(word))]
good_word = []
print(len(word))
for i in range(len(word)):
    if search[i] == 0:
        search[i] = 1
        w = It(word[i])
        add_num(w, pos[i])
        location = [loc for loc, x in enumerate(word) if x == word[i]]
        for j in location:
            if search[j] == 0:
                search[j] = 1
                add_num(w, pos[j])
        good_word.append(w)
        print(i)

with open('B.txt', 'w+', encoding='gbk') as fw:
    for i in good_word:
        restore = [i.name, str(i.a), str(i.b), str(i.c), str(i.d), str(i.e), str(i.f), str(i.g), str(i.h), str(i.i), str(i.j), str(i.k), str(i.l), str(i.m), str(i.n), str(i.o), str(i.p), str(i.q), str(i.r),
                   str(i.s), str(i.t), str(i.u), str(i.v), str(i.w), str(i.x), str(i.y), str(i.z)]
        fw.writelines(','.join(restore))
        fw.write('\n')
