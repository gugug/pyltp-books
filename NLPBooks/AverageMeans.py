# coding=utf-8
from nltk.corpus import wordnet
class AverageMeans:
     def  get_average_means(self,poses):
        words = set(wordnet.words())  # 读取wordnet中的所有词
        pos_num = {}  # pos_num用以记录各词性词数
        pos_sens ={}  # pos_sens用以记录各词性词义数
        for pos in poses:
            pos_num[pos] = 0
            pos_sens[pos] = 0
        for word in words:
            terms = wordnet.synsets(word)
            cur_pos_num = {u'n': 0, u'v': 0, u's': 0, u'a': 0, u'r': 0}
            for term in terms:
                cur_pos_num[term.pos()] += 1
            for pos in poses:
                if cur_pos_num[pos] != 0:
                    pos_num[pos] += 1
                    pos_sens[pos] += cur_pos_num[pos]
        result = []
        for pos in poses:
            result.append(float(pos_sens[pos])/pos_num[pos])
        return result

if __name__ == '__main__':
    poses = [u'n', u'v', u's', u'a', u'r']
    am = AverageMeans()
    result = am.get_average_means(poses)
    for i in range(len(poses)):
        print poses[i],
        print "的平均多义性：" + str(result[i]) #总词义数/总词=数


