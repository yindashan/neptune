#!usr/bin/env python
#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    department = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=15, blank=True)


'''
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
import datetime

class ProfileBase(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field):
                    fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)
        
class Profile(object):
    __metaclass__ = ProfileBase

class MyProfile(Profile):
    nickname = models.CharField(max_length = 255)
    birthday = models.DateTimeField(null = True, blank = True)
    city = models.CharField(max_length = 30, blank = True)
    university = models.CharField(max_length = 255, blank = True)
    
    def is_today_birthday(self):
        return self.birthday.date() == datetime.date.today()

'''    


    