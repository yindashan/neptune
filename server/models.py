#!usr/bin/env python
#coding: utf-8
from django.db import models
from softform.models import SoftForm
'''
    服务器管理表
'''
class Server(models.Model):
    nocid = models.CharField(max_length=64) # 机房编号
    nocname = models.CharField(max_length=64) # 机房名称
    elementid = models.CharField(max_length=64) # 资产编号
    saltid = models.CharField(max_length=64) # saltID。唯一标识
    in_ip = models.CharField(max_length=64) # 内网IP
    out_ip = models.CharField(max_length=64) # 外网IP
    manage_account = models.CharField(max_length=64) # 管理帐号
    manage_password = models.CharField(max_length=64) # 管理密码
    manage_port = models.IntegerField(blank=True, null=True, default=22) # 管理端口
    service_name = models.CharField(max_length=128)  # 服务名称
    virtual_flag = models.IntegerField(blank=True, null=True)  # 标记是否为虚拟机。0：虚拟机；1：物理机；
    salt_status = models.IntegerField(blank=True, null=True)  # salt返回状态。0：未安装；1：运行中；2：停用
    status = models.IntegerField(blank=True, null=True)  # 运行状态。0：正常；1：备用；2：停用；
    agent_flag = models.IntegerField(default=0)  # 标记是否需要代理才能ping通。0：不需要；1：需要；
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 创建时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 修改时间，格式为'0000-00-00 00:00:00'
    
    softforms = models.ManyToManyField(SoftForm)  # 软件组。记录此服务器上安装的所有公共软件
    agent_server = models.ForeignKey('self', null=True) # 多对一递归自关联
    
    def __unicode__(self):
        return self.saltid
    
    
    
    