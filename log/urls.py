#!usr/bin/env python
#coding: utf-8
'''
Created on 2012-5-29

@author: jingwen.wu
'''
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'log.views.index',name="log_index"),
    url(r'^index/$', 'log.views.index', name="log_index"),
    url(r'^add/$', 'log.views.add',name="log_add"),
    url(r'^edit/(?P<id>\d+)/$', 'log.views.edit',name="log_edit"),
    url(r'^detail/(?P<id>\d+)/$', 'log.views.detail',name="log_detail"),
    url(r'^delete/(?P<id>\d+)/$', 'log.views.delele',name="log_delete"),
    url(r'^selecteddelete/$', 'log.views.selecteddelete',name="log_selecteddelete"),
    url(r'^changerecord/(?P<log_type>\d+)/(?P<relate_id>\d+)/$', 'log.views.changerecord',name="log_changerecord"),
    
)