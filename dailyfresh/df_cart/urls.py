from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart),
    url(r'^add(\d+)_(-)?(\d+)/$', views.add),
    url(r'^delete/(\d+)/$', views.delete)
]