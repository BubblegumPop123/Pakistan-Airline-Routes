from django.urls import path
from . import views

urlpatterns = [
    path("",views.show),
    path("getPath",views.getPath)
]