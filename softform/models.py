#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-3-27

@author: jingwen.wu

'''

from django.db import models

class SoftForm(models.Model):
    '''
    基础应用模板表
    '''    
    soft_type = models.CharField(max_length = 32)  # 软件类型。如，apache
    soft_name = models.CharField(max_length = 64)  # 软件包名称。如，httpd
    version = models.CharField(max_length = 64)  # 版本
    os = models.CharField(max_length = 32)  # 运行所需操作系统
    os_byte = models.CharField(max_length = 16)  # 操作系统位数
    os_version = models.CharField(max_length = 32)  # 操作系统版本
    
    def __unicode__(self):
        return self.soft_name    
