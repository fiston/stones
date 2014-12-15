import re
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


# print SingleKeyGenerator