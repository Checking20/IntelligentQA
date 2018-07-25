from flask import render_template, session, redirect, url_for
import json

from . import main

from .search import search_questions
from .search import train_model


# 主页(测试服务器是否正常链接)
@main.route('/', methods=['GET'])
def hello_world():
    return 'Hello world!'


# 智能搜索（使用D2V模型）
@main.route('/search/<int:start>/<int:row>/<text>', methods=['GET', 'POST'])
def search(start,row,text):
    return search_questions(text, start, row)


# 手动调用训练模型（关闭：内存不够）
@main.route('/trainmodel/', methods=['GET'])
def model_train():
    # train_model()
    return "由于服务器本身性能问题，本接口暂时关闭"