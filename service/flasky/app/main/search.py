from gensim.models.doc2vec import Doc2Vec,TaggedDocument
from datetime import date
import requests
import jieba
import json

# 绝对路径
sw_url = '/root/github/IntelligentQA-master/flasky/stop_words.txt'
model_url_prefix = '/root/github/IntelligentQA-master/flasky/'


# 进行分词并转换成模型需要的格式
def pretreatment(json_list):
    '''
    :param json_list: 文档json数据转换得到的dict_list
    :return: list of TaggedDocument
    '''
    # 设置停用词
    stopwords = []
    with open(sw_url, encoding="UTF-8") as input_file:
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
    '''
    :param timing: 延迟（离线计算下一天的模型）
    :return: 无返回值
    '''
    resp = requests.post('http://60.205.216.102:8080/abcde')
    docs = pretreatment(resp.json()['data'])
    model = Doc2Vec(alpha=0.025, min_alpha=0.025, min_count=2, window=10, vector_size=400, sample=1e-5, train_lbls=False, workers=1)
    # 建立词典
    model.build_vocab(docs)
    # 训练模型
    model.train(docs, total_examples=model.corpus_count, epochs=80)
    tom = date.today()
    model.save(model_url_prefix+"models/d2v_"+date(tom.year, tom.month, tom.day+timing).strftime('%Y-%m-%d')+".model")


# 寻找最相似的提问
def get_similar(word_list, topn):
    '''
    :param word_list 分词结果
    :param topn 最相似的N个
    :return list of tuple(问题id,相似度)
    '''

    model = None
    # 如果得不到当天的模型，使用默认模型
    try:
        model = Doc2Vec.load("models/d2v_"+date.today().strftime('%Y-%m-%d')+".model")
    except FileNotFoundError:
        model = Doc2Vec.load("models/d2v_default.model")
    # 计算提问的向量
    infer = model.infer_vector(word_list)
    return model.docvecs.most_similar([infer], topn=topn)


# 针对查询进行相关问题检索
def search_questions(text, start=0, row=20):
    '''
    :param text: 用户查询文本
    :param start: 起始序号
    :param row: 需要结果个数
    :return: 序列化的json
    '''
    # 添加停止词
    stopwords = []
    with open(sw_url, encoding="UTF-8") as input_file:
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
    return json.dumps(get_similar(sentence, topn=start+row)[start:])

if __name__ == '__main__':
    train_model(timing=1)