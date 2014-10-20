#!usr/bin/env python
#coding: utf-8

from django.db import models

class LDAPConf(models.Model):
    server = models.CharField(max_length=64) # server地址
    base_dn = models.CharField(max_length=64) # Base DN值
    domainname = models.CharField(max_length=64) # 域名
    loginname = models.CharField(max_length=64) # 登录名
    username = models.CharField(max_length=64) # 用户名
    password = models.CharField(max_length=64) # 密码
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 启用时间,添加此机房的时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 禁用时间,停用此机房的时间，格式为'0000-00-00 00:00:00'
    
    def __unicode__(self):
        return self.server
    
    
class OpenStackConf(models.Model):
    username = models.CharField(max_length=64) # 用户名
    password = models.CharField(max_length=64) # 密码
    tenant_name = models.CharField(max_length=64)
    auth_url = models.CharField(max_length=64)
    computer_api_version = models.CharField(max_length=64)
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 启用时间,添加此机房的时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 禁用时间,停用此机房的时间，格式为'0000-00-00 00:00:00'
    
    def __unicode__(self):
        return self.username
    
    
class A8Conf(models.Model):
    url = models.CharField(max_length=64) # server地址
    username = models.CharField(max_length=64) # 用户名
    password = models.CharField(max_length=64) # 密码
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 启用时间,添加此机房的时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 禁用时间,停用此机房的时间，格式为'0000-00-00 00:00:00'
    
    def __unicode__(self):
        return self.url

