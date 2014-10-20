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


import time


class dynamicconfTest(TestCase):
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
    
    #ldap
    def test_ldapconf_index(self):
        dynamicconfstatus = self.client.post('/dynamicconf/index_ldapconf/')
        self.assertEqual(dynamicconfstatus.status_code, 200)
    
    def test_ldapconf_add(self):
        dynamicconfstatus = self.client.post('/dynamicconf/add_ldapconf/', {'server':'fromunittest', 'base_dn':'Unittest', 'domainname':'111', 'loginname':'222', 'username':'222', 'password':'222'})
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '添加成功')
    
    def test_ldapconf_repeatedadd(self):
        self.client.post('/dynamicconf/add_ldapconf/', {'server':'fromunittest', 'base_dn':'Unittest', 'domainname':'111', 'loginname':'222', 'username':'222', 'password':'222'})
        dynamicconfstatus = self.client.post('/dynamicconf/add_ldapconf/', {'server':'fromunittest', 'base_dn':'Unittest', 'domainname':'111', 'loginname':'222', 'username':'222', 'password':'222'})
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '该LDAP的server已经存在不能添加')
    
    def test_ldapconf_delete(self):
        for i in range(10): 
            self.client.post('/dynamicconf/add_ldapconf/', {'server':'fromunittest'+ str(i), 'base_dn':'Unittest', 'domainname':'111', 'loginname':'222', 'username':'222', 'password':'222'})
        dynamicconfstatus=self.client.post('/dynamicconf/delete_ldapconf/2/')
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')
    
    def test_ldapconf_edit(self):
        for i in range(10): 
            self.client.post('/dynamicconf/add_ldapconf/', {'server':'fromunittest'+ str(i), 'base_dn':'Unittest', 'domainname':'111', 'loginname':'222', 'username':'222', 'password':'222'})
        dynamicconfstatus = self.client.post('/dynamicconf/edit_ldapconf/4/',{'server':'fromunittest'+ str(i), 'base_dn':'2', 'domainname':'ad', 'loginname':'2a', 'username':'222', 'password':'222'})
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '编辑成功')
        
    
    #openstack
    def test_openstackconf_index(self):
        dynamicconfstatus = self.client.post('/dynamicconf/index_openstackconf/')
        self.assertEqual(dynamicconfstatus.status_code, 200)
    
    def test_openstackconf_add(self):
        dynamicconfstatus = self.client.post('/dynamicconf/add_openstackconf/', {'username':'fromunittest', 'password':'Unittest', 'tenant_name':'111', 'auth_url':'222', 'computer_api_version':'222'})
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '添加成功')
    
    def test_openstackconf_delete(self):
        for i in range(10): 
            self.client.post('/dynamicconf/add_openstackconf/', {'username':'fromunittest'+str(i), 'password':'Unittest', 'tenant_name':'111', 'auth_url':'222', 'computer_api_version':'222'})
        dynamicconfstatus=self.client.post('/dynamicconf/delete_openstackconf/2/')
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')
    
    def test_openstackconf_edit(self):
        for i in range(10): 
            self.client.post('/dynamicconf/add_openstackconf/', {'username':'fromunittest'+str(i), 'password':'Unittest', 'tenant_name':'111', 'auth_url':'222', 'computer_api_version':'222'})
        dynamicconfstatus = self.client.post('/dynamicconf/edit_openstackconf/4/',{'username':'fromest', 'password':'Unitst', 'tenant_name':'111x', 'auth_url':'222xv', 'computer_api_version':'222'})
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '编辑成功')
    
    # A8
    def test_A8_index(self):
        dynamicconfstatus = self.client.post('/dynamicconf/index_a8conf/')
        self.assertEqual(dynamicconfstatus.status_code, 200)
    
    def test_A8_add(self):
        dynamicconfstatus = self.client.post('/dynamicconf/add_a8conf/', {'url':'fromunittest', 'username':'Unittest', 'password':'111'})
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '添加成功')
    def test_A8_repeatedadd(self):
        self.client.post('/dynamicconf/add_a8conf/', {'url':'fromunittest', 'username':'Unittest', 'password':'111'})       
        dynamicconfstatus = self.client.post('/dynamicconf/add_a8conf/', {'url':'fromunittest', 'username':'Unittest', 'password':'111'})
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], 'A8的url已经存在不能添加')
        
    def test_A8_delete(self):
        for i in range(10): 
            self.client.post('/dynamicconf/add_a8conf/', {'url':'fromunittest'+str(i), 'username':'Unittest', 'password':'111'})       
        dynamicconfstatus = self.client.post('/dynamicconf/delete_a8conf/2/')
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')
    
    def test_A8_edit(self):
        for i in range(10): 
            self.client.post('/dynamicconf/add_a8conf/', {'url':'fromunittest'+str(i), 'username':'Unittest', 'password':'111'})       
        dynamicconfstatus = self.client.post('/dynamicconf/edit_a8conf/2/', {'url':'fromunittestaaasd', 'username':'Unittest', 'password':'111'})    
        data = json.loads(dynamicconfstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '编辑成功')