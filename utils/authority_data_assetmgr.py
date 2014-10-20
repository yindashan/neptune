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
                            "button_name": u"解锁",
                            "button_type": "unlock"
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
                            "button_name": u"导出",
                            "button_type": "export"
                        },
                        {
                            "button_name": u"恢复",
                            "button_type": "revert"
                        },
                        {
                            "button_name": u"回收",
                            "button_type": "recover"
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
                "module_name": u"服务上线管理",
                "module_type": "applyonline",
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
                            "button_name": u"管理",
                            "button_type": "manage"
                        },
                        {
                            "button_name": u"部署",
                            "button_type": "deploy"
                        },
                        {
                            "button_name": u"验证",
                            "button_type": "validate"
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




