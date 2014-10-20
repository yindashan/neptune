#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.defaults import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^index/$', 'server.views.index', name="server_index"),
    url(r'^add/$', 'server.views.add',name="server_add"),
    url(r'^delete/(?P<id>\d+)/$', 'server.views.delete',name="server_delete"),
    url(r'^selecteddelete/$', 'server.views.selecteddelete',name="server_selecteddelete"),
    url(r'^edit/(?P<id>\d+)/$', 'server.views.edit',name="server_edit"),
    url(r'^searchback/$', 'server.views.searchback',name="server_searchback"),
    url(r'^validate/$', 'server.views.validate',name="server_validate"),
#    url(r'^autocomplete/$', 'server.views.autocomplete', name = "server_autocomplete"),

    url(r'^searchback_softform/$', 'server.views.searchback_softform',name="server_searchback_softform"),
    url(r'^searchback_agent/$', 'server.views.searchback_agent',name="server_searchback_agent"),
    
    url(r'^role/$', 'server.views.role',name="server_role"),
    url(r'^getsoftform/$', 'server.views.getsoftform',name="server_getsoftform"),
    
    # setup salt-minion
    url(r'^setup/(?P<id>\d+)/$', 'server.views.setup',name="server_setup"),
    
    # start salt-minion
    url(r'^start/(?P<id>\d+)/$', 'server.views.start',name="server_start"),
    
    # stop salt-minion
    url(r'^stop/(?P<id>\d+)/$', 'server.views.stop',name="server_stop"),
    
    # restart salt-minion
    url(r'^restart/(?P<id>\d+)/$', 'server.views.restart',name="server_restart"),
    
)

