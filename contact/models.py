from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    email = models.EmailField(max_length=255, null=False, verbose_name=_('Email'))
    subject = models.CharField(max_length=100, null=False, verbose_name=_('Username'))
    message = models.CharField(max_length=40, null=False, verbose_name=_('Message Content'))

    def __unicode__(self):
        return self.email + ':' + self.subject

