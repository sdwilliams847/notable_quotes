from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^new_quote$', views.new_quote),
    url(r'^quotes/favorite/(?P<id>\d+)$', views.new_favorite),
    url(r'^quotes/delete/(?P<id>\d+)$', views.delete_favorite),
    url(r'^users/(?P<id>\d+)$', views.user_page),
    url(r'^delete/quote/(?P<id>\d+)$', views.delete_quote),
]