#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'account.views.index',name="accounts_index"),
    url(r'^index/$', 'account.views.index', name="accounts_index"),
    url(r'^info/(?P<id>\d+)/$', 'account.views.info',name="accounts_info"),
    url(r'^register/$', 'account.views.register',name="accounts_register"),
    url(r'^edit/(?P<id>\d+)/$', 'account.views.edit',name="accounts_edit"),
    url(r'^delete/(?P<id>\d+)/$', 'account.views.delete',name="accounts_delete"),
    url(r'^login/$', 'account.views.login',name="accounts_login"),
    url(r'^selecteddelete/$', 'account.views.selecteddelete',name="accounts_selecteddelete"),
    url(r'^logout/$', 'account.views.logout',name="accounts_logout"),
    url(r'^searchback_role/$', 'account.views.searchback_role',name="accounts_searchback_role"),
    url(r'^searchback_ldap/$', 'account.views.searchback_ldap',name="accounts_searchback_ldap"),
    url(r'^autocomplete/$', 'account.views.autocomplete', name = "accounts_autocomplete"),
)