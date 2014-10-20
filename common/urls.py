#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'common.views.index',name="index"),
    url(r'^nav_index/$', 'common.views.nav_index', name="common_index"),
    url(r'^nav_resource/$', 'common.views.nav_resource', name="common_resource"),
    url(r'^nav_log/$', 'common.views.nav_log', name="common_log"),
    url(r'^nav_ippool/$', 'common.views.nav_ippool', name="common_ippool"),
    url(r'^nav_user/$', 'common.views.nav_user', name="common_user"),
    url(r'^nav_authority/$', 'common.views.nav_authority', name="common_authority"),
    
    url(r'^main/$', 'common.views.main', name="common_main"),
    
)