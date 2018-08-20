# -*- coding: utf-8 -*-

# $Id:$

from django.conf.urls import include
from django.conf.urls import url

from djira import views

# URL patterns for djira

urlpatterns = [
    # Exemples:
    # url(r"^$", "djira.views.home", name="home"),
    # url(r"^blog/", include("blog.urls")),
    # url(r"^blog/(?P<pk>\d+)/", views.blog_view, name="blog_view"),

    url(r"^(?P<name>\w+)/$", views.dispatcher, name="djira_dispatcher_view")
    #MARKER:urls
]
