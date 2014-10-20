#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-4-2

@author: jingwen.wu
'''

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^index/$', 'schedule.views.index_schedule', name="schedule_index"),
    url(r'^add/$', 'schedule.views.add_schedule',name="schedule_add"),
    url(r'^edit/(?P<id>\d+)/$', 'schedule.views.edit_schedule',name="schedule_edit"),
    url(r'^go/(?P<id>\d+)/$', 'schedule.views.go_schedule',name="schedule_go"),
    url(r'^delete/(?P<id>\d+)/$', 'schedule.views.delete_schedule',name="schedule_delete"),
    url(r'^selecteddelete/$', 'schedule.views.selecteddelete_schedule',name="schedule_selecteddelete"),
    url(r'^detail/(?P<id>\d+)/$', 'schedule.views.detail_schedule',name="schedule_detail"),
    url(r'^log/(?P<id>\d+)/$', 'schedule.views.show_log',name="schedule_log"),
    url(r'^pre_next_log/(?P<id>\d+)/$', 'schedule.views.show_pre_next_log',name="schedule_pre_next_log"),
 
)