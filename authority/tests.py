#coding: utf-8
'''
Created on 2012-5-30

@author: jingwen.wu
'''
#from django.db import models
import json
from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from account.models import UserProfile
from django.contrib.auth.hashers import *
from account.views import login


#表信息
class authorityTableTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        password = make_password('admin', salt=None, hasher='default')
        user = User(username='admin', password=password, email='admin@admin.com')
        user.save();
        userprofile = UserProfile(user=user, department='admin', phone='admin')
        userprofile.save()
        #系统自带的login函数，不会触发自定义的login函数
#        self.client.login(username='admin', password='admin')
        self.client.post('/account/login/', {'username':'admin', 'password':'admin'})
    
    def test_authority_index_table(self):
        authorityTableStatus = self.client.post('/authority/index_table/')
        self.assertEqual(authorityTableStatus.status_code, 200)
    def test_authority_index_table5(self):
        authorityTableStatus = self.client.post('/authority/index_table/',{'q':'5'})
        self.assertEqual(authorityTableStatus.status_code, 200) 
    
    def test_authority_add_table(self):
        authorityTableStatus = self.client.post('/authority/add_table/',{'table_name':'管理', 'table_desc':'申请资源'})
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '添加成功')
            
    def test_authority_add_reapet_table(self):
        authorityTableStatus = self.client.post('/authority/add_table/',{'table_name':'管理', 'table_desc':'申请资源'})
        authorityTableStatus = self.client.post('/authority/add_table/',{'table_name':'管理', 'table_desc':'申请资源'})
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '表名已经存在不能添加')
          
    def test_authority_delete_table_error(self):
        for i in range(10): 
            self.client.post('/authority/add_table/',{'table_name':'管理' + str(i), 'table_desc':'申请资源'})
        self.client.post('/authority/add_field/',{'org.table_name':'管理1', 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        authorityTableStatus=self.client.post('/authority/delete_table/2/')
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '该表下面有所属字段不能删除')

    def test_authority_delete_table(self):
        for i in range(10): 
            self.client.post('/authority/add_table/',{'table_name':'管理' + str(i), 'table_desc':'申请资源'})
        authorityTableStatus=self.client.post('/authority/delete_table/2/')
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')
    
    def test_authority_selecteddelete_table(self):
        for i in range(10): 
            self.client.post('/authority/add_table/',{'table_name':'管理' + str(i), 'table_desc':'申请资源'})
        authorityTableStatus=self.client.post('/authority/selecteddelete_table/',{'ids':'1,2,3,5'})
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '选中项删除成功')

    def test_authority_selecteddelete_table_error(self):
        for i in range(10): 
            self.client.post('/authority/add_table/',{'table_name':'管理' + str(i), 'table_desc':'申请资源'})
        #添加table关联字段
        self.client.post('/authority/add_field/',{'org.table_name':'管理1', 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        authorityTableStatus=self.client.post('/authority/selecteddelete_table/',{'ids':'1,2,3,5'})
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '选中表下面有所属字段不能批量删除')

      
    def test_authority_edit_table(self):
        for i in range(10): 
            self.client.post('/authority/add_table/',{'table_name':'管理' + str(i), 'table_desc':'申请资源'})
        authorityTableStatus = self.client.post('/authority/edit_table/4/',{'table_name':'申请资源', 'table_desc':'管理资源'})
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '编辑成功')



#字段信息
class authorityFieldTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        password = make_password('admin', salt=None, hasher='default')
        user = User(username='admin', password=password, email='admin@admin.com')
        user.save();
        userprofile = UserProfile(user=user, department='admin', phone='admin')
        userprofile.save()
        #系统自带的login函数，不会触发自定义的login函数
