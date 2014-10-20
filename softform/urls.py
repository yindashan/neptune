#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-3-28

@author: jingwen.wu
'''
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^index/$', 'softform.views.index', name="softform_index"),
    url(r'^add/$', 'softform.views.add_softform',name="softform_add"),
    url(r'^delete/(?P<id>\d+)/$', 'softform.views.delete_softform',name="softform_delete"),
    url(r'^selecteddelete/$', 'softform.views.selecteddelete_softform',name="softform_selecteddelete"),
    url(r'^edit/(?P<id>\d+)/$', 'softform.views.edit_softform',name="softform_edit"),
)