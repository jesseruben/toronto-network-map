from django.conf.urls import  url
from .views import LoginView, LogoutView, UpdatePasswordView, ForgotPasswordView, DeactivateView, SetPasswordView
from .views import UserViewSet

urlpatterns = [
    url(r'^register/$', UserViewSet.as_view({'post': 'create', }), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^updatepassword/$', UpdatePasswordView.as_view(), name='updatepassword'),
    url(r'^forgotpassword/$', ForgotPasswordView.as_view(), name='forgotpassword'),
    url(r'^deactivate/$', DeactivateView.as_view(), name='deactivate'),
    url(r'^setpassword/$', SetPasswordView.as_view(), name='setpassword'),
]
