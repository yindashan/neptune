#!usr/bin/env python
#coding: utf-8

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'file.views.upload_file', name = "upload_file"),
    url(r'^upload_file/$', 'file.views.upload_file', name = "upload_file"),
    url(r'^download_file/$', 'file.views.download_file', name = "download_file"),
    
)
