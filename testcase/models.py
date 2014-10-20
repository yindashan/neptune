#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-2-28

@author: jingwen.wu
'''
from django.db import models

class Testcase(models.Model):
    '''
    测试用例表
    '''    
    name = models.CharField(max_length = 64)  # 名称。用于区分各测试用例
    content = models.CharField(max_length = 128)  # 内容
    case_type = models.IntegerField(default = 0)  # 0：URL方式；1：测试脚本执行方式；
    
    def __unicode__(self):
        return self.content