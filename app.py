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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
