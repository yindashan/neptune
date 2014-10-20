#!usr/bin/env python
#coding: utf-8

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # LDAP
    url(r'^index_ldapconf/$', 'dynamicconf.views.index_ldapconf', name="dynamicconf_index_ldapconf"),
    url(r'^add_ldapconf/$', 'dynamicconf.views.add_ldapconf',name="dynamicconf_add_ldapconf"),
    url(r'^delete_ldapconf/(?P<id>\d+)/$', 'dynamicconf.views.delete_ldapconf',name="dynamicconf_delete_ldapconf"),
    url(r'^edit_ldapconf/(?P<id>\d+)/$', 'dynamicconf.views.edit_ldapconf',name="dynamicconf_edit_ldapconf"),
    
    # OpenStack
    url(r'^index_openstackconf/$', 'dynamicconf.views.index_openstackconf', name="dynamicconf_index_openstackconf"),
    url(r'^add_openstackconf/$', 'dynamicconf.views.add_openstackconf',name="dynamicconf_add_openstackconf"),
    url(r'^delete_openstackconf/(?P<id>\d+)/$', 'dynamicconf.views.delete_openstackconf',name="dynamicconf_delete_openstackconf"),
    url(r'^edit_openstackconf/(?P<id>\d+)/$', 'dynamicconf.views.edit_openstackconf',name="dynamicconf_edit_openstackconf"),
    
    # A8
    url(r'^index_a8conf/$', 'dynamicconf.views.index_a8conf', name="dynamicconf_index_a8conf"),
    url(r'^add_a8conf/$', 'dynamicconf.views.add_a8conf',name="dynamicconf_add_a8conf"),
    url(r'^delete_a8conf/(?P<id>\d+)/$', 'dynamicconf.views.delete_a8conf',name="dynamicconf_delete_a8conf"),
    url(r'^edit_a8conf/(?P<id>\d+)/$', 'dynamicconf.views.edit_a8conf',name="dynamicconf_edit_a8conf"),

)