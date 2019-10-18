from django.conf.urls import url
from . import views
from views import *

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list/(\d+)_(\d+)_(\d+)/$', views.list),
    url(r'^(\d+)/$', views.detail),
    url(r'^search/$', MysearchView()),
]