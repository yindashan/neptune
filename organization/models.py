#!usr/bin/env python
#coding: utf-8

from django.db import models

class Organization(models.Model):
    organization_name = models.CharField(max_length=64) # 组织结构名称
    organization_desc = models.CharField(max_length=64, blank=True)  # 组织结构描述
    level = models.IntegerField(default=0) # 组织机构级别。0为高德集团
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 启用时间,添加此机房的时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 禁用时间,停用此机房的时间，格式为'0000-00-00 00:00:00'
    
    parent_organization = models.ForeignKey('self', null=True) # 多对一递归自关联
    
    def __unicode__(self):
        return self.organization_name
    
    class Meta:
        ordering = ('level',)

