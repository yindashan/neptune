#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-3-27

@author: jingwen.wu
'''
from django.db import models

'''
应用包表
'''
class AppPackage(models.Model):
    package_name = models.CharField(max_length=128)  # 应用包名
    down_type = models.IntegerField(default=0)  # 应用包下载方式。0：“http”；1：“ftp”；2：“svn”；3:u"上传"
    down_path = models.CharField(max_length=256)  # 下载路径
    username = models.CharField(max_length=64)  # 用户名。用于获取应用包
    password = models.CharField(max_length=64)  # 密码
    package_path = models.CharField(max_length=128)  # 文件保存路径
    status = models.IntegerField(default=1)  # 应用包状态。0：u“无效”；1：u“有效”；
    desc = models.CharField(max_length=256)  # 说明
    
    def __unicode__(self):
        return self.package_name
    
    