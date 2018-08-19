# -*- coding: utf-8 -*-

# $Id:$

# URL test patterns for djira. Use this file to ensure a consistent
# set of URL patterns are used when running unit tests. This test_urls
# module should be referred to by your test class.

from django.conf.urls import include
from django.conf.urls import url


urlpatterns = [
    # url(r"^accounts/", include("django.contrib.auth.urls")),
    # url(r"^formsng/", include("hera_formsng.urls")),
    # url(r"^utils/", include("hera_utils.urls")),
    url(r"^app/", include("djira.urls")),
]
