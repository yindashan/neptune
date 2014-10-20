#!usr/bin/env python
#coding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # 根据用户名获取用户所属角色
    url(r'^get_roles/(?P<username>\w+)/$', 'authority.views.get_roles',name="authority_get_roles"),
    
    # 获取所有模块
    url(r'^get_modules/$', 'authority.views.get_modules', name="authority_get_modules"),
    url(r'^get_modules_db/$', 'authority.views.get_modules_db', name="authority_get_modules_db"),
    url(r'^get_buttons/(?P<module_type>\w+)/$', 'authority.views.get_buttons', name="authority_get_buttons"),
    url(r'^get_modulefields/(?P<module_type>\w+)/$', 'authority.views.get_modulefields', name="authority_get_modulefields"),
    
    # 功能节点(模块)
    url(r'^index_module/$', 'authority.views.index_module', name="authority_index_module"),
    url(r'^add_module/$', 'authority.views.add_module',name="authority_add_module"),
    url(r'^delete_module/(?P<id>\d+)/$', 'authority.views.delete_module',name="authority_delete_module"),
    url(r'^selecteddelete_module/$', 'authority.views.selecteddelete_module',name="authority_selecteddelete_module"),
    url(r'^edit_module/(?P<id>\d+)/$', 'authority.views.edit_module',name="authority_edit_module"),

    # 节点里的字段
    url(r'^index_modulefield/$', 'authority.views.index_modulefield', name="authority_index_modulefield"),
    url(r'^add_modulefield/$', 'authority.views.add_modulefield',name="authority_add_modulefield"),
    url(r'^delete_modulefield/(?P<id>\d+)/$', 'authority.views.delete_modulefield',name="authority_delete_modulefield"),
    url(r'^selecteddelete_modulefield/$', 'authority.views.selecteddelete_modulefield',name="authority_selecteddelete_modulefield"),
    url(r'^edit_modulefield/(?P<id>\d+)/$', 'authority.views.edit_modulefield',name="authority_edit_modulefield"),
    
    # 功能按钮(添加、修改、删除等)
    url(r'^index_button/$', 'authority.views.index_button', name="authority_index_button"),
    url(r'^add_button/$', 'authority.views.add_button',name="authority_add_button"),
    url(r'^delete_button/(?P<id>\d+)/$', 'authority.views.delete_button',name="authority_delete_button"),
    url(r'^selecteddelete_button/$', 'authority.views.selecteddelete_button',name="authority_selecteddelete_button"),
    url(r'^edit_button/(?P<id>\d+)/$', 'authority.views.edit_button',name="authority_edit_button"),
    
    # 角色
    url(r'^index_role/$', 'authority.views.index_role', name="authority_index_role"),
    url(r'^add_role/$', 'authority.views.add_role',name="authority_add_role"),
    url(r'^delete_role/(?P<id>\d+)/$', 'authority.views.delete_role',name="authority_delete_role"),
    url(r'^selecteddelete_role/$', 'authority.views.selecteddelete_role',name="authority_selecteddelete_role"),
    url(r'^edit_role/(?P<id>\d+)/$', 'authority.views.edit_role',name="authority_edit_role"),
    
    url(r'^searchback_role_user/$', 'authority.views.searchback_role_user',name="authority_searchback_role_user"),
    
    url(r'^relate_role_user/(?P<id>\d+)/$', 'authority.views.relate_role_user',name="authority_relate_role_user"),
    url(r'^relate_role_module/(?P<id>\d+)/$', 'authority.views.relate_role_module',name="authority_relate_role_module"),
    url(r'^relate_role_button/(?P<id>\d+)/$', 'authority.views.relate_role_button',name="authority_relate_role_button"),
    url(r'^relate_role_modulefield/(?P<id>\d+)/$', 'authority.views.relate_role_modulefield',name="authority_relate_role_modulefield"),
    
    url(r'^autocomplete_module/$', 'authority.views.autocomplete_module', name = "authority_autocomplete_module"),
    url(r'^autocomplete_role/$', 'authority.views.autocomplete_role', name = "authority_autocomplete_role"),
    
)




