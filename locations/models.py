from django.db import models
from cities_light.abstract_models import *
from cities_light.receivers import *
import autoslug


__all__ = ['CONTINENT_CHOICES', 'to_search', 'to_ascii', 'filter_non_cities', 'filter_non_included_countries_country',
           'filter_non_included_countries_region', 'filter_non_included_countries_city']


class Country(AbstractCountry):
    """
    Inherited from cities_light class to add simple localized field
    alternate names had comma separated values which were not useful, esp. for searching
    INSERT INTO locations_country(`id`, `name_ascii`, `geoname_id`, `alternate_names`, `name`, `code2`, `code3`,
    `continent`, `tld`, `phone`, `slug`) SELECT `id`, `name_ascii`, `geoname_id`, `alternate_names`,
    `name`, `code2`, `code3`, `continent`, `tld`, `phone`, `slug` FROM cities_light_country;
    """
    # set null True for easier migrations and updates from remote db
    localized_name = models.CharField(max_length=64, null=True)

    def __unicode__(self):
        return self.name

# to connect cities_light signal to our inherited class
connect_default_signals(Country)
__all__.append('Country')


class Region(AbstractRegion):
    """
    Inherited from cities_light class to add simple localized field
    alternate names had comma separated values which were not useful, esp. for searching
    """
    # set null True for easier migrations and updates from remote db
    localized_name = models.CharField(max_length=64, null=True)

    def __unicode__(self):
        return self.localized_name

# to connect cities_light signal to our inherited class
connect_default_signals(Region)
__all__.append('Region')


class City(AbstractCity):
    """
    Inherited from cities_light class to add simple localized field
    alternate names had comma separated values which were not useful, esp. for searching
    """
    # set null True for easier migrations and updates from remote db
    localized_name = models.CharField(max_length=64, null=True)

    def __unicode__(self):
        return self.localized_name

# to connect cities_light signal to our inherited class
connect_default_signals(City)
__all__.append('City')







