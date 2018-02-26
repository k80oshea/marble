from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.local),
    url(r'^main$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^travels$', views.dashboard),
    url(r'^travels/add$', views.add_plan),
    url(r'^createtrip$', views.create),
    url(r'^join/(?P<dest_id>\d+)$', views.join),
    url(r'^travels/destination/(?P<dest_id>\d+)$', views.destination),
    url(r'^logout$', views.logout)
]