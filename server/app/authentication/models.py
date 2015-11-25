from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from polymorphic import PolymorphicModel, PolymorphicManager

class UserManager(DjangoUserManager, PolymorphicManager):
    pass


class User(PolymorphicModel, AbstractUser):

    objects = UserManager()

    class Meta:
        verbose_name = u'User'
        verbose_name_plural = u'Users'
        app_label = 'authentication'

    def __unicode__(self):
        return self.username
