#!usr/bin/env python
#coding: utf-8
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from utils.constants import account_usertype_dict

from django.contrib.auth.models import User

def index(request):
    return render_to_response('account/login.html', {}, context_instance=RequestContext(request))
    #return render_to_response('common/index.html', {'account_usertype_dict':account_usertype_dict}, context_instance=RequestContext(request))

@login_required
def nav_index(request):
    if request.user.is_authenticated():
        # 从request中取值
        username = request.user.username
    return render_to_response('common/nav_index.html', {}, context_instance=RequestContext(request))

@login_required
def nav_resource(request):
    return render_to_response('common/nav_resource.html', {}, context_instance=RequestContext(request))

@login_required
def nav_log(request):
    return render_to_response('common/nav_log.html', {}, context_instance=RequestContext(request))

@login_required
def nav_ippool(request):
    return render_to_response('common/nav_ippool.html', {}, context_instance=RequestContext(request))

@login_required
def nav_user(request):
    return render_to_response('common/nav_user.html', {}, context_instance=RequestContext(request))

@login_required
def nav_authority(request):
    return render_to_response('common/nav_authority.html', {}, context_instance=RequestContext(request))

@login_required
def main(request):
    return render_to_response('common/main.html', {}, context_instance=RequestContext(request))

