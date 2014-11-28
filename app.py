#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask import Flask, render_template

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    manager.run()
