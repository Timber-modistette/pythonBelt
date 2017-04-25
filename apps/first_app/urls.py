from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^homepage$', views.homepage),
	url(r'^logout$', views.logout),
	url(r'^createQuote$', views.createQuote),
	url(r'^favouritequote/(?P<quoteid>\d*)$', views.favouritequote),
	url(r'^userProfile/(?P<userid>\d*)$', views.userProfile),
	url(r'^removequote/(?P<quoteid>\d*)$', views.removequote),



]