from flask import render_template, session, redirect, url_for

from . import main


# 主页(测试服务器是否正常链接)
@main.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello world!'