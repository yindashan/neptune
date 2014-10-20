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
 
class LogTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        password = make_password('admin', salt=None, hasher='default')
        user = User(username='admin', password=password, email='admin@admin.com')
        user.save();
        userprofile = UserProfile(user=user, usertype='4', department='admin', phone='admin')
        userprofile.save()
        self.client.login(username='admin', password='admin')
        
    def test_log_add(self):
        logstatus = self.client.post('/log/add/', {'username':'aaaa', 'content':'aaaaaa', 'level':'1'})
        data = json.loads(logstatus.content)
        #if self.assertEqual(data['statusCode'], 200) == None:
        self.assertEqual(data['statusCode'], 200)
            #print data['message']
            #print "添加日志成功"

    def test_log_delete(self):
        for i in range(20):
           self.client.post('/log/add/',{'username':'aaaa'+str(i), 'content':'aaaaaa', 'level':'1'})
        logstatus = self.client.post('/log/delete/2/')
        data = json.loads(logstatus.content)
        #if self.assertEqual(data['statusCode'], 200)==None:
        self.assertEqual(data['statusCode'], 200)
            #print data['message']
            #print "删除日志成功"

    def test_log_selecteddelete(self):
        for i in range(20):
           self.client.post('/log/add/',{'username':'aaaa'+str(i), 'content':'aaaaaa', 'level':'1'})
        logstatus=self.client.post('/log/selecteddelete/',{'ids':'3,5,8,9'})
        data = json.loads(logstatus.content)
        #if self.assertEqual(data['statusCode'], 200)==None:
        self.assertEqual(data['statusCode'], 200)
            #print data['message']
            #print "选中日志删除成功"
    
    def test_log_edit(self):
        for i in range(20):
           self.client.post('/log/add/',{'username':'aaaa'+str(i), 'content':'aaaaaa', 'level':'1'})
        logstatus=self.client.post('/log/edit/1/',{'username':'aaaa', 'content':'aaaaaa', 'level':'1'})
        data = json.loads(logstatus.content)
        #if self.assertEqual(data['statusCode'], 200)==None:
        self.assertEqual(data['statusCode'], 200)
            #print data['message']
            #print "编辑日志成功"

    def test_log_search(self):
        for i in range(20):
           self.client.post('/log/add/',{'username':'aaaa'+str(i), 'content':'aaaaaa', 'level':'1'})       
        ispstatus=self.client.post('/log/search/',{'q':'aaa'})
#        selecteddelete
#        print self.client.get('/isp/').content
