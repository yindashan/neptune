#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-3-28

@author: jingwen.wu
'''
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^index/$', 'apppackage.views.index', name="apppackage_index"),
    url(r'^add/$', 'apppackage.views.add_apppackage',name="apppackage_add"),
    url(r'^delete/(?P<id>\d+)/$', 'apppackage.views.delete_apppackage',name="apppackage_delete"),
    url(r'^selecteddelete/$', 'apppackage.views.selecteddelete_apppackage',name="apppackage_selecteddelete"),
    url(r'^edit/(?P<id>\d+)/$', 'apppackage.views.edit_apppackage',name="apppackage_edit"),
)