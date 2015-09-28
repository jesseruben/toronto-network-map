from django.contrib import admin
from .models import Server, NDTProfile, NDT
# Register your models here.
admin.site.register(Server)
admin.site.register(NDT)
admin.site.register(NDTProfile)
