#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-4-2

@author: jingwen.wu
'''

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # 操作模板
    url(r'^index/$', 'action.views.index_action', name="action_index"),
    url(r'^add/$', 'action.views.add_action',name="action_add"),
    url(r'^edit/(?P<id>\d+)/$', 'action.views.edit_action',name="action_edit"),
    url(r'^delete/(?P<id>\d+)/$', 'action.views.delete_action',name="action_delete"),
    url(r'^selecteddelete/$', 'action.views.selecteddelete_action',name="action_selecteddelete"),
    url(r'^detail/(?P<id>\d+)/$', 'action.views.detail_action',name="action_detail"),
    
    # 操作组
    url(r'^index_actiongroup/$', 'action.views.index_actiongroup', name="actiongroup_index"), 
    url(r'^add_actiongroup/$', 'action.views.add_actiongroup',name="actiongroup_add"),
    url(r'^edit_actiongroup/(?P<id>\d+)/$', 'action.views.edit_actiongroup',name="actiongroup_edit"),
    url(r'^delete_actiongroup/(?P<id>\d+)/$', 'action.views.delete_actiongroup',name="actiongroup_delete"),
    url(r'^selecteddelete_actiongroup/$', 'action.views.selecteddelete_actiongroup',name="actiongroup_selecteddelete"),  
    url(r'^detail_actiongroup/(?P<id>\d+)/$', 'action.views.detail_actiongroup',name="actiongroup_detail"),
    
)