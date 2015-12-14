from django.db import models
from django.utils.translation import ugettext as _
from accounts.models import User
from isp.models import ISP
from locations.models import Country
from django.db.models.signals import pre_save
from django.dispatch import receiver
from random import SystemRandom
import hashlib


class NDTProfile(models.Model):
    # TODO: change the countries/cities implementation
    CANADA = 'CANADA'
    AMERICA = 'AMERICA'

    COUNTRY_CHOICES = (
        ('CANADA', _("Canada")),
        ('AMERICA', _("The United States of America")),
    )

    BUSINESS = 'BUSINESS'
    HOME = 'HOME'
    PUBLIC = 'PUBLIC'

    SERVICE_TYPE_CHOICES = (
        ('BUSINESS', _("Business")),
        ('HOME', _("Home")),
        ('PUBLIC', _("Public")),
    )

    user = models.ForeignKey(User, null=True)
    # 5 decimal places for latitude and longitude is accurate to within ~ 1.11 meters
    name = models.CharField(max_length=20, blank=False, null=False)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    nominal_download_rate = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True,
                                                verbose_name='nominal download rate')
    nominal_upload_rate = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True,
                                              verbose_name='nominal upload rate')
    bandwidth = models.IntegerField(blank=True, null=True, verbose_name='internet bandwidth')
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    contract = models.BooleanField(default=False, verbose_name='on contract?')
    service_type = models.CharField(choices=SERVICE_TYPE_CHOICES, max_length=20, null=False,
                                    blank=False)
    vpn = models.NullBooleanField()
    rating_general = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='general rating')
    rating_customer_service = models.PositiveSmallIntegerField(blank=True, null=True,
                                                               verbose_name='customer service rating')
    country = models.ForeignKey(Country, null=True)
    province = models.CharField(max_length=64, null=True)
    city = models.CharField(null=True, max_length=64)
    promotion = models.NullBooleanField()
    isp = models.ForeignKey(ISP)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"NDT PROFILE ID #{0} BELONGING TO USER WITH NAME {1}".format(self.id, self.name)


def _create_hash():
    rand = SystemRandom()
    return hashlib.sha512(str(rand.getrandbits(512))).hexdigest()


class NDT(models.Model):
    BUSINESS = 'BUSINESS'
    HOME = 'HOME'
    PUBLIC = 'PUBLIC'

    SERVICE_TYPE_CHOICES = (
        ('BUSINESS', _("Business")),
        ('HOME', _("Home")),
        ('PUBLIC', _("Public")),
    )

    ndt_profile = models.ForeignKey(NDTProfile, null=True)
    # All rates in Kilobits
    download_rate = models.FloatField(null=False, blank=False, verbose_name='Actual Download Rate (Kb)')
    upload_rate = models.FloatField(null=False, blank=False, verbose_name='Actual Upload Rate (Kb)')
    nominal_download_rate = models.FloatField(null=True, blank=True,
                                              verbose_name='Theoretical Download Rate(Kb)')
    nominal_upload_rate = models.FloatField(null=True, blank=True,
                                            verbose_name='Theoretical Upload Rate (Kb)')
    latency = models.DecimalField(max_digits=6, decimal_places=3, default=0, null=False, blank=False)
    # 5 decimal places for latitude and longitude is accurate to within ~ 1.11 meters
    latitude = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # Bandwidth is in Kilobytes
    bandwidth = models.IntegerField(blank=True, null=True, verbose_name='internet bandwidth (KB)')
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    city = models.CharField(null=True, max_length=64)
    country = models.ForeignKey(Country, null=True)
    isp_name = models.CharField(max_length=64, null=True)
    service_type = models.CharField(choices=SERVICE_TYPE_CHOICES, max_length=20, null=True,
                                    blank=True, default='Home')
    province = models.CharField(max_length=64, null=True)
    rating_general = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='general rating')
    hash = models.CharField(max_length=100, unique=True, default=_create_hash,
                            verbose_name='unique hash value used for UI identification')
    average_index = models.DecimalField(max_digits=5, decimal_places=2, default=1, blank=False,
                                        null=False, verbose_name='Number of test results contributing to the average')

    def __unicode__(self):
        return u"NDT ID #{0}".format(self.id)


class Web100(models.Model):
    ndt = models.ForeignKey(NDT, null=False)
    blob = models.TextField(null=False)


class Server(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'Server Name')
    country = models.ForeignKey(Country, null=False, verbose_name=u'Country Name')
    url = models.URLField(max_length=500, verbose_name=u'Server URL')
    active = models.BooleanField(default=True, verbose_name=u'Server Active')

    def __unicode__(self):
        return u"Server name: {0} in {1}.".format(self.name, self.country)

