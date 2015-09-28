from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
     we haven't defined a model for the manager, so self refers to the default model of
     BaseUserManager which is defined in settings.AUTH_USER_MODEL
    """
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError(_('User must have a valid email address.'))
        if not kwargs.get('username'):
            raise ValueError(_('Users must have a valid username.'))

        user = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Remember to add AUTH_USER_MODEL = 'accounts.User' and add accounts in installed app
    """
    email = models.EmailField(unique=True, max_length=255, db_index=True, verbose_name=_('Email'))
    username = models.CharField(max_length=40, unique=True, verbose_name=_('Username'))
    is_active = models.BooleanField(default=True, null=False,
                                    verbose_name=_('Only active user can login in the frontend'))
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('The time when the user was created'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Last time user got update'))
    notifications = models.IntegerField(default=0, verbose_name=_('Number of new notifications'))
    objects = UserManager()
    # User.objects.get(**kwargs)  objects is the built-in manager when we don't define it

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_short_name(self):
        return u"{0}".format(self.username)

    def get_full_name(self):
        return u"{0}".format(self.username)

    def __unicode__(self):
        return self.username


class UserUID(models.Model):
    """
    This class implements forgot password and email activation functionality for user model
    We want the user to be deleted to cascade to this model so we keep the default which is on_delete=cascade:
    if a user account is deleted all its records in this table will be deleted as well.
    """
    TYPE = (
        ('forgotPassword', _('Forgot Password')),
        ('activation', _('User Activation'))
    )
    user = models.ForeignKey(User, verbose_name=_('User'))
    guid = models.CharField(unique=True, max_length=100, verbose_name=_('Globally Unique Identifier (GUID)'))
    expiration_date = models.DateTimeField(default=timezone.now, verbose_name=_('Expiration Date'))
    type = models.CharField(choices=TYPE, default='forgotPassword', max_length=1, verbose_name=_('Type'))
