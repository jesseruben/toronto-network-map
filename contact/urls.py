from contact.views import ContactView
from django.conf.urls import url

urlpatterns = [url(r'^$', ContactView.as_view(), name='contact')]