#        self.client.login(username='admin', password='admin')
        self.client.post('/account/login/', {'username':'admin', 'password':'admin'})
        
        for i in range(10): 
            self.client.post('/authority/add_table/',{'table_name':'管理' + str(i), 'table_desc':'申请资源'})
            
    def test_authority_index_field(self):
        authorityFieldStatus = self.client.post('/authority/index_field/')
        self.assertEqual(authorityFieldStatus.status_code, 200)
    def test_authority_index_field5(self):
        authorityFieldStatus = self.client.post('/authority/index_field/',{'q':'5'})
        self.assertEqual(authorityFieldStatus.status_code, 200) 
    
    def test_authority_add_field(self):
        authorityFieldStatus = self.client.post('/authority/add_field/',{'org.table_name':'管理1', 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        data = json.loads(authorityFieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '添加成功')
    
        
    def test_authority_add_error_field(self):
        authorityFieldStatus = self.client.post('/authority/add_field/',{'org.table_name':'', 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        data = json.loads(authorityFieldStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '表名为空不能添加')

    def test_authority_delete_field(self):
        for i in range(10):
            self.client.post('/authority/add_field/',{'org.table_name':'管理' + str(i), 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        authorityFieldStatus=self.client.post('/authority/delete_field/2/')
        data = json.loads(authorityFieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')
        
    def test_authority_delete_field_error(self):
        for i in range(10):
            self.client.post('/authority/add_field/',{'org.table_name':'管理' + str(i), 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        #添加模块
        self.client.post('/authority/add_module/',{'module_name':'管理', 'module_type':'管理机房', 'order':'2', 'module_desc':'3'})
        #添加模块关联此字段
        self.client.post('/authority/add_modulefield/',{'modulefield_name':'modulefield_name', 'modulefield_type':'modulefield_type', 'order':'2', 'org1.module_name':'管理', 'org2.field_id':'2'})
        authorityTableStatus=self.client.post('/authority/delete_field/2/')
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '该字段跟模块字段关联不能删除')
    
    def test_authority_selecteddelete_field(self):
        for i in range(10): 
            self.client.post('/authority/add_field/',{'org.table_name':'管理' + str(i), 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        authorityTableStatus=self.client.post('/authority/selecteddelete_field/',{'ids':'1,2,3,5'})
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '选中项删除成功')
        
    def test_authority_selecteddelete_field_error(self):
        for i in range(10): 
            self.client.post('/authority/add_field/',{'org.table_name':'管理' + str(i), 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        #添加模块
        self.client.post('/authority/add_module/',{'module_name':'管理', 'module_type':'管理机房', 'order':'2', 'module_desc':'3'})
        #添加模块关联此字段
        self.client.post('/authority/add_modulefield/',{'modulefield_name':'modulefield_name', 'modulefield_type':'modulefield_type', 'order':'2', 'org1.module_name':'管理', 'org2.field_id':'2'})
        authorityTableStatus=self.client.post('/authority/selecteddelete_field/',{'ids':'1,2,3,5'})
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], u'选中字段跟模块字段关联不能批量删除')

    def test_authority_edit_field(self):
        for i in range(10): 
            self.client.post('/authority/add_field/',{'org.table_name':'管理' + str(i), 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        authorityTableStatus = self.client.post('/authority/edit_field/2/',{'org.table_name':'管理2', 'field_name':'管理机房2', 'field_type':'申请资源', 'field_size':'修改', 'field_desc':'申请资源4'})
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], u'编辑成功')


        

#模块信息
class authorityModuleTest(TestCase):    
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        password = make_password('admin', salt=None, hasher='default')
        user = User(username='admin', password=password, email='admin@admin.com')
        user.save();
        userprofile = UserProfile(user=user, department='admin', phone='admin')
        userprofile.save()
        #系统自带的login函数，不会触发自定义的login函数
#        self.client.login(username='admin', password='admin')
        self.client.post('/account/login/', {'username':'admin', 'password':'admin'})
        
    def test_authority_index_module(self):
        authorityModuleStatus = self.client.post('/authority/index_module/')
        self.assertEqual(authorityModuleStatus.status_code, 200)
    def test_authority_index_module5(self):
        authorityModuleStatus = self.client.post('/authority/index_module/',{'q':'5'})
        self.assertEqual(authorityModuleStatus.status_code, 200)
    
    def test_authority_add_module(self):
        authorityModuleStatus = self.client.post('/authority/add_module/',{'module_name':'模块', 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
        data = json.loads(authorityModuleStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '添加成功')
           
    def test_authority_add_repeat_module(self):
        self.client.post('/authority/add_module/',{'module_name':'模块', 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
        authorityModuleStatus = self.client.post('/authority/add_module/',{'module_name':'模块', 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
        data = json.loads(authorityModuleStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '模块名已经存在不能添加')
    
    def test_authority_delete_module(self):
        for i in range(10):
            self.client.post('/authority/add_module/',{'module_name':'模块' + str(i), 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
        authorityModuleStatus=self.client.post('/authority/delete_module/2/')
        data = json.loads(authorityModuleStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')
        
    def test_authority_delete_module_error1(self):
        for i in range(10):
            self.client.post('/authority/add_module/',{'module_name':'模块' + str(i), 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
        #添加按钮
        self.client.post('/authority/add_button/',{'org.module_name':'模块1', 'button_name':'按钮', 'button_type':'2', 'order':'3'})
        authorityModuleStatus=self.client.post('/authority/delete_module/2/')
        data = json.loads(authorityModuleStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '该模块下面有关联按钮不能删除')
        
    def test_authority_delete_module_error2(self):
        for i in range(10):
            self.client.post('/authority/add_module/',{'module_name':'模块' + str(i), 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
        #添加表
        self.client.post('/authority/add_table/',{'table_name':'管理', 'table_desc':'申请资源'})
        #添加字段
        self.client.post('/authority/add_field/',{'org.table_name':'管理', 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        #添加模块字段关联此模块
        self.client.post('/authority/add_modulefield/',{'modulefield_name':'modulefield_name', 'modulefield_type':'modulefield_type', 'order':'2', 'org1.module_name':'模块5', 'org2.field_id':'1'})
        authorityModuleStatus=self.client.post('/authority/delete_module/6/')
        data = json.loads(authorityModuleStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '该模块下面有关联模块字段不能删除')

    def test_authority_selecteddelete_module(self):
        for i in range(10): 
            self.client.post('/authority/add_module/',{'module_name':'模块' + str(i), 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
        authorityModuleStatus=self.client.post('/authority/selecteddelete_module/',{'ids':'1,2,3,5'})
        data = json.loads(authorityModuleStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '选中项删除成功')
    
    def test_authority_selecteddelete_module_error1(self):
        for i in range(10):
            self.client.post('/authority/add_module/',{'module_name':'模块' + str(i), 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
        #添加按钮
        self.client.post('/authority/add_button/',{'org.module_name':'模块1', 'button_name':'按钮', 'button_type':'2', 'order':'3'})
        authorityModuleStatus=self.client.post('/authority/selecteddelete_module/',{'ids':'1,2,3,6'})
        data = json.loads(authorityModuleStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '选中模块下面有关联按钮不能批量删除')
        
    def test_authority_selecteddelete_module_error2(self):
        for i in range(10): 
            self.client.post('/authority/add_module/',{'module_name':'模块' + str(i), 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
        #添加表
        self.client.post('/authority/add_table/',{'table_name':'管理', 'table_desc':'申请资源'})
        #添加字段
        self.client.post('/authority/add_field/',{'org.table_name':'管理', 'field_name':'管理机房', 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        #添加模块字段关联此模块
        self.client.post('/authority/add_modulefield/',{'modulefield_name':'modulefield_name', 'modulefield_type':'modulefield_type', 'order':'2', 'org1.module_name':'模块5', 'org2.field_id':'1'})
        authorityModuleStatus=self.client.post('/authority/selecteddelete_module/',{'ids':'1,2,3,6'})
        data = json.loads(authorityModuleStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '选中模块下面有关联模块字段不能批量删除')
        
    def test_authority_edit_module(self):
        for i in range(10): 
            self.client.post('/authority/add_module/',{'module_name':'模块' + str(i), 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
        authorityTableStatus = self.client.post('/authority/edit_module/2/',{'module_name':'模块', 'module_type':'模块2', 'order':'3', 'module_desc':'模块管理aa'})
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], u'编辑成功')
        
        
#模块字段信息
class authorityModulefieldTest(TestCase):    
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        password = make_password('admin', salt=None, hasher='default')
        user = User(username='admin', password=password, email='admin@admin.com')
        user.save();
        userprofile = UserProfile(user=user, department='admin', phone='admin')
        userprofile.save()
        #系统自带的login函数，不会触发自定义的login函数
#        self.client.login(username='admin', password='admin')
        self.client.post('/account/login/', {'username':'admin', 'password':'admin'})
        
        #添加表
        for i in range(10):
            self.client.post('/authority/add_table/',{'table_name':'管理' + str(i), 'table_desc':'申请资源'})
        #添加字段
        for i in range(10):
            self.client.post('/authority/add_field/',{'org.table_name':'管理' + str(i), 'field_name':'管理机房' + str(i), 'field_type':'申请资源', 'field_size':'3', 'field_desc':'申请资源'})
        #添加模块
        for i in range(10): 
            self.client.post('/authority/add_module/',{'module_name':'模块' + str(i), 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})

    def test_authority_index_modulefield(self):
        authorityModulefieldStatus = self.client.post('/authority/index_modulefield/')
        self.assertEqual(authorityModulefieldStatus.status_code, 200)
    def test_authority_index_modulefield5(self):
        authorityModulefieldStatus = self.client.post('/authority/index_modulefield/',{'q':'5'})
        self.assertEqual(authorityModulefieldStatus.status_code, 200)
    
    def test_authority_add_modulefield(self):
        authorityModulefieldStatus = self.client.post('/authority/add_modulefield/',{'modulefield_name':'modulefield_name', 'modulefield_type':'modulefield_type', 'order':'2', 'org1.module_name':'模块5', 'org2.field_id':'1'})
        data = json.loads(authorityModulefieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '添加成功')
           
    def test_authority_add_modulefield_error1(self):
        authorityModulefieldStatus = self.client.post('/authority/add_modulefield/',{'modulefield_name':'modulefield_name', 'modulefield_type':'modulefield_type', 'order':'2', 'org1.module_name':'', 'org2.field_id':'1'})
        data = json.loads(authorityModulefieldStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '关联模块为空不能添加')
    def test_authority_add_modulefield_error2(self):
        authorityModulefieldStatus = self.client.post('/authority/add_modulefield/',{'modulefield_name':'modulefield_name', 'modulefield_type':'modulefield_type', 'order':'2', 'org1.module_name':'模块5', 'org2.field_id':''})
        data = json.loads(authorityModulefieldStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '关联字段为空不能添加')
    
    def test_authority_delete_modulefield(self):
        for i in range(10):
            self.client.post('/authority/add_modulefield/',{'modulefield_name':'modulefield_name', 'modulefield_type':'modulefield_type', 'order':'2', 'org1.module_name':'模块5', 'org2.field_id':'1'})
        authorityModulefieldStatus=self.client.post('/authority/delete_modulefield/2/')
        data = json.loads(authorityModulefieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')
    
    def test_authority_edit_field(self):
        for i in range(10): 
            self.client.post('/authority/add_modulefield/',{'modulefield_name':'modulefield_name', 'modulefield_type':'modulefield_type', 'order':'2', 'org1.module_name':'模块5', 'org2.field_id':'1'})
        authorityTableStatus = self.client.post('/authority/edit_modulefield/2/',{'modulefield_name':'modulefield', 'modulefield_type':'modulefield', 'order':'5', 'org1.module_name':'模块5', 'org2.field_id':'1'})
        data = json.loads(authorityTableStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], u'编辑成功')
              
    def test_authority_selecteddelete_modulefield(self):
        for i in range(10): 
            self.client.post('/authority/add_modulefield/',{'modulefield_name':'modulefield_name'+ str(i), 'modulefield_type':'modulefield_type', 'order':'2', 'org1.module_name':'模块5', 'org2.field_id':'1'})
        authorityModulefieldStatus = self.client.post('/authority/selecteddelete_modulefield/',{'ids':'1,2,3,6'})
        data = json.loads(authorityModulefieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '选中项删除成功')



#按钮
class authorityButtonfieldTest(TestCase):    
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        password = make_password('admin', salt=None, hasher='default')
        user = User(username='admin', password=password, email='admin@admin.com')
        user.save();
        userprofile = UserProfile(user=user, department='admin', phone='admin')
        userprofile.save()
        #系统自带的login函数，不会触发自定义的login函数
#        self.client.login(username='admin', password='admin')
        self.client.post('/account/login/', {'username':'admin', 'password':'admin'})
        
        #添加模块
        for i in range(10): 
            self.client.post('/authority/add_module/',{'module_name':'模块' + str(i), 'module_type':'模块', 'order':'2', 'module_desc':'模块管理'})
    
    def test_authority_index_button(self):
        authorityButtonfieldStatus = self.client.post('/authority/index_button/')
        self.assertEqual(authorityButtonfieldStatus.status_code, 200)
    def test_authority_index_button5(self):
        authorityButtonfieldStatus = self.client.post('/authority/index_button/',{'q':'5'})
        self.assertEqual(authorityButtonfieldStatus.status_code, 200)
    
    def test_authority_add_button(self):
        authorityButtonfieldStatus = self.client.post('/authority/add_button/',{'org.module_name':'模块2', 'button_name':'按钮', 'button_type':'按钮2', 'order':'2'})
        data = json.loads(authorityButtonfieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '添加成功')
    
    def test_authority_add_button_error(self):
        authorityButtonfieldStatus = self.client.post('/authority/add_button/',{'org.module_name':'', 'button_name':'按钮', 'button_type':'按钮2', 'order':'2'})
        data = json.loads(authorityButtonfieldStatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '模块名为空不能添加')
    
    def test_authority_edit_button(self):
        for i in range(10): 
            self.client.post('/authority/add_button/',{'org.module_name':'模块1', 'button_name':'按钮' + str(i) , 'button_type':'按钮2', 'order':'2'})
        authorityButtonfieldStatus = self.client.post('/authority/edit_button/2/',{'org.module_name':'模块1', 'button_name':'按钮', 'button_type':'按钮2', 'order':'2'})
        data = json.loads(authorityButtonfieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], u'编辑成功')
    
    def test_authority_delete_button(self):
        for i in range(10):
            self.client.post('/authority/add_button/',{'org.module_name':'模块1', 'button_name':'按钮' + str(i) , 'button_type':'按钮2', 'order':'2'})
        authorityButtonfieldStatus=self.client.post('/authority/delete_button/2/')
        data = json.loads(authorityButtonfieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')

    def test_authority_selecteddelete_button(self):
        for i in range(10): 
            self.client.post('/authority/add_button/',{'org.module_name':'模块1', 'button_name':'按钮' + str(i) , 'button_type':'按钮2', 'order':'2'})
        authorityModuleStatus=self.client.post('/authority/selecteddelete_button/',{'ids':'1,2,3,5'})
        data = json.loads(authorityModuleStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '选中项删除成功')




#角色
class authorityRolefieldTest(TestCase):    
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        password = make_password('admin', salt=None, hasher='default')
        user = User(username='admin', password=password, email='admin@admin.com')
        user.save();
        userprofile = UserProfile(user=user, department='admin', phone='admin')
        userprofile.save()
        #系统自带的login函数，不会触发自定义的login函数
#        self.client.login(username='admin', password='admin')
        self.client.post('/account/login/', {'username':'admin', 'password':'admin'})
   
    def test_authority_index_role(self):
        authorityRolefieldStatus = self.client.post('/authority/index_role/')
        self.assertEqual(authorityRolefieldStatus.status_code, 200)
    def test_authority_index_role5(self):
        authorityRolefieldStatus = self.client.post('/authority/index_role/',{'q':'5'})
        self.assertEqual(authorityRolefieldStatus.status_code, 200)
    
    def test_authority_add_role(self):
        authorityRolefieldStatus = self.client.post('/authority/add_role/',{'role_name':'超人', 'role_desc':'我是超人', 'org.username':'', 'modulecheckbox':[], 'buttoncheckbox':[], 'modulefieldcheckbox':[]})
        data = json.loads(authorityRolefieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '添加成功')
    
    def test_authority_edit_role(self):
        for i in range(10): 
            self.client.post('/authority/add_role/',{'role_name':'超人' + str(i), 'role_desc':'我是超人', 'org.username':'', 'modulecheckbox':[], 'buttoncheckbox':[], 'modulefieldcheckbox':[]})
        authorityRolefieldStatus = self.client.post('/authority/edit_role/2/',{'role_name':'超人是我', 'role_desc':'我才是超人', 'org.username':'', 'modulecheckbox':[], 'buttoncheckbox':[], 'modulefieldcheckbox':[]})
        data = json.loads(authorityRolefieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], u'编辑成功')
    
    def test_authority_delete_role(self):
        for i in range(10):
            self.client.post('/authority/add_role/',{'role_name':'超人' + str(i), 'role_desc':'我是超人', 'org.username':'', 'modulecheckbox':[], 'buttoncheckbox':[], 'modulefieldcheckbox':[]})
        authorityRolefieldStatus = self.client.post('/authority/delete_role/2/')
        data = json.loads(authorityRolefieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')
    
    def test_authority_selecteddelete_role(self):
        for i in range(10): 
            self.client.post('/authority/add_role/',{'role_name':'超人' + str(i), 'role_desc':'我是超人', 'org.username':'', 'modulecheckbox':[], 'buttoncheckbox':[], 'modulefieldcheckbox':[]})
        authorityRolefieldStatus = self.client.post('/authority/selecteddelete_role/',{'ids':'1,2,3,6'})
        data = json.loads(authorityRolefieldStatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '选中项删除成功')
