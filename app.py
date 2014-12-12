#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from urllib import parse
from functools import wraps
from utils import SingleKeyGenerator

from flask_wtf import Form
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, request, session, flash, url_for


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = SingleKeyGenerator(32).key
app.config['SQLALCHEMY_COMMIT_ON_TEAR_DOWN'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASE_DIR, "stones.db")

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class Password(object):
    def __init__(self, message=None):
        if not message:
            message = "You password must include atleast one lowercase, \
            uppercase, number and a special character"
        self.message = message

    def __call__(self, form, field):
        regex = '[a-z]+'
        if not re.search(regex, field.data):
            raise ValidationError(self.message)


class LoginForm(Form):
    username = StringField('Username', [DataRequired()],
                           description="Please enter your name")
    password = PasswordField('Password', [DataRequired()],
                             description="Please enter your password")
    submit = SubmitField('Login')


class RegistrationForm(Form):
    username = StringField('Username', [DataRequired(), Length(2)])
    password = PasswordField('Password', [DataRequired(), Length(6), Password(),
                                          EqualTo('confirm')])
    confirm = PasswordField('Confirm', [DataRequired()])
    email = StringField('Email', [DataRequired(), Email()])
    firstname = StringField('Firstname')
    lastname = StringField('Lastname')
    telephone = StringField('Telephone')
    submit = SubmitField('Register')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(32), unique=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    telephone = db.Column(db.String(12))

    def __repr__(self):
        return '<User: %s>' % self.username


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            flash("A user with the username already exist", "alert-warning")
        else:
            db.session.add(User(username=form.username.data,
                                password=form.password.data,
                                email=form.email.data,
                                firstname=form.firstname.data,
                                lastname=form.lastname.data,
                                telephone=form.telephone.data))

            flash("You have successfully registered", "alert-success")
            return redirect(url_for('login'))

    return render_template('registration.html', form=form)


@app.route('/logout')
def logout():
    return redirect(url_for('home'))


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    manager.run()
