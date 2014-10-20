#!usr/bin/env python
#coding: utf-8

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'organization.views.index',name="organization_index"),
    url(r'^index/$', 'organization.views.index', name="organization_index"),
    url(r'^add/$', 'organization.views.add',name="organization_add"),
    url(r'^edit/(?P<id>\d+)/$', 'organization.views.edit',name="organization_edit"),
    url(r'^delete/(?P<id>\d+)/$', 'organization.views.delete',name="organization_delete"),
    url(r'^selecteddelete/$', 'organization.views.selecteddelete',name="organization_selecteddelete"),
    url(r'^searchback/$', 'organization.views.searchback',name="organization_searchback"),
    url(r'^autocomplete/$', 'organization.views.autocomplete', name = "organization_autocomplete"),
)