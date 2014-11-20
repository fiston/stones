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


@application.route('/greet/<name>')
def greetings(name):
    return "<h2>Mwaramutse, %s. Mbese murugo baraho!</h2>" % name


@application.route('/counter/<int:value>')
def counter(value):
    values = {1: 'one', 2:'two', 3:'three', 4:'four', 5:'five'}
    return "Number %s" % values.get(value, 'Unknown')

if __name__ == '__main__':
    application.run(port=3000, debug=True)
