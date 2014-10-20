#!usr/bin/env python
#coding: utf-8
from django.db import models

class ApplyOnline(models.Model):
    applyid = models.CharField(max_length=64) # 申请单号,唯一标识一个申请单
    service_name = models.CharField(max_length=64) # 服务名称
    service_domainname = models.CharField(max_length=64) # 服务域名
    version = models.CharField(max_length=64) # 版本号
    apply_user = models.CharField(max_length=64) # 申请人
    apply_time = models.DateTimeField(blank=True, null=True) # 申请时间，格式为'0000-00-00 00:00:00'
    priority = models.IntegerField(blank=True, null=True) # 优先级，0为紧急，1为一般
    file_name = models.CharField(max_length=128) # 更新文件名
    file_url = models.CharField(max_length=255) # 更新文件下载链接
    online_time = models.DateTimeField(blank=True, null=True) # 计划上线时间，格式为'0000-00-00 00:00:00'
    develop_user = models.CharField(max_length=128) # 相关研发人员
    test_user = models.CharField(max_length=128) # 相关测试人员
    operate_user = models.CharField(max_length=128) # 相关运维人员
    
    # 测试相关
    is_system_test = models.IntegerField(blank=True, null=True) # 系统测试，0为未测试，1为已测试
    is_function_test = models.IntegerField(blank=True, null=True) # 功能测试，0为未测试，1为已测试
    is_capability_test = models.IntegerField(blank=True, null=True) # 性能测试，0为未测试，1为已测试
    is_pressure_test = models.IntegerField(blank=True, null=True) # 压力测试，0为未测试，1为已测试
    is_ui_test = models.IntegerField(blank=True, null=True) # UI测试，0为未测试，1为已测试
    is_special_test = models.IntegerField(blank=True, null=True) # 专项测试，0为未测试，1为已测试
    is_uat_test = models.IntegerField(blank=True, null=True) # 用户接受测试(UAT)，0为未测试，1为已测试
    is_stability_test = models.IntegerField(blank=True, null=True) # 稳定性测试，0为未测试，1为已测试
    is_version_control = models.IntegerField(blank=True, null=True) # 版本控制，0为未控制，1为已控制
    is_train_complete = models.IntegerField(blank=True, null=True) # 培训完成，0为未培训，1为已培训
    is_datatransfer_complete = models.IntegerField(blank=True, null=True) # 数据转换完成，0为未完成数据转换，1为已完成数据转换
    is_document_complete = models.IntegerField(blank=True, null=True) # 文档完整，0为不完整，1为完整
    is_environment_complete = models.IntegerField(blank=True, null=True) # 环境符合要求，0为不符合，1为符合
    is_backup_plan = models.IntegerField(blank=True, null=True) # 是否有回退计划，0为没有，1为有
    is_paramconf_complete = models.IntegerField(blank=True, null=True) # 系统参数配置完成，0为未完成，1为完成
    is_can_online = models.IntegerField(blank=True, null=True) # 可否上线，0为不能上线，1为可上线
    is_check_url = models.IntegerField(blank=True, null=True) # 健康检查url是否变更，0为不变更，1为变更
    check_url = models.CharField(max_length=255, blank=True, null=True) # 新健康检查url
    
    deploy_step = models.CharField(max_length=512, blank=True, null=True) # 部署步骤
    backup_method = models.CharField(max_length=512, blank=True, null=True) # 回滚方案
    update_check = models.CharField(max_length=512, blank=True, null=True) # 更新验证
    applyonline_desc = models.CharField(max_length=512, blank=True, null=True) # 申请上线备注
    
    status = models.IntegerField(default=0) # 申请单状态。“0”为申请，“1”为部署，“2”为成功，“3”为失败，“4”为作废。
    flag = models.IntegerField(default=0) # 删除标志位。“0”为已删除，“1”为未删除。
    
    start_time = models.DateTimeField(u"创建时间", auto_now_add=True) # 创建时间，格式为'0000-00-00 00:00:00'
    end_time = models.DateTimeField(u"修改时间", auto_now=True) # 修改时间，格式为'0000-00-00 00:00:00'
    
    def __unicode__(self):
        return self.applyid
    
    
    
    