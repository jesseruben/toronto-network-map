import django_filters as filters
from .models import NDTProfile, NDT


class NDTProfileFilter(filters.FilterSet):
    class Meta:
        model = NDTProfile
        '''
        Just some comments for understanding...
        the 'exact' means you can search by appending to url: ?name=searchterm
        the 'icontains' means you can search (case insensitive) by appending to url: ?name__icontains=searchterm
        '''
        fields = {'name': ['exact', 'icontains'], 'service_type': ['exact', 'icontains']}


class NDTFilter(filters.FilterSet):
    class Meta:
        model = NDT
        fields = {'download_rate': ['exact', 'gte', 'lte'], 'upload_rate': ['exact', 'gte', 'lte'],
                  'isp_name': ['exact', 'icontains'], 'rating_general': ['exact', 'gte', 'lte'],
                  'price': ['exact', 'gte', 'lte']}
