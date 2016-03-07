from .views import FaqViewSet
from django.conf.urls import url

urlpatterns = [url(r'^$', FaqViewSet.as_view({'get': 'list'}), name='faq')]
