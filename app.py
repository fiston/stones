#! /usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/service')
def service():
    return render_template('service.html')

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()

