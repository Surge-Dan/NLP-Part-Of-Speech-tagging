# -*- coding: utf-8 -*-
trans_list = {}
alphabet = []

for i in range(97, 123):  # 利用ASCII码将26个英文字母放入列表alphabet中
    alphabet.append(chr(i))

with open('PeopleDaily_Clean.txt', 'r+', encoding='utf-8') as fr:
    for line in fr.readlines():
        word = line.strip().split()
        for i in range(len(word) - 1):
            cur_pos = word[i].split('/')[1]
            next_pos = word[i + 1].split('/')[1]
            if cur_pos in trans_list:
                if next_pos in trans_list[cur_pos]:
                    trans_list[cur_pos][next_pos] += 1
                else:
                    trans_list[cur_pos][next_pos] = 1
            else:
                trans_list[cur_pos] = {next_pos: 1}


with open('A.txt', 'w+', encoding='utf-8') as fw:
    fw.write(' ,')
    fw.write(','.join(alphabet))
    fw.write('\n')
    for i in alphabet:
        if i in trans_list.keys():
            fw.write(i + ',')
            w = []
            for j in alphabet:
                if j in trans_list[i].keys():
                    w.append(trans_list[i][j])
                else:
                    w.append(1)
            print(w)
            w_new = [str(x) for x in w]
            fw.write(','.join(w_new).strip('['']'))
            fw.write('\n')
        else:
            fw.write(i + ',')
            fw.write(','.join(str(1) for i in range(26)))
            fw.write('\n')
