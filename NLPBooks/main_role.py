# coding=utf-8
import nltk

__author__ = 'gu'

from pyltp import Segmentor
from pyltp import Postagger,SentenceSplitter
import os

class Books:
    """
    获取每一章节的主要人物 和整本书的主要人物
    """
    ltp_model_path = "PycharmProjects/myltpdata/ltp_data"
    book_root_path = "PycharmProjects/mybooks/Book/"
    mainrole_root_path = "PycharmProjects/mybooks/MainRole/"
    mainlo_root_path = "PycharmProjects/mybooks/MainLocaltion/"

    seg = Segmentor()
    seg.load(ltp_model_path + '/cws.model')
    postagger = Postagger()  # 初始化实例
    postagger.load(ltp_model_path + '/pos.model')  # 加载模型


    def readBookLines(self, path):
        rf = open(path, "r")
        lines = rf.readlines()
        rf.close()
        return lines

    def writeTxt(self, path, namelist):
        wf = open(path, "w")
        for name,times,freq in namelist:
            wf.write(str(name)+ " "+str(times)+" "+str(freq) + "\n")
        wf.close()

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
        # self.seg.release()
        return words_list


    def posttagerNLNS(self,word_list):
        """
        nl  location noun   城郊
        ns  geographical name   北京
        :return:
        """
        postags = self.postagger.postag(word_list)  # 词性标注
        localtion_list = []
        for word, tag in zip(word_list, postags):
            if (tag == "nl" or tag == "ns") and len(word) > 3:
                print word + '/' + tag
                localtion_list.append(word)
        # postagger.release()  # 释放模型
        return localtion_list


    def posttaggerNH(self, word_list):
        """
        ltp的词性标注,获取人名nh
        :param word_list:
        :return:
        """

        postags = self.postagger.postag(word_list)  # 词性标注
        name_list = []
        for word, tag in zip(word_list, postags):
            if tag == "nh" and len(word) > 3:
                print word + '/' + tag
                name_list.append(word)
        # postagger.release()  # 释放模型
        return list(postags), name_list

    def getTopTen(self, namelist):
        """
        item times freq == itf
        :param namelist:
        :return:
        """
        resultitf = []
        resultname = []
        top10Name = []
        chapter_fdist = nltk.FreqDist(namelist)
        top_name_list = sorted(chapter_fdist.iteritems(), key=lambda x: x[1], reverse=True)
        for name, num in top_name_list[0:10]:
            tmplist = [name] * num
            top10Name+=tmplist
            resultname.append(name)
        chapter_fdist_ten = nltk.FreqDist(top10Name)
        for name1, num1 in sorted(chapter_fdist_ten.iteritems(), key=lambda x: x[1], reverse=True):
            print name1,num1,round(float(chapter_fdist_ten.freq(name1)), 2)
            resultitf.append((name1,num1,round(float(chapter_fdist_ten.freq(name1)), 2)))
        return resultitf,resultname

    def mainLocaltion(self,dirName="西游记白话文"):
        txtlist = os.listdir(self.book_root_path+dirName)
        lo_list_book = []
        for txt in txtlist:
            lo_list_chapter = []
            print txt
            lines = self.readBookLines(self.book_root_path+dirName + "/" + txt)
            for line in lines:
                if line != "":
                    sents = SentenceSplitter.split(line)
                    for sent in sents:
                        words_line = self.segmentor(sent)
                        lo_list_line = self.posttagerNLNS(words_line)
                        lo_list_chapter += lo_list_line
            # 统计每一章节top 10
            top_itf_chapter,top_lo_chapter = self.getTopTen(lo_list_chapter)
            lo_list_book += top_lo_chapter
            self.writeTxt(self.mainlo_root_path+dirName + "/" + txt, top_itf_chapter)
            print txt+"本章节top 10----------------------"
            for cloname,clotimes,clofreq in top_itf_chapter:
                print cloname,clotimes,clofreq
        # 统计整本书 top 10
        top_loitf_book,top_lo_book = self.getTopTen(lo_list_book)
        self.writeTxt(self.mainlo_root_path+dirName + "/AllChapter.txt", top_loitf_book)
        print "整本书 top 10----------------------"
        for bloname,blotimes,blofreq in top_loitf_book:
            print bloname,blotimes,blofreq

    def mainName(self, dirName):
        txtlist = os.listdir(self.book_root_path+dirName)
        name_list_book = []
        for txt in txtlist:
            name_list_chapter = []
            print txt
            lines = self.readBookLines(self.book_root_path+dirName + "/" + txt)
            for line in lines:
                if line != "":
                    sents = SentenceSplitter.split(line)
                    for sent in sents:
                        words_line = self.segmentor(sent)
                        postags_line, name_list_line = self.posttaggerNH(words_line)
                        name_list_chapter += name_list_line
            # 统计每一章节top 10
            top_itf_chapter,top_name_chapter = self.getTopTen(name_list_chapter)  # [(name,times,freq),()]
            name_list_book += top_name_chapter
            self.writeTxt(self.mainrole_root_path+dirName + "/" + txt, top_itf_chapter)
            print txt+"本章节top 10----------------------"
            for cname,ctimes,cfreq in top_itf_chapter:
                print cname,ctimes,cfreq
        # 统计整本书 top 10
        top_itf_book,top_name_book = self.getTopTen(name_list_book)
        self.writeTxt(self.mainrole_root_path+dirName + "/AllChapter.txt", top_itf_book)
        print "整本书 top 10----------------------"
        for bname,btimes,bfreq in top_itf_book:
            print bname,btimes,bfreq

    def getAllMainName(self):
        dirNames = os.listdir(self.book_root_path)
        for dirname in dirNames:
            print dirname
            self.mainName(dirname)

    def getAllMainLo(self):
        dirNames = os.listdir(self.book_root_path)
        for dirname in dirNames:
            print dirname
            self.mainLocaltion(dirname)


book = Books()
book.getAllMainLo()
book.getAllMainName()
