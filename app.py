#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField,TextAreaField,PasswordField
from wtforms.validators import DataRequired,Email
from flask import Flask, render_template,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '*&^&^786&^$#%$##$@!@#~!@~@#?><?></.,./7*&6%^$$54343$#FFGHv@##2xgh===_+);;,/,.<><{]P{}}|{]::'
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)


class NameForm(Form):
    name = StringField('Name', description="Please enter your name",
                       validators=[DataRequired()])
    submit = SubmitField('Send')

class LoginForm(Form):
    username = StringField('username', description="Please enter your username",
                       validators=[DataRequired()])
    password = PasswordField('password', description="Enter a valid password",
                       validators=[DataRequired()])
    submit = SubmitField('Send')


class ContactForm(Form):
    name = StringField('Name', description="Please enter your name",
                       validators=[DataRequired()])
    email = StringField('Email', description="Please enter your e-mail",
                       validators=[Email()])
    message = TextAreaField('Message', description="Please enter your Message",
                       validators=[DataRequired()])
    submit = SubmitField('Send')

class RegisterForm(Form):
    username = StringField('username', description="Please choose your username",
                       validators=[DataRequired()])
    password = StringField('password', description="Please choose your password",
                       validators=[DataRequired()])
    name = StringField('Name', description="Please enter your name",
                       validators=[DataRequired()])
    email = StringField('Email', description="Please enter your e-mail",
                       validators=[Email()])
    telephone = StringField('telephone', description="Please enter your phone number",
                       validators=[DataRequired()])
    submit = SubmitField('Register')


@app.route('/', methods=['GET', 'POST'])
def login():
    username = None
    password = None
    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        if username=='ventum'  and password == '123':
            flash('Successfully loged in!','alert-success')
            return render_template('home.html', login_form=login_form, username=session.get('username'))
        else:
            login_form.username.data = ''
            login_form.password.data = ''
            flash('Incorrect username or password!','alert-error')
            return redirect(url_for('login'))
    return render_template('login.html', login_form=login_form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    name = None
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Your name has been changed succeffully!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('home'))
    return render_template('home.html', form=form)



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    name = None
    email = None
    message = None
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        name = contact_form.name.data; contact_form.name.data = ''
        email = contact_form.email.data; contact_form.email.data = ''
        message = contact_form.message.data; contact_form.message.data = ''
    return render_template('contact.html', contact_form=contact_form, name=name,email=email,message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    username = None
    password = None
    name = None
    email = None
    telephone = None

    register_form = RegisterForm()
    if register_form.validate_on_submit():
        username = register_form.username.data; register_form.username.data = ''
        password = register_form.password.data; register_form.password.data = ''
        name = register_form.name.data; register_form.name.data = ''
        email = register_form.email.data; register_form.email.data = ''
        telephone = register_form.telephone.data; register_form.telephone.data = ''
    return render_template('register.html', register_form=register_form, username=username,password=password,name=name,email=email,telephone=telephone)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role is : %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User is : %r>' %self.username


if __name__ == '__main__':
    manager.run()
