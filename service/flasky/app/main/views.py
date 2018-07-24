from flask import render_template, session, redirect, url_for
import json

from . import main

from .search import search_questions
from .search import train_model


# 主页(测试服务器是否正常链接)
@main.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello world!'


# 智能搜索
@main.route('/search/<text>', methods=['GET', 'POST'])
def search(text):
    return search_questions(text)


# 手动调用训练模型
@main.route('/trainmodel/', methods=['GET'])
def model_train():
    train_model()
    return json.dumps(True)