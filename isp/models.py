from django.db import models
from django.utils.translation import ugettext as _


class ISP(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    website = models.URLField(max_length=500, null=False, blank=False)
    phone = models.IntegerField(null=False, blank=False)
    support_phone = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(max_length=3, blank=True)
    facebook = models.URLField(max_length=500, null=True, blank=True)
    twitter = models.URLField(max_length=500, null=True, blank=True)
    support_link = models.URLField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return u"ISP name: {0}".format(self.name)


class Plan(models.Model):
    isp = models.ForeignKey(ISP, null=False, related_name='plans')
    name = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False)
    contract = models.BooleanField(default=False)
    contract_length = models.IntegerField(blank=True, null=True)  # in months
    download_rate = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False)
    upload_rate = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False)
    bandwidth = models.BooleanField(default=True)
    bandwidth_limit = models.IntegerField(blank=True, null=True)  # in GB
    limited_offer = models.BooleanField(default=False)
    link = models.URLField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u"Plan name: {0} which belongs to isp: {1}".format(self.name, self.isp.name)
