from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('contact/', index, name='contact'),

    #API
    path('api/contact/', contact_api, name='contact_api'),

    #API
    path("api/unavailable-dates/", unavailable_dates, name="unavailable_dates"),
    path("api/unavailable-times/", unavailable_times, name="unavailable_times"),
]