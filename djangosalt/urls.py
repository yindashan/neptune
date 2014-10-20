# -*- coding: utf-8 -*-

from djangosalt.utils import REGEX_JID, REGEX_HOSTNAME

from django.conf.urls import patterns, url

urlpatterns = patterns('djangosalt.views',
    url(r'^$', 'apiwrapper'),
    
    url(r'^salt_shell/$', 'salt_shell', name="djangosalt_salt_shell"),
    url(r'^simple_shell/$', 'simple_shell', name="djangosalt_simple_shell"),
    url(r'^compound_shell/$', 'compound_shell', name="djangosalt_compound_shell"),
    url(r'^file_manager/$', 'file_manager', name="djangosalt_file_manager"),
    url(r'^package_manager/$', 'package_manager', name="djangosalt_package_manager"),
    url(r'^searchback/$', 'searchback',name="djangosalt_searchback"),
    
    
    url(r'^index/$', 'index', name="djangosalt_index"),
    url(r'^testping/(?P<tgt>' + REGEX_HOSTNAME + ')/$', 'testping', name="djangosalt_testping"),
    url(r'^postping/$', 'postping', name="djangosalt_postping"),
    url(r'^testpostping/$', 'testpostping', name="djangosalt_testpostping"),
    
    url(r'^minions/$', 'minions_list'),
    url(r'^minions/(?P<tgt>' + REGEX_HOSTNAME + ')/$', 'minions_details'),

    url(r'^jobs/$', 'jobs_list'),
    url(r'^jobs/(?P<jid>' + REGEX_JID + ')/$', 'jobs_details'),

    url(r'^ping/(?P<tgt>' + REGEX_HOSTNAME + ')/$', 'ping'),
    url(r'^pingoutput/(?P<tgt>' + REGEX_HOSTNAME + ')/$', 'pingoutput'),
    url(r'^echo/(?P<tgt>' + REGEX_HOSTNAME + ')/(?P<arg>\w+)/$', 'echo'),
)
