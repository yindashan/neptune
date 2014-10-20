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
                "module_name": u"Salt脚本执行",
                "module_type": "saltshell",
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
                "module_name": u"简单脚本执行",
                "module_type": "simpleshell",
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
                "module_name": u"复杂脚本执行",
                "module_type": "compoundshell",
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
                "module_name": u"配置文件管理",
                "module_type": "filemanager",
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
                "module_name": u"软件包管理",
                "module_type": "packagemanager",
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
                "module_name": u"服务器管理",
                "module_type": "server",
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
                            "button_name": u"安装",
                            "button_type": "setup"
                        },
                        {
                            "button_name": u"启动",
                            "button_type": "start"
                        },
                        {
                            "button_name": u"关闭",
                            "button_type": "stop"
                        },
                        {
                            "button_name": u"重启",
                            "button_type": "restart"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"基础应用模板管理",
                "module_type": "softform",
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
                "module_name": u"应用软件包管理",
                "module_type": "apppackage",
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
                "module_name": u"操作模板管理",
                "module_type": "action",
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
                "module_name": u"操作组管理",
                "module_type": "actiongroup",
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
                "module_name": u"上线计划管理",
                "module_type": "schedule",
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
                            "button_name": u"执行",
                            "button_type": "execute"
                        }
                    ]
                },
                "fields": {
                    "field": [
                        
                    ]
                }
            },
            {
                "module_name": u"服务上线申请",
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




