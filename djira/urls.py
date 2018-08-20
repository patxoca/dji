# -*- coding: utf-8 -*-

# $Id:$

from functools import partial

from django.conf.urls import url

from djira import views


urlpatterns = [
    url(r"^$", partial(views.dispatcher, name="__list__"), name="djira_root_view"),
    url(r"^(?P<name>\w+)/$", views.dispatcher, name="djira_dispatcher_view")
]
