from django.urls import path
from .views import *
from django.conf import urls

urlpatterns = [
    path('', home, name='home'),
    path("marsweather/", marsWeather, name="marsweather"),
    path("mrp/", mrp, name='mrp'),
    path("mrp/spirit/", mrpspirit, name='mrpspirit'),
    path("mrp/opportunity/", mrpopportunity, name='mrpopportunity'),
    path("mrp/curiosity/", mrpcuriosity, name='mrpcuriosity'),
    path("trekimagery", trekImagery, name="trekimagery"),
    path("search/", nasaSearch, name="nasasearch"),
    path("crewmembers/", crewMembers, name="crewmembers")
]

urls.handler404 = 'nasafree.views.handlerErrorPage'