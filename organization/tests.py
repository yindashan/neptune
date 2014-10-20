#coding: utf-8
#from django.db import models
import json
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from account.models import UserProfile
from django.contrib.auth.hashers import *
from account.views import login

import time



class organization_Test(TestCase):
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
 
    def test_organization_index(self):
        organizationstatus = self.client.post('/organization/index/')
        self.assertEqual(organizationstatus.status_code, 200)
    def test_organization_index5(self):
        organizationstatus = self.client.post('/organization/index/',{'numPerPage':'5', 'pageNum':'5'})
        self.assertEqual(organizationstatus.status_code, 200)
    def test_organization_index_query(self):
        for i in range(10): 
            self.client.post('/organization/add/', {'organization_name':'架构平台中心' + str(i), 'organization_desc':'架构平台中心', 'level':'3', 'org.parent_organization_name':''})
        organizationstatus = self.client.post('/organization/index/',{'query':'架构平台中心1'})
        self.assertEqual(organizationstatus.status_code, 200) 
    def test_organization_searchback_query(self):
        for i in range(10): 
            self.client.post('/organization/add/', {'organization_name':'架构平台中心' + str(i), 'organization_desc':'架构平台中心', 'level':'3', 'org.parent_organization_name':''})
        organizationstatus = self.client.post('/organization/searchback/',{'numPerPage':'5', 'pageNum':'5', 'query':'架构平台中心1'})
        self.assertEqual(organizationstatus.status_code, 200)
           
    def test_organization_add(self):
        self.client.post('/organization/add/', {'organization_name':'架构平台中心', 'organization_desc':'架构平台中心', 'level':'3', 'org.parent_organization_name':''})
        organizationstatus = self.client.post('/organization/add/', {'organization_name':'运维技术部', 'organization_desc':'运维技术部', 'level':'4', 'org.parent_organization_name':'架构平台中心'})
        data = json.loads(organizationstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '添加成功')

    def test_organization_repeatadd(self):
        self.client.post('/organization/add/', {'organization_name':'架构平台中心', 'organization_desc':'架构平台中心', 'level':'3', 'org.parent_organization_name':''})
        self.client.post('/organization/add/', {'organization_name':'运维技术部', 'organization_desc':'运维技术部', 'level':'4', 'org.parent_organization_name':'架构平台中心'})
        organizationstatus = self.client.post('/organization/add/', {'organization_name':'运维技术部', 'organization_desc':'运维技术部', 'level':'4', 'org.parent_organization_name':'架构平台中心'})
        data = json.loads(organizationstatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '组织机构名称已经存在不能添加')

    def test_organization_delete(self):
        for i in range(10): 
            self.client.post('/organization/add/',{'organization_name':'架构平台中心' + str(i), 'organization_desc':'架构平台中心', 'level':'3', 'org.parent_organization_name':''})
        organizationstatus=self.client.post('/organization/delete/2/')
        data = json.loads(organizationstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')

    def test_organization_delete_error(self):
        self.client.post('/organization/add/', {'organization_name':'架构平台中心', 'organization_desc':'架构平台中心', 'level':'3', 'org.parent_organization_name':''})
        for i in range(10): 
            self.client.post('/organization/add/',{'organization_name':'运维技术部' + str(i), 'organization_desc':'运维技术部', 'level':'4', 'org.parent_organization_name':'架构平台中心'})
        organizationstatus=self.client.post('/organization/delete/1/')
        data = json.loads(organizationstatus.content)
        self.assertEqual(data['statusCode'], 302)
        self.assertEqual(data['message'], '该组织机构有下属组织机构不能删除')

    def test_organization_selecteddelete(self):
        for i in range(10): 
            self.client.post('/organization/add/',{'organization_name':'架构平台中心' + str(i), 'organization_desc':'架构平台中心', 'level':'3', 'org.parent_organization_name':''})
        organizationstatus=self.client.post('/organization/selecteddelete/',{'ids':'1,2,3,5'})
        data = json.loads(organizationstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '删除成功')

    def test_organization_selecteddelete_error(self):
        self.client.post('/organization/add/', {'organization_name':'架构平台中心', 'organization_desc':'架构平台中心', 'level':'3', 'org.parent_organization_name':''})
        for i in range(10): 
            self.client.post('/organization/add/',{'organization_name':'运维技术部' + str(i), 'organization_desc':'运维技术部', 'level':'4', 'org.parent_organization_name':'架构平台中心'})
        organizationstatus=self.client.post('/organization/selecteddelete/',{'ids':'1,2,3,5'})
        data = json.loads(organizationstatus.content)
        self.assertEqual(data['statusCode'],302)
        self.assertEqual(data['message'], '该组织机构有下属组织机构不能删除')

    def test_organization_edit(self):
        for i in range(10): 
            self.client.post('/organization/add/', {'organization_name':'架构平台中心'+ str(i), 'organization_desc':'架构平台中心', 'level':'3', 'org.parent_organization_name':''})
            #虽然添加时org.parent_organization_name为空，但后台自动传给了它一个parent_organization_name值，在前台编辑的时候会自动渲染加上这个值，由于测试没有经过前台页面
            #所以无法渲染，要人为在org.parent_organization_name上加上edit编号对应的值       
        organizationstatus=self.client.post('/organization/edit/4/',{'organization_name':'1', 'organization_desc':'2', 'level':'4', 'org.parent_organization_name':'架构平台中心3'})
        data = json.loads(organizationstatus.content)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['message'], '编辑成功')
