#! /usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,IntegerField, SubmitField,TextAreaField

from wtforms.validators import DataRequired,NumberRange,Email

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'V6%.,]{|\]d*/.,47-.,.<><.,./.,.,,][p[po08097869785^&%&^5865648(&897POJ86534324#%$^%$%^%$^$&^%^&97&^&^78943kj&^jksd'"``-)==+++-0090-998087^&6756565#232@!@#GJ{}'j"''

@app.route('/',methods=['GET','POST'])
def home():
    name = None
    age = None
    email = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        age = form.age.data
        form.age.data = None
        email = form.email.data
        form.email.data = ''
    return render_template('home.html', form=form, name=name,age=age,email=email)


@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    form = ContactForm()
    return render_template('contact.html',form=form)
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

class NameForm(Form):
    email = StringField("Email:", validators=[Email()])
    name = StringField("What is your name?", validators=[DataRequired()])
    age = IntegerField("How old are you?", validators=[NumberRange()])

    submit = SubmitField('Submit')

class ContactForm(Form):
    email = StringField("Email:", validators=[Email()])
    name = StringField("What is your name?", validators=[DataRequired()])
    message = TextAreaField("Message:", validators=[DataRequired()])

    submit = SubmitField('Submit')

if __name__ == '__main__':
    manager.run()

