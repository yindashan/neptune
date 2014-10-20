#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-2-28

@author: jingwen.wu
'''
from django.db import models

from server.models import Server
from softform.models import SoftForm
from apppackage.models import AppPackage
from action.models import ActionGroup
from testcase.models import Testcase
    
class Schedule(models.Model):
    '''
    上线计划表
    '''    
    schedule_id = models.CharField(max_length = 64, unique = True)  # 上线计划单号。唯一标识
    service_name = models.CharField(max_length = 64)  # 服务名称。唯一标识
    server_group = models.ManyToManyField(Server, related_name = 'server_group+')  # 服务器组
    softform_group = models.ManyToManyField(SoftForm, related_name = 'softform_group+')  # 基础应用模板组
    apppackage_group = models.ManyToManyField(AppPackage, related_name = 'apppckage_group+')  # 应用服务组
    actiongroups = models.ManyToManyField(ActionGroup, related_name = 'actiongroup+')  # 操作流程
    testcase_group = models.ManyToManyField(Testcase, related_name='testcase_group+')  # 测试用例组
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)  # 创建时间，格式为'0000-00-00 00:00:00'
    start_time = models.DateTimeField(blank=True, null=True)  # 执行开始时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(blank=True, null=True)  # 执行结束时间，格式为'0000-00-00 00:00:00'
    executive_state = models.IntegerField(default = 0)  # 执行状态。0：已建单；1：灰度执行中:2：全上执行中；3：灰度完成；4：全上完成；5：灰度回退完成；6：全上回退完成；7：灰度中断；8：全上中断；9：灰度回退失败；10：全上回退失败；
    auto_rollback = models.IntegerField(default = 0)  # 自动回滚标识。 0：自动回滚；1：不自动回滚；
    department_dep = models.CharField(max_length = 64)  # 研发部门
    contact = models.CharField(max_length = 32)  # 联系人
    contact_info = models.CharField(max_length = 64)  # 联系信息
    department = models.CharField(max_length = 64)  # 上线部署部门
    user_name = models.CharField(max_length = 32)  # 操作人员
    
    def __unicode__(self):
        return self.schedule_id
    

class ScheduleLog(models.Model):
    '''
    上线计划执行日志
    '''
    log_name = models.CharField(max_length = 64)  # 日志名称
    schedule_id = models.CharField(max_length = 64)  # 上线计划单号。唯一标识
    create_time = models.DateTimeField(u"记录时间", auto_now_add=True)  # 记录时间，格式为'0000-00-00 00:00:00'
    state = models.IntegerField(default = 0)  # 标识此日志是否可显示。state=0，可显示，state=1，与此日志关联的schedule被删除，日志不能显示。
    pre_id = models.IntegerField(default = 0)  # 上一个日志的id
    next_id = models.IntegerField(default = 0)  # 下一个日志的id
    
    def __unicode__(self):
        return self.log_name