#!usr/bin/env python
#coding: utf-8
'''
Created on Dec 19, 2012

@author: dashan.yin
'''
# 权限相关json格式数据
authority_data = {
    "modules": {
        "module": [
            {
                "module_name": u"运营商管理",
                "module_type": "isp",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        {
                            "field_name": u"运营商地址",
                            "field_type": "address"
                        },
                        {
                            "field_name": u"客服电话",
                            "field_type": "phone1"
                        },
                        {
                            "field_name": u"常用电话",
                            "field_type": "phone2"
                        }
                    ]
                }
            },
            {
                "module_name": u"机房管理",
                "module_type": "nocinfo",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        {
                            "field_name": u"机房地址",
                            "field_type": "address"
                        },
                        {
                            "field_name": u"机房联系人",
                            "field_type": "noc_username"
                        },
                        {
                            "field_name": u"联系方式",
                            "field_type": "phone"
                        }
                    ]
                }
            },
            {
                "module_name": u"机房网络管理",
                "module_type": "nocnetinfo",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        {
                            "field_name": u"子网掩码",
                            "field_type": "ip_mark"
                        },
                        {
                            "field_name": u"默认网关",
                            "field_type": "gateway"
                        },
                        {
                            "field_name": u"本地DNS1",
                            "field_type": "ldns1"
                        },
                        {
                            "field_name": u"本地DNS2",
                            "field_type": "ldns2"
                        }
                    ]
                }
            },
            {
                "module_name": u"机架管理",
                "module_type": "rack",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        {
                            "field_name": u"机架额定电流",
                            "field_type": "rated_amp"
                        },
                        {
                            "field_name": u"机架已使用电流",
                            "field_type": "used_amp"
                        },
                        {
                            "field_name": u"机架总空间",
                            "field_type": "space"
                        },
                        {
                            "field_name": u"机架剩余空间",
                            "field_type": "left_space"
                        }
                    ]
                }
            },
            {
                "module_name": u"设备管理",
                "module_type": "equipment",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        },
                        {
                            "button_name": u"超级管理",
                            "button_type": "super"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        {
                            "field_name": u"设备序列号",
                            "field_type": "sequence"
                        },
                        {
                            "field_name": u"售后编号",
                            "field_type": "service_no"
                        },
                        {
                            "field_name": u"采购时间",
                            "field_type": "buy_time"
                        },
                        {
                            "field_name": u"保修期限",
                            "field_type": "deadline"
                        }
                    ]
                }
            },
            {
                "module_name": u"服务器配置管理",
                "module_type": "serverconf",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        {
                            "field_name": u"管理帐号",
                            "field_type": "manage_account"
                        },
                        {
                            "field_name": u"管理密码",
                            "field_type": "manage_password"
                        },
                        {
                            "field_name": u"管理IP",
                            "field_type": "manage_ip"
                        },
                        {
                            "field_name": u"管理端口",
                            "field_type": "manage_port"
                        }
                    ]
                }
            },
            {
                "module_name": u"虚拟机管理",
                "module_type": "virtualmachine",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        },
                        {
                            "button_name": u"超级管理",
                            "button_type": "super"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        {
                            "field_name": u"管理帐号",
                            "field_type": "manage_account"
                        },
                        {
                            "field_name": u"管理密码",
                            "field_type": "manage_password"
                        },
                        {
                            "field_name": u"管理端口",
                            "field_type": "manage_port"
                        }
                    ]
                }
            },
            {
                "module_name": u"IP管理",
                "module_type": "ippool",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        {
                            "field_name": u"子网掩码",
                            "field_type": "ipMask"
                        }
                    ]
                }
            },
            {
                "module_name": u"申请资源管理",
                "module_type": "applyresource",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "field_name": u"申请",
                            "field_type": "apply"
                        },
                        {
                            "field_name": u"查看详情",
                            "field_type": "detail"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"组织机构管理",
                "module_type": "organization",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"固定资产管理",
                "module_type": "asset",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"报损",
                            "button_type": "damage"
                        },
                        {
                            "button_name": u"借用",
                            "button_type": "lend"
                        },
                        {
                            "button_name": u"调配",
                            "button_type": "distribute"
                        },
                        {
                            "button_name": u"转移",
                            "button_type": "transfer"
                        },
                        {
                            "button_name": u"退库",
                            "button_type": "withdraw"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"报损资产管理",
                "module_type": "assetdamage",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"待回收资产管理",
                "module_type": "assetrecover",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"资产变动管理",
                "module_type": "assetchange",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"资产账管理",
                "module_type": "assetaccount",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"设备代码管理",
                "module_type": "equipmentcode",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"公司代码管理",
                "module_type": "companycode",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"部门代码管理",
                "module_type": "departmentcode",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"导入",
                            "button_type": "import"
                        },
                        {
                            "button_name": u"导出",
                            "button_type": "export"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"动态配置管理",
                "module_type": "dynamicconf",
                "buttons": {
                    "button": [
                        
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"帐号管理",
                "module_type": "account",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        },
                        {
                            "button_name": u"添加",
                            "button_type": "add"
                        },
                        {
                            "button_name": u"修改",
                            "button_type": "edit"
                        },
                        {
                            "button_name": u"删除",
                            "button_type": "delete"
                        },
                        {
                            "button_name": u"超级管理",
                            "button_type": "superuser"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"权限管理",
                "module_type": "authority",
                "buttons": {
                    "button": [
                        
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"日志管理",
                "module_type": "log",
                "buttons": {
                    "button": [
                        {
                            "button_name": u"查询",
                            "button_type": "select"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            }
                   
                   
                   
                   
                   
                   
                   
        ]
    }
}




