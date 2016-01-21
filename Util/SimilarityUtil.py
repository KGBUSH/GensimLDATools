# coding: utf-8


from Entity.GlobalValue import *

from gensim import corpora, models, similarities

import os
import shutil



def saveSimiResults(numCorpus, sort_sims, simi_resultpath):
    """
    把 第numCorpus 篇语料的相似度匹配较高的前30个结果保存到文件
    :param numCorpus: 当前要计算相似度匹配的语料
    :param sort_sims: 得到的相似度结果
    :param simi_resultpath: 要存储的位置
    :return:
    """
    fsim = open(simi_resultpath, 'w')
    print 'Saving the similarityResults of the ' + str(numCorpus) + ' corpus'
    fsim.write('the similarityResults of the ' + str(numCorpus) + ' corpus:' + '\n\n')
    simnum = 0
    for tup in sort_sims:
        fsim.write(str(tup) + '\n')
        simnum += 1
        if simnum >= 30:
            break
    fsim.close()






class SimilarityUtil(object):
    """
    对语料库中每一篇corpus做一次相似度查询，并把结果存入文件
    """
    def __init__(self, myCorporaLocation, myLDALocation):
        """
        载入相似度查询所需要的 语料库， LDA模型， 并得出index
        :param myCorporaLocation: 语料库的位置
        :param myLDALocation: lda模型的位置
        :return:
        """
        self._list_corpus = corpora.MmCorpus(myCorporaLocation)
        self._lda = models.LdaModel.load(myLDALocation)

        self._index = similarities.MatrixSimilarity(self._lda[self._list_corpus])

        # 先清空similarityResult文件夹， 再创建
        if os.path.isdir(GLOBAL_simiresultsFolder):
            shutil.rmtree(GLOBAL_simiresultsFolder, True)
        os.makedirs(GLOBAL_simiresultsFolder)


    @property
    def list_corpora(self):
        return self._list_corpus



    def similarityQuery(self, numofCorpus):
        """
        对第numofCorpus篇语料单独做一次相似度计算
        :param numofCorpus:  当前语料在list_corpora中的编号
        :return:
        """

        vec_bow = self._list_corpus[numofCorpus]
        vec_lda = self._lda[vec_bow]
        sims = self._index[vec_lda]
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])

        simi_resultpath = GLOBAL_simiresultsFolder + '\\sims_corpus' + str(numofCorpus) + '.txt'
        # 存入文件
        saveSimiResults(numofCorpus, sort_sims, simi_resultpath)









if __name__ == "__main__":

    # 载入语料库和lda模型
    CorporaLocation = GLOBAL_generatedFiles + '\\' + GLOBAL_corporaTfidfName
    LDALocation = GLOBAL_generatedFiles + '\\' + 'topics20___iterations1000___.lda'
    mysimi = SimilarityUtil(myCorporaLocation=CorporaLocation, myLDALocation=LDALocation)

    for x in xrange(len(mysimi.list_corpora)):
        mysimi.similarityQuery(numofCorpus=x)

