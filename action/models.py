#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-2-28

@author: jingwen.wu
'''
from django.db import models

class Action(models.Model):
    '''
    原子操作表
    '''
    action_type = models.CharField(max_length = 64)  # 类型。如，apache,lse    
    name = models.CharField(max_length = 64, unique = True)  # 名称。如，LSE4部署。
    run_os = models.CharField(max_length = 64)  # 操作正常执行所需的操作系统
    action_cmd = models.CharField(max_length = 512)  # 操作
    
    def __unicode__(self):
        return self.name
    
class ActionGroup(models.Model):
    '''
    操作流程表
    '''
    name = models.CharField(max_length = 64, unique = True)  # 名称
    desc = models.CharField(max_length = 128)  # 分组说明
    
    def __unicode__(self):
        return self.name
    
class ActionOrder(models.Model):
    '''
    操作次序表
    '''
    action = models.ForeignKey(Action)  # 原子操作
    group = models.ForeignKey(ActionGroup)  # 操作流程组
    order = models.IntegerField()  # 序列号，从0开始记录
    
    def __unicode__(self):
        return unicode(self.order)