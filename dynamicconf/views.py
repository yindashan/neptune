#!usr/bin/env python
#coding: utf-8

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from log.models import Log
from dynamicconf.models import LDAPConf
from dynamicconf.models import OpenStackConf
from dynamicconf.models import A8Conf

'''
    LDAP配置
'''
@login_required
def index_ldapconf(request):
    
    ldapconfs = LDAPConf.objects.all()
    if ldapconfs:
        ldapconf = ldapconfs[0]
        return render_to_response('dynamicconf/ldapconf/basepage.html', {'ldapconf':ldapconf}, context_instance=RequestContext(request))
    return render_to_response('dynamicconf/ldapconf/basepage.html', {'ldapconfs':ldapconfs}, context_instance=RequestContext(request))
    
@login_required
def add_ldapconf(request):
    if request.POST:
        server = request.POST.get('server', None)
        base_dn = request.POST.get('base_dn', None)
        domainname = request.POST.get('domainname', None)
        loginname = request.POST.get('loginname', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        #验证重复server名称
        servers = LDAPConf.objects.filter(server__iexact=server)
        if servers:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'ldapconfindex'), "callbackType":request.POST.get('callbackType',None), "message":u'该LDAP的server已经存在不能添加'}), mimetype='application/json')
        else:
            ldapconf = LDAPConf(server=server, base_dn=base_dn, domainname=domainname, loginname=loginname, username=username, password=password)
            ldapconf.save()
            
            Log(username=request.user.username, content=u"成功添加LDAP配置信息: " + ldapconf.server, level=1).save()
            return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'ldapconfindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
        
    return render_to_response('dynamicconf/ldapconf/add.html')

@login_required
def edit_ldapconf(request, id):
    
    ldapconf = get_object_or_404(LDAPConf, pk=int(id))
    if request.POST:
        ldapconf.server = request.POST.get('server', None)
        ldapconf.base_dn = request.POST.get('base_dn', None)
        ldapconf.domainname = request.POST.get('domainname', None)
        ldapconf.loginname = request.POST.get('loginname', None)
        ldapconf.username = request.POST.get('username', None)
        ldapconf.password = request.POST.get('password', None)
        
        ldapconf.save()
        
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'ldapconfindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    
    return render_to_response('dynamicconf/ldapconf/edit.html', {'ldapconf': ldapconf})


@login_required
def delete_ldapconf(request, id):
    ldapconf = LDAPConf.objects.get(id=id)
    Log(username=request.user.username, content=u"成功删除LDAP配置信息: " + ldapconf.server, level=1).save()
    ldapconf.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'ldapconfindex'), "callbackType":request.POST.get('callbackType', None), "message":u'删除成功'}), mimetype='application/json')


'''
    OpenStack配置
'''
@login_required
def index_openstackconf(request):
    
    openstackconfs = OpenStackConf.objects.all()
    if openstackconfs:
        openstackconf = openstackconfs[0]
        return render_to_response('dynamicconf/openstackconf/basepage.html', {'openstackconf':openstackconf}, context_instance=RequestContext(request))
    return render_to_response('dynamicconf/openstackconf/basepage.html', {'openstackconfs':openstackconfs}, context_instance=RequestContext(request))
    
@login_required
def add_openstackconf(request):
    if request.POST:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        tenant_name = request.POST.get('tenant_name', None)
        auth_url = request.POST.get('auth_url', None)
        computer_api_version = request.POST.get('computer_api_version', None)
        
        openstackconf = OpenStackConf(username=username, password=password, tenant_name=tenant_name, auth_url=auth_url, computer_api_version=computer_api_version)
        openstackconf.save()
        
        Log(username=request.user.username, content=u"成功添加OpenStack配置信息: " + openstackconf.auth_url, level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'openstackconfindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
        
    return render_to_response('dynamicconf/openstackconf/add.html')

@login_required
def edit_openstackconf(request, id):
    
    openstackconf = get_object_or_404(OpenStackConf, pk=int(id))
    if request.POST:
        openstackconf.username = request.POST.get('username', None)
        openstackconf.password = request.POST.get('password', None)
        openstackconf.tenant_name = request.POST.get('tenant_name', None)
        openstackconf.auth_url = request.POST.get('auth_url', None)
        openstackconf.computer_api_version = request.POST.get('computer_api_version', None)
        
        openstackconf.save()
        
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'openstackconfindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    
    return render_to_response('dynamicconf/openstackconf/edit.html', {'openstackconf': openstackconf})


@login_required
def delete_openstackconf(request, id):
    openstackconf = OpenStackConf.objects.get(id=id)
    Log(username=request.user.username, content=u"成功删除OpenStack配置信息: " + openstackconf.auth_url, level=1).save()
    openstackconf.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'openstackconfindex'), "callbackType":request.POST.get('callbackType', None), "message":u'删除成功'}), mimetype='application/json')


'''
    A8配置
'''
@login_required
def index_a8conf(request):
    
    a8confs = A8Conf.objects.all()
    if a8confs:
        a8conf = a8confs[0]
        return render_to_response('dynamicconf/a8conf/basepage.html', {'a8conf':a8conf}, context_instance=RequestContext(request))
    return render_to_response('dynamicconf/a8conf/basepage.html', {'a8confs':a8confs}, context_instance=RequestContext(request))
    
@login_required
def add_a8conf(request):
    if request.POST:
        url = request.POST.get('url', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        #验证重复url名称
        urls = A8Conf.objects.filter(url__iexact=url)
        if urls:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'a8confindex'), "callbackType":request.POST.get('callbackType',None), "message":u'A8的url已经存在不能添加'}), mimetype='application/json')
        else:
            a8conf = A8Conf(url=url, username=username, password=password)
            a8conf.save()
            
            Log(username=request.user.username, content=u"成功添加A8配置信息: " + a8conf.url, level=1).save()
            return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'a8confindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
        
    return render_to_response('dynamicconf/a8conf/add.html')

@login_required
def edit_a8conf(request, id):
    
    a8conf = get_object_or_404(A8Conf, pk=int(id))
    if request.POST:
        a8conf.url = request.POST.get('url', None)
        a8conf.username = request.POST.get('username', None)
        a8conf.password = request.POST.get('password', None)
        
        a8conf.save()
        
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'a8confindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    
    return render_to_response('dynamicconf/a8conf/edit.html', {'a8conf': a8conf})


@login_required
def delete_a8conf(request, id):
    a8conf = A8Conf.objects.get(id=id)
    Log(username=request.user.username, content=u"成功删除A8配置信息: " + a8conf.url, level=1).save()
    a8conf.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'a8confindex'), "callbackType":request.POST.get('callbackType', None), "message":u'删除成功'}), mimetype='application/json')



'''
    获取LDAP配置对象
'''
def get_ldapconf():
    ldapconfs = LDAPConf.objects.all()
    if ldapconfs:
        ldapconf = ldapconfs[0]
        return ldapconf
    else:
        return None

'''
    获取OpenStack配置对象
'''
def get_openstackconf():
    openstackconfs = OpenStackConf.objects.all()
    if openstackconfs:
        openstackconf = openstackconfs[0]
        return openstackconf
    else:
        return None

'''
    获取A8配置对象
'''
def get_a8conf():
    a8confs = A8Conf.objects.all()
    if a8confs:
        a8conf = a8confs[0]
        return a8conf
    else:
        return None










