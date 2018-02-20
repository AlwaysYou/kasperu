from django.db import models
from django.contrib.auth.models import User
from pbkdf2 import crypt
from django.conf import settings
import re

SECRET_KEY = settings.AUTH_SECRET_KEY
SALT = ''.join(re.findall("[a-zA-Z0-9]+", SECRET_KEY))
NUMERO_DE_ITERACIONES = 500

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    archivo_csv = models.FileField(upload_to="uploads",
                                   blank=True, null=True)
    class Meta:
        verbose_name = 'Usuarios Registrados'
        verbose_name_plural = 'Usuarios Registrados'

    def __unicode__(self):
        return u'{0}'.format(self.email)

    def is_password_valid(self, password):
        return is_password_valid(password, self.password)

    def is_authenticated(self):
        return True

    @property
    def is_staff(self):
        return False
# Create your models here.
# HELPERS

def encrypt_password(password):
    ''' Encripta la contraseña '''
    return crypt(password, SALT, NUMERO_DE_ITERACIONES)


def is_password_valid(password, encoded):
    ''' Contrasta la contraseña brindada con el valor encriptado '''
    return encrypt_password(password) == encoded

User._meta.get_field('username').max_length = 255
