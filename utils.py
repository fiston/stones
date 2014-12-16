import re,smtplib
import binascii
from os import urandom

from wtforms.validators import ValidationError


class SingleKeyGenerator(object):
    _instance = None

    def __new__(self, size):
        if not self._instance:
            self._instance = super(SingleKeyGenerator, self).__new__(self)
            self.key = binascii.b2a_hqx(urandom(size)).decode('utf-8')
        return self._instance


class Password(object):
    """
    makes sure that field data contains atleast
    lowercase, uppercase, digit and ponctuation letters. Based on what is missing display a custom message
    """

    def __init__(self, message=None):
        if not message:
            message = "Password must contain atleast lowercase, uppercase, digit and special character"
        self.message = message

    def __call__(self, form, field):
        is_complex_pass = re.match('^.*(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*[\W]).*$', field.data)

        if not is_complex_pass:
            raise ValidationError(self.message)

class Telephone(object):
    """
    makes sure that field data contains atleast
    lowercase, uppercase, digit and ponctuation letters. Based on what is missing display a custom message
    """

    def __init__(self, message=None):
        if not message:
            message = "The telphone you are using is not registered in Rwanda"
        self.message = message

    def __call__(self, form, field):

        if (field.data.startswith('0788') or field.data.startswith('0785') or field.data.startswith('0784')) and len(field.data)==10:
            pass
        elif field.data.startswith('072') and len(field.data)==10:
            pass
        elif field.data.startswith('073') and len(field.data)==10:
            pass
        else:
            raise ValidationError(self.message)


def email_sender():
    receivers = ['ventum11@gmail.com']
    name = raw_input("name: ")
    email=raw_input('email: ')
    subject=raw_input('subject: ')
    content=raw_input('message: ')

    message = """From: %s <%s>
    To: %s
    Subject: %s

    %s
    """%(name,email,receivers,subject,content)

    try:
       smtpObj = smtplib.SMTP('localhost')
       smtpObj.sendmail(email, receivers, message)
       print "Successfully sent email"
    except:
        print "Error: unable to send email"
# print SingleKeyGenerator