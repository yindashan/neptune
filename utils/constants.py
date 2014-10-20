#!usr/bin/env python
#coding: utf-8
'''
Created on Jun 27, 2012

@author: dashan.yin
'''

# 用户权限字典
account_usertype_dict = {1:u'普通用户', 2:u'普通运维人员', 3:u'运维管理员', 4:u'超级管理员'}

# 机房状态字典
nocinfo_status_dict = {0:u'备用', 1:u'使用', 2:u'报废'}

# 机架状态字典
rack_status_dict = {0:u'备用', 1:u'使用', 2:u'报废'}

# 设备状态字典
equipment_status_dict = {0:u'备用', 1:u'使用', 2:u'报废', 3:u'报修', 4:u'修理', 5:u'闲置', 6:u'待定'}

# IP类型字典
ip_type_dict = {0:u'内网', 1:u'外网'}

# IP状态字典
ip_status_dict = {0:u'备用', 1:u'使用'}

# 日志级别字典
log_level_dict = {0:'DEBUG', 1:'INFO', 2:'WARN', 3:'ERROR'}

# 日志类型字典
log_type_dict = {0:u'其他日志', 1:u'运营商日志', 2:u'机房日志', 3:u'机架日志', 4:u'物理机日志', 5:u'虚拟机日志'}

# 服务上线申请单状态字典
applyonline_status_dict = {0:u'申请', 1:u'待验证', 2:u'成功', 3:u'失败'}

# 资产状态字典
asset_status_dict = {0:u'正常', 1:u'报损', 2:u'待回收'}

# 查询状态字段
inquiry_status_dict = {0: u'在使用', 1: u'已删除', 2: u'全部'}

# 对账标识字典
reconcile_flag_dict = {0:u'无', 1:u'OK', 2:u'盘盈', 3:u'盘亏', 4:u'应调到低耗', 5:u'待财务查找', 6:u'待资产查找', 7:u'待部门查找'}
_reconcile_flag_dict = {u'无':0, u'OK':1, u'盘盈':2, u'盘亏':3, u'应调到低耗':4, u'待财务查找':5, u'待资产查找':6, u'待部门查找':7}
# 资产变动状态字典
assetchange_status_dict = {0:u'退库', 1:u'调配', 2:u'借用', 3:u'新增', 4:u'转移', 5:u'报损', 6:u'盘点'}

# 流程状态字典
flow_state_dict = {0:u'审批完成', 1:u'待发', #A8
             3:u'待处理', 4:u'处理中', 6:u'回退', 7:u'取回',  # A8审批处理中
             5:u'被撤销', 15:u'被终止',  # A8审批非正常结束
             9:u'已创建虚拟机', 19:u'正在创建虚拟机', 29:u'创建虚拟机失败'  #OpenStack创建虚拟机
             }

# 网络资源类型字典
net_type_dict = {0:u'在线机房', 1:u'公司机房'}

# 操作系统类型
os_type_dict = {0:'32位Linux Redhat5.5', 1:'32位Linux Redhat6.0', 
                2:'64位Linux Redhat5.5', 3:'64位Linux Redhat6.0', 
                4:'32位Centos5.5', 5:'32位Centos6.0', 
                6:'64位Centos5.5', 7:'64位Centos6.0', 
                8:'32位 Windows7', 9:'64位Windows7', 
                10: '32位centos-i386', 11:'4位centos',
                12:'64位WindowsServer2008', 13:'64位cirros-0.3.0-x86_64',
                13:'64位min-centos-64bit'}



# 应用软件包下载方式
down_type_dict = {0:'http', 1:'ftp', 2:'svn', 3:u'上传'}

# 执行状态
executive_state_dict = {0: u'全部', 1: u'已建单', 2: u'灰度执行中', 3: u'全上执行中', 4: u'灰度完成', 
                        5: u'全上完成', 6: u'灰度回退完成', 7: u'全上回退完成', 8: u'灰度中断', 
                        9: u'全上中断', 10: u'灰度回退失败', 11: u'全上回退失败'}

# 测试用例测试方式
case_type_dict = {0:u'URL方式', 1:u'测试脚本执行方式'}


# salt-minion statsu
salt_status_dict = {0:u'全部', 1:u'未安装', 2:u'运行中', 3:u'停用'}




