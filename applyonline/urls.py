#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^index/$', 'applyonline.views.index', name="applyonline_index"),
    url(r'^detail/(?P<id>\d+)/$', 'applyonline.views.detail', name="applyonline_detail"),
    url(r'^add/$', 'applyonline.views.add', name="applyonline_add"),
    url(r'^edit/(?P<id>\d+)/$', 'applyonline.views.edit', name="applyonline_edit"),
    url(r'^deploy_success/(?P<id>\d+)/$', 'applyonline.views.deploy_success', name="applyonline_deploy_success"),
    url(r'^deploy_failure/(?P<id>\d+)/$', 'applyonline.views.deploy_failure', name="applyonline_deploy_failure"),
    url(r'^validate_success/(?P<id>\d+)/$', 'applyonline.views.validate_success', name="applyonline_validate_success"),
    url(r'^validate_failure/(?P<id>\d+)/$', 'applyonline.views.validate_failure', name="applyonline_validate_failure"),
    url(r'^delete/(?P<id>\d+)/$', 'applyonline.views.delete', name="applyonline_delete"),
    url(r'^selecteddelete/$', 'applyonline.views.selecteddelete', name="applyonline_selecteddelete"),
    
    
)