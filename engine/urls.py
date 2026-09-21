from django.contrib import admin
from django.urls import path

from engine.api import api
from engine.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
