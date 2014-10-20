#!usr/bin/env python
#coding: utf-8
from django.db import models

class Log(models.Model):
    
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 创建时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 修改时间，格式为'0000-00-00 00:00:00'
    username = models.CharField(max_length=64) # 操作用户名称
    content = models.CharField(max_length=255) # 操作内容
    log_type = models.IntegerField(default=0) # 日志类型。0:'其他日志', 1:'机房日志', 2:'机架日志', 3:'物理机日志', 4:'虚拟机日志'
    relate_id = models.IntegerField(null=True) # 关联主键id
    sequence = models.CharField(max_length=64) # 序列号
    level = models.IntegerField(default=1) # 日志级别。“0”为DEBUG，“1”为INFO，“2”为WARN，“3”为ERROR
    
    def __unicode__(self):
        return self.username
    


