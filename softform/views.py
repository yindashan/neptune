#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-3-27

@author: jingwen.wu

基础应用模板
'''
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from log.models import Log
from softform.models import SoftForm


@login_required
def index(request):
    '''
    索引，查询基础应用模板，查询条件是软件类型和软件包名称
    '''
    retdir = {}
    softforms = SoftForm.objects.order_by('soft_type')
    if 'soft_type' in request.POST and request.POST['soft_type']:
        soft_type = request.POST['soft_type']
        retdir['soft_type'] = soft_type
        softforms = softforms.filter(soft_type__icontains = soft_type)
    if 'soft_name' in request.POST and request.POST['soft_name']:
        soft_name = request.POST['soft_name']
        retdir['soft_name'] = soft_name
        softforms = softforms.filter(soft_name__icontains = soft_name)
    orderField = request.POST.get('orderField', None)
    orderDirection = request.POST.get('orderDirection', None)
    if orderField != None and orderField != '' and orderDirection != None and orderDirection != '':
        retdir['orderField'] = orderField
        retdir['orderDirection'] = orderDirection
        if orderDirection == 'asc':
            softforms = softforms.order_by(orderField)
        elif orderDirection == 'desc':
            softforms = softforms.order_by('-' + orderField)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(softforms, numPerPage)  # 每页显示数目
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        softforms = paginator.page(page)
    except (EmptyPage, InvalidPage):
        softforms = paginator.page(paginator.num_pages)
    tmpdir = {'softforms': softforms, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('softform/basepage.html', retdir, context_instance = RequestContext(request))
    
@login_required
def add_softform(request):
    '''
    新增基础应用模板
    '''    
    if request.POST:
        
        soft_type = request.POST.get('soft_type', None)  # 软件类型。如，apache
        soft_name = request.POST.get('soft_name', None)  # 软件包名称。如，httpd
        version  = request.POST.get('version', None)  # 版本
        os = request.POST.get('os', None)  # 运行所需操作系统
        os_byte = request.POST.get('os_byte', None)  # 操作系统位数
        os_version = request.POST.get('os_version', None)  # 操作系统版本
        
        softform = SoftForm.objects.filter(soft_name__iexact = soft_name, version__iexact = version)
        if softform:
            return HttpResponse(simplejson.dumps({"statusCode": 302, 
                                                  "navTabId": request.POST.get('navTabId', 'softformindex'), 
                                                  "callbackType": request.POST.get('callbackType', None), 
                                                  "message": u'此软件包名称已存在，不能添加',
                                                  "info": u'此软件包名称已存在，不能添加',
                                                  "result": u'此软件包名称已存在，不能添加'}),
                                mimetype='application/json')
        softform = SoftForm(soft_type = soft_type, soft_name = soft_name, 
                            version = version, os = os, os_byte = os_byte, 
                            os_version = os_version)
        softform.save()
        Log(username = request.user.username, 
            content = u"基础应用模板添加成功，软件包名称是：" + soft_name).save()
        return HttpResponse(simplejson.dumps({"statusCode": 200, 
                                              "navTabId": request.POST.get('navTabId', 'softformindex'), 
                                              "callbackType": request.POST.get('callbackType', 'closeCurrent'), 
                                              "message": u'基础应用模板' + softform.soft_name + u'添加成功'}), 
                            mimetype = 'application/json')
    return render_to_response('softform/add.html')
    
@login_required
def edit_softform(request, id):
    '''
    编辑基础应用模板
    '''
    softform = get_object_or_404(SoftForm, pk = int(id))
    if request.POST:
        version = request.POST.get('version', None)
        os = request.POST.get('os', None)
        os_byte = request.POST.get('os_byte', None)
        os_version = request.POST.get('os_version', None)
        
        if softform.version != version:
            Log(username = request.user.username, 
                content = u"基础应用模板" + softform.soft_name + \
                          u"，版本由" + str(softform.version) + u"改为" + str(version)).save()
            softform.version = version
        if softform.os != os:
            Log(username = request.user.username, 
                content = u"基础应用模板" + softform.soft_name + \
                          u"，操作系统由" + str(softform.os) + u"改为" + str(os)).save()
            softform.os = os
        if str(softform.os_byte) != str(os_byte):
            Log(username = request.user.username, 
                content = u"基础应用模板" + softform.soft_name + \
                          u"，操作系统位数由" + str(softform.os_byte) + u"改为" + str(os_byte)).save()
            softform.os_byte = os_byte
        if softform.os_version != os_version:
            Log(username = request.user.username, 
                content = u"基础应用模板" + softform.soft_name + \
                          u"，操作系统版本由" + str(softform.os_version) + u"改为" + str(os_version)).save()
            softform.os_version = os_version
        softform.save()

        return HttpResponse(simplejson.dumps({"statusCode": 200, 
                                              "navTabId": request.POST.get('navTabId', 'softformindex'), 
                                              "callbackType": request.POST.get('callbackType', 'closeCurrent'), 
                                              "message": u'基础应用模板' + softform.soft_name + u'编辑成功'}), 
                            mimetype = 'application/json')
    return render_to_response('softform/edit.html', {'softform': softform})        

@login_required
def delete_softform(request,id):
    '''
    删除基础应用模板
    '''
    softform = SoftForm.objects.get(id = id)
    softform.delete()
    Log(username = request.user.username, 
        content = u"基础应用模板" + softform.soft_name + u"删除成功").save()
    return HttpResponse(simplejson.dumps({"statusCode": 200, 
                                          "navTabId": request.POST.get('navTabId', 'softformindex'), 
                                          "callbackType": request.POST.get('callbackType', ''), 
                                          "message": u'基础应用模板' + softform.soft_name + u'删除成功'}), 
                        mimetype = 'application/json')

@login_required
def selecteddelete_softform(request):
    ids = request.POST.get('ids', None)
    if ids:
        softforms = SoftForm.objects.extra(where = ['id IN (' + ids + ')'])
        for softform in softforms:
            Log(username = request.user.username, 
                content = u"基础应用模板" + softform.soft_name + u"删除成功").save()
        softforms.delete()
    return HttpResponse(simplejson.dumps({"statusCode": 200, 
                                          "navTabId": request.POST.get('navTabId', 'softformindex'), 
                                          "callbackType": request.POST.get('callbackType', ''), 
                                          "message": u'选中基础应用模板删除成功'}), 
                        mimetype = 'application/json')
    
