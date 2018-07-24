from gensim.models.doc2vec import Doc2Vec,TaggedDocument
from datetime import date
import requests
import jieba
import json


# 进行分词并转换成模型需要的格式
def pretreatment(json_list):
    # 设置停用词
    stopwords = []
    with open('stop_words.txt', encoding="UTF-8") as input_file:
        stopwords = [line.strip() for line in input_file.readlines()]
        stopwords += ['\n', ' ']

    # 预处理
    docs = []
    # 将json转换成文档
    for cur_json in json_list:
        cur_doc = str(cur_json['title'])
        cur_doc += str(cur_json['desc'])
        sentence = []
        raw_sentence = list(jieba.cut(cur_doc))
        for word in raw_sentence:
            if word in stopwords:
                continue
            sentence.append(word)
        docs.append(TaggedDocument(sentence, [str(cur_json['id'])]))

    return docs


# 训练模型
def train_model(timing=0):
    resp = requests.get('http://211.87.230.22:8080/abcde')
    docs = pretreatment(resp.json()['data'])
    model = Doc2Vec(dm=1, sample=0, vector_size=200, window=10, min_count=1, workers=4)
    model.build_vocab(docs)
    model.train(docs, total_examples=model.corpus_count, epochs=80)
    tom = date.today()
    model.save("models/d2v_"+date(tom.year, tom.month, tom.day+timing).strftime('%Y-%m-%d')+".model")


# 寻找最相似的提问
def get_similar(word_list, topn):
    '''
    :param word_list 分词结果
    :param topn 最相似的N个
    '''
    model = Doc2Vec.load("models/d2v_"+date.today().strftime('%Y-%m-%d')+".model")
    infer = model.infer_vector(word_list)
    return model.docvecs.most_similar([infer], topn=topn)


# 针对查询进行相关问题检索
def search_questions(text):
    # 添加停止词
    stopwords = []
    with open('stop_words.txt', encoding="UTF-8") as input_file:
        stopwords = [line.strip() for line in input_file.readlines()]
        stopwords += ['\n', ' ']

    # 对查询进行分词
    sentence = []
    raw_sentence = list(jieba.cut(text))
    print(raw_sentence)
    for word in raw_sentence:
        if word in stopwords:
            continue
        sentence.append(word)

    return json.dumps(get_similar(sentence, topn=20))