# coding=utf-8
__author__ = 'gu'

import os
from pyltp import Segmentor,Postagger,SentenceSplitter

class PostagBook:
    """
    生成标注语料的代码类
    :keyword dan 表示 d-副词 a-形容词 n-名词
    """

    ltp_model_path = "PycharmProjects/myltpdata/ltp_data"
    book_root_path = "PycharmProjects/mybooks/Book"
    postag_root_path = "PycharmProjects/mybooks/PostagBook"
    seg = Segmentor()
    seg.load(ltp_model_path + '/cws.model')

    postagger = Postagger()  # 初始化实例
    postagger.load(ltp_model_path + '/pos.model')  # 加载模型

    def getAllPath(self):
        txtpathlist = []
        dirlist = os.listdir(self.book_root_path)
        for dirname in dirlist:
            print dirname
            path = self.book_root_path + "/"+dirname
            txtlist = os.listdir(path)
            for txtname in txtlist:
                print txtname
                txtpath = path + "/"+txtname
                txtpathlist.append(txtpath)
        print len(txtpathlist)
        return txtpathlist


    def segmentor(self, sentence="你好，广东外语外贸大学欢迎你。"):
        """
        ltp的分词模型
        :return:
        :param sentence:
        """

        words = self.seg.segment(sentence)
        words_list = list(words)
        # for word in words_list:
        #     print word
        # seg.release()
        return words_list

    def posttagger(self, word_list):
        """
        ltp的词性标注
        :param word_list:
        :return:
        """

        postags = self.postagger.postag(word_list)  # 词性标注
        dan_list = []
        for word, tag in zip(word_list, postags):
            if tag == "n" or tag == "a" or tag == "d":
                if len(word) > 3:
                    print word + '/' + tag
                    dan_list.append(word)
        # postagger.release()  # 释放模型
        return dan_list


    # d  a  n
    def getDan(self,path="PycharmProjects/mybooks/Book/西游记/1.txt"):
        dan_list = []
        rf = open(path,"r")
        lines = rf.readlines()
        rf.close()
        for line in lines:
            if line != "":
                sents = SentenceSplitter.split(line)
                for sent in sents:
                    words = self.segmentor(sent)
                    dan_list_line = self.posttagger(words)
                    dan_list += dan_list_line
        return list(set(dan_list))

    def getResult(self):
        allResult = []
        txtPathList = self.getAllPath()
        for txtPath in txtPathList:
            dan_list = self.getDan(txtPath)
            allResult += dan_list
        print len(allResult)
        print len(set(allResult))
        resultList = sorted(list(set(allResult)))
        self.writeDan(self.postag_root_path,"Postag.txt",resultList)
        return resultList

    def writeDan(self,path,filename,sortedList):
        wf = open(path+"/"+filename,"w")
        for elem in sortedList:
            wf.write(elem)
            # wf.write("\n")
        wf.close()

    def spiltTxt(self,path=postag_root_path+"/Postag.txt"):

        rf = open(path,"r")
        lines = rf.readlines()
        rf.close()
        print len(lines)
        self.writeDan(self.postag_root_path,"jingxing1.txt",lines[0:4000])
        self.writeDan(self.postag_root_path,"dage1.txt",lines[4000:8000])
        self.writeDan(self.postag_root_path,"zhenyu1.txt",lines[8000:])

import time
start = time.time()
postagebook = PostagBook()
# postagebook.getResult()
postagebook.spiltTxt()
end = time.time()
print end - start
