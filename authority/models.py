#!usr/bin/env python
#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
    
    
'''功能节点(模块)'''
class Module(models.Model):
    module_name = models.CharField(max_length=64) # 模块名称
    module_type = models.CharField(max_length=64) # 模块类型
    order = models.IntegerField() # 排列顺序
    module_desc = models.CharField(max_length=255) # 模块描述
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 启用时间,添加此机房的时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 禁用时间,停用此机房的时间，格式为'0000-00-00 00:00:00'
    
    def __unicode__(self):
        return self.module_name
    
    class Meta:
        ordering = ('order',)
    
    
'''节点里的字段'''
class ModuleField(models.Model):
    modulefield_name = models.CharField(max_length=64) # 节点里的字段名称
    modulefield_type = models.CharField(max_length=64) # 模块字段类型
    order = models.IntegerField() # 排列顺序
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 启用时间,添加此机房的时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 禁用时间,停用此机房的时间，格式为'0000-00-00 00:00:00'
    
    module = models.ForeignKey(Module) # 节点里的字段与功能节点(模块)多对一关联(外键关联)
    
    def __unicode__(self):
        return self.modulefield_name
    
    class Meta:
        ordering = ('module', 'order', )
    
    
'''功能按钮(添加、修改、删除等)'''
class Button(models.Model):
    button_name = models.CharField(max_length=64) # 按钮名称
    button_type = models.CharField(max_length=64) # 按钮类型
    order = models.IntegerField() # 排列顺序
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 启用时间,添加此机房的时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 禁用时间,停用此机房的时间，格式为'0000-00-00 00:00:00'
    
    module = models.ForeignKey(Module) # 功能按钮(添加、修改、删除等)与功能节点(模块)多对一关联(外键关联)
    
    def __unicode__(self):
        return self.button_name
    
    class Meta:
        ordering = ('module', 'order', )
    

'''角色'''
class Role(models.Model):
    role_name = models.CharField(max_length=64) # 角色名称
    role_desc = models.CharField(max_length=255) # 角色描述
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 启用时间,添加此机房的时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 禁用时间,停用此机房的时间，格式为'0000-00-00 00:00:00'
    
    users = models.ManyToManyField(User) # 角色与用户多对多关联
    modules = models.ManyToManyField(Module) # 角色与功能节点(模块)多对多关联
    buttons = models.ManyToManyField(Button) # 角色与功能按钮(添加、修改、删除等)多对多关联
    modulefields = models.ManyToManyField(ModuleField) # 角色与节点里的字段多对多关联
    
    def __unicode__(self):
        return self.role_name
    
    
    
    
    