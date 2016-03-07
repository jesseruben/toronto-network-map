from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce import models as tinymce_models


class Faq(models.Model):
    question = models.CharField(max_length=1000, null=False, verbose_name=_('Question'))
    answer = tinymce_models.HTMLField(null=False, verbose_name=_('Answer'))

    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
