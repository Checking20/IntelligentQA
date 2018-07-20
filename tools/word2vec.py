# -*-coding=utf-8-*-
import jieba
import jieba.analyse
import json
from gensim.models import word2vec
import gensim
from gensim.test.utils import common_texts

# 预处理：读取文件、分词、去停用词
def pretreatment(file_name,stop_word_file):
    '''
    :param file_name: 文件名
    :param stop_word_file：停止词文件
    '''
    # 设置停用词
    stopwords = []
    with open(stop_word_file, encoding="UTF-8") as input_file:
        stopwords = [line.strip() for line in input_file.readlines()]
        stopwords+['\n',' ']

    # 预处理
    with open(file_name) as raw_data:
        json_data = json.load(raw_data)
        sentence_list = []
        # 将json转换成文档
        for cur_json in json_data:
            cur_doc = cur_json['title']
            cur_doc += cur_json['desc']
            cur_doc += cur_json['answer_best']
            for text in cur_json['answers_other']:
                cur_doc += text
            sentence = []
            raw_sentence = list(jieba.cut(cur_doc))
            for word in raw_sentence:
                if word in stopwords:
                    continue
                sentence.append(word)
            sentence_list.append(sentence)
        
        # 返回句子序列
        print("中文分词完成")
        return sentence_list

# 模型训练
def model_training(sentence_list,model_name):
    '''
    :param sentence_list 训练数据
    :param model_name 模型名称
    '''
    # 词向量维度
    model_size = 500
    # 上下文窗口长度
    model_window = 5
    # 最小计数
    min_count = 3
    # 开启线程数
    workers = 4

    # 模型训练
    model = word2vec.Word2Vec(sentences=sentence_list,size=model_size, window=model_window, min_count=min_count, workers=workers)
    # 存储模型
    model.save(model_name)
    
    
if __name__ == "__main__":
    sentence_list = pretreatment("data3_new.json","stop_words.txt")
    model_training(sentence_list,"w2v.model")
    