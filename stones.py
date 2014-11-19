#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

application = Flask(__name__)


@application.route('/')
def index():
    return "<h1>Hello, World!</h1>"

@application.route('/kigali')
def where_are_you():
    return "<h2>I am in the capital of Rwanda</h2>"

@application.route('/user/<name>')
def get_user(name):
    return "<h2>Hello, %s</h2>" % name

if __name__ == '__main__':
    application.run(port=3000, debug=True)
