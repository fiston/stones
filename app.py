#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aabbccddeeff!##$##@'
manager = Manager(app)
bootstrap = Bootstrap(app)


class NameForm(Form):
    name = StringField('Name', description="Please enter your name",
                       validators=[DataRequired()])
    submit = SubmitField('Send')


@app.route('/', methods=['GET', 'POST'])
def home():
    name = None
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('home.html', form=form, name=name)


if __name__ == '__main__':
    manager.run()
