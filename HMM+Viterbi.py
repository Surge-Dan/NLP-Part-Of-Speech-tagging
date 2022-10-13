# -*- coding: utf-8 -*-
import json
import math
import pandas as pd


class HMMPosTag:
    def __init__(self):
        self.trans_prop = {}
        self.emit_prop = {}
        self.start_prop = {}
        self.poslist = []
        self.trans_sum = {}
        self.emit_sum = {}

    def __upd_trans(self, curpos, nxtpos):
        """更新转移矩阵

        Args:
            curpos: 当前词性
            nxtpos: 下一词性
        """
        if curpos in self.trans_prop:
            if nxtpos in self.trans_prop[curpos]:
                self.trans_prop[curpos][nxtpos] += 1
            else:
                self.trans_prop[curpos][nxtpos] = 1
        else:
            self.trans_prop[curpos] = {nxtpos: 1}

    def __upd_emit(self, pos, word):
        """更新发射矩阵

        Args:
            pos: 词性
            word: 词语
        """
        if pos in self.emit_prop:
            if word in self.emit_prop[pos]:
                self.emit_prop[pos][word] += 1
            else:
                self.emit_prop[pos][word] = 1
        else:
            self.emit_prop[pos] = {word: 1}

    def __upd_start(self, pos):
        """更新初始状态矩阵

        Args:
            pos: 初始词语的词性
        """
        if pos in self.start_prop:
            self.start_prop[pos] += 1
        else:
            self.start_prop[pos] = 1

    def train(self, data_path):
        """训练 HMM 模型、求得转移矩阵、发射矩阵、初始状态矩阵

        Args:
            data_path: 训练数据的路径
        """
        f = open(data_path, 'r', encoding='utf-8')
        for line in f.readlines():
            line = line.strip().split()
            # 统计初始状态的概率
            self.__upd_start(line[0].split('/')[1])
            # 统计转移概率、发射概率
            for i in range(len(line) - 1):
                self.__upd_emit(line[i].split('/')[1], line[i].split('/')[0])
                self.__upd_trans(line[i].split('/')[1],
                                 line[i + 1].split('/')[1])
            i = len(line) - 1
            self.__upd_emit(line[i].split('/')[1], line[i].split('/')[0])
        f.close()
        # 记录所有的 pos
        self.poslist = list(self.emit_prop.keys())
        self.poslist.sort()
        # 统计 trans、emit 矩阵中各个 pos 的归一化分母
        num_trans = [
            sum(self.trans_prop[key].values()) for key in self.trans_prop
        ]
        self.trans_sum = dict(zip(self.trans_prop.keys(), num_trans))
        num_emit = [
            sum(self.emit_prop[key].values()) for key in self.emit_prop
        ]
        self.emit_sum = dict(zip(self.emit_prop.keys(), num_emit))

    def predict(self, sentence):
        """Viterbi算法预测词性

        Args:
            sentence: 分词后的句子（空格隔开）

        Returns:
            list: 词性标注序列 
        """
        sentence = sentence.strip().split()
        posnum = len(self.poslist)
        dp = pd.DataFrame(index=self.poslist)
        path = pd.DataFrame(index=self.poslist)
        # 初始化dp矩阵（dp矩阵 = posnum * wordsnum 存储每个word每个pos的最大概率）
        start = []
        num_sentence = sum(self.start_prop.values()) + posnum
        for pos in self.poslist:
            sta_pos = self.start_prop.get(pos, 1e-16) / num_sentence
            sta_pos *= (self.emit_prop[pos].get(sentence[0], 1e-16) /
                        self.emit_sum[pos])
            sta_pos = math.log(sta_pos)
            start.append(sta_pos)
        dp[0] = start
        # 初始化path矩阵
        path[0] = ['_start_'] * posnum
        # 递推
        for t in range(1, len(sentence)):  # 句子中第 t 个词
            prob_pos, path_point = [], []
            for i in self.poslist:  # i 为当前词的 pos
                max_prob, last_point = float('-inf'), ''
                emit = math.log(self.emit_prop[i].get(sentence[t], 1e-16) / self.emit_sum[i])
                for j in self.poslist:  # j 为上一次的 pos
                    tmp = dp.loc[j, t - 1] + emit
                    tmp += math.log(self.trans_prop[j].get(i, 1e-16) / self.trans_sum[j])
                    if tmp > max_prob:
                        max_prob, last_point = tmp, j
                prob_pos.append(max_prob)
                path_point.append(last_point)
            dp[t], path[t] = prob_pos, path_point
        # 回溯
        prob_list = list(dp[len(sentence) - 1])
        cur_pos = self.poslist[prob_list.index(max(prob_list))]
        path_que = []
        path_que.append(cur_pos)
        for i in range(len(sentence) - 1, 0, -1):
            cur_pos = path[i].loc[cur_pos]
            path_que.append(cur_pos)
        # 返回结果
        postag = []
        for i in range(len(sentence)):
            postag.append(sentence[i] + '/' + path_que[-i - 1])
        return postag


if __name__ == "__main__":
    HMM = HMMPosTag()
    HMM.train("./PeopleDaily_Clean.txt")
    test = HMM.predict("勉励 广大 职工 发挥 工人阶级 主力军 作用 ， 为 企业 改革 发展 建功立业")
    print(test)
