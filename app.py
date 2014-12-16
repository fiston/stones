#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField,TextAreaField,PasswordField,IntegerField,SelectField,FieldList,TextField,ValidationError
from wtforms.validators import DataRequired,Email,Length,EqualTo
from flask import Flask, render_template,session,redirect,url_for,flash,abort
from flask_sqlalchemy import SQLAlchemy
import os,re,smtplib
from utils import *

app = Flask(__name__)

# ================  GENERAL CONFIGURATIONS ==============
app.config['SECRET_KEY'] = SingleKeyGenerator(200).key

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
manager = Manager(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)
# ================= END GENERAL CONFIGURATIONS ===========

# ================== MODELS ==============================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(64))
    name = db.Column(db.String(32))
    email = db.Column(db.String(32),unique=True)
    telephone = db.Column(db.String(12))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User  %r>' %self.username

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

# ================ END MODELS ===========================

# ===================   FORMS =========================
class LoginForm(Form):
    username = StringField('username', description="Please enter your username",
                       validators=[DataRequired()])
    password = PasswordField('password', description="Enter a valid password",
                       validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(Form):
    username = StringField('username', description="Please choose your username",
                       validators=[DataRequired()])
    password = PasswordField('password', description="Please choose your password",
                       validators=[DataRequired(),Length(min=6),EqualTo('confirm', message='Passwords mismatch! Please retype your password and confirm it correctly!'),Password()])
    confirm = PasswordField('Confirm', description="Please retype your password",
                       validators=[DataRequired()])
    # role = SelectField(choices=[('1', 'Administrator'), ('2', 'Moderator'), ('3', 'Staff')])
    role = SelectField(choices= [(str(_.id),str(_.name)) for _ in Role.query.all()],description="please select the role")
    name = StringField('Name', description="Please enter your name",
                       validators=[DataRequired()])
    email = StringField('Email', description="Please enter your e-mail",
                       validators=[Email()])
    telephone = StringField('telephone', description="Please enter your phone number",
                       validators=[DataRequired()])
    submit = SubmitField('Register')

class ContactForm(Form):
    name = StringField('Name', description="Please enter your name",
                       validators=[DataRequired()])
    email = StringField('Email', description="Please enter your e-mail",
                       validators=[Email()])
    subject = StringField('Subject', description="Please enter the subject",
                       validators=[DataRequired()])
    message = TextAreaField('Message', description="Please enter your Message",
                       validators=[DataRequired()])
    submit = SubmitField('Send')

class RoleForm(Form):
    role_name = StringField('role name', description="Enter a role name",
                       validators=[DataRequired()])
    submit = SubmitField('role')

# ==================== END FORMS ===================


# ===================== VIEWS ========================
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data,password=form.password.data).first()
        if user:
            flash('Successfully loged in!','alert-success')
            session['name'] = user.name
            return render_template('home.html')
        else:
            form.username.data = ''
            form.password.data = ''
            flash('Incorrect username or password!','alert-danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('name',None)
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('name'):
        flash('Access is denied, please login to access requested page','alert-info')
        return redirect(url_for('login'))

    return render_template('home.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if not session.get('name'):
        flash('Access is denied, please login to access requested page','alert-info')
        return redirect(url_for('login'))

    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data; form.name.data = ''
        email = form.email.data; form.email.data = ''
        subject = form.subject.data; form.subject.data = ''
        message = form.message.data; form.message.data = ''
        receiver = ['ventum11@gmail.com']
        # content=raw_input('message: ')

        body1 = """From: %s <%s>
        To: %s
        Subject: %s

        %s
        """%(name,email,receiver,subject,message)
        try:
           smtpObj = smtplib.SMTP('localhost')
           smtpObj.sendmail(email,receiver, body1)
           flash("Successfully sent email",'alert-success')
        except:
            flash('Unable to send e-mail. verify your email and check the connection', 'alert-danger')
    return render_template('contact.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data,password=form.password.data,name=form.name.data,email=form.email.data,telephone=form.telephone.data,role_id=form.role.data)
            db.session.add(user)
            flash("user %s was added successfully. Now you can login with your credentials"%user.name,'alert-success')
        else:
            flash("user %s already exists! please add a new one"%user.name,'alert-danger')
            return redirect(url_for('register'))
        form.username.data = ''
        form.password.data = ''
        # register_form.role.data = ''
        form.name.data = ''
        form.email.data = ''
        form.telephone.data = ''
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/role', methods=['GET', 'POST'])
def role():
    if not session.get('name'):
        flash('Access is denied, please login to access requested page','alert-info')
        return redirect(url_for('login'))

    form = RoleForm()
    if form.validate_on_submit():
        role = User.query.filter_by(username=form.rolename.data).first()
        if role is None:
            role = Role(role_name=form.role_name.data)
            db.session.add(role)
            flash("Role %s was added successfully"%role.name,'alert-success')
        else:
            flash("Role %s already exists! please add a new one"%role.name,'alert-danger')
        form.role_name.data = ''
        return redirect(url_for('register'))
    return render_template('register.html', role_form=form)

@app.errorhandler(404)
def not_found_404(error):
    return render_template('404.html'),404
# ================ END VIEWS ============================




if __name__ == '__main__':
    manager.run()

