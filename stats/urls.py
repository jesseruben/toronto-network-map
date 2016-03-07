from django.conf.urls import url
from .views import RegionalCircleView, AllTestsView, RegionalRectView

urlpatterns = [
    url(r'^regionalCircle/$', RegionalCircleView.as_view()),
    url(r'^regionalRect/$', RegionalRectView.as_view()),
    url(r'^allTests/$', AllTestsView.as_view())
]
