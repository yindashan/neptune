#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-2-28

@author: jingwen.wu

操作管理
'''
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import csv

from log.models import Log
from action.models import Action, ActionGroup, ActionOrder


@login_required
def index_action(request):
    '''
    索引，查询操作模板，查询条件是操作模板类型和操作模板名称
    '''
    retdir = {}    
    actions = Action.objects.order_by('action_type')
    if 'action_type' in request.POST and request.POST['action_type']:
        action_type = request.POST['action_type']
        retdir['action_type'] = action_type
        actions = actions.filter(action_type__icontains=action_type)
    if 'name' in request.POST and request.POST['name']:
        name = request.POST['name']
        retdir['name'] = name
        actions = actions.filter(name__icontains=name)
    orderField = request.POST.get('orderField', None)
    orderDirection = request.POST.get('orderDirection', None)
    if orderField != None and orderField != '' and orderDirection != None and orderDirection != '':
        retdir['orderField'] = orderField
        retdir['orderDirection'] = orderDirection
        if orderDirection == 'asc':
            actions = actions.order_by(orderField)
        elif orderDirection == 'desc':
            actions = actions.order_by('-' + orderField)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(actions, numPerPage)  # 每页显示数目
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        actions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        actions = paginator.page(paginator.num_pages)
    tmpdir = {'actions': actions, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('action/basepage_action.html', retdir, context_instance=RequestContext(request))
    
@login_required
def add_action(request):
    '''
    新增操作模板
    '''    
    if request.POST:
        action_type = request.POST.get('action_type', None)  # 类型。如，apache,lse
        name = request.POST.get('name', None)  # 名称。如，LSE4部署。
        run_os = request.POST.get('run_os', None)  # 操作模板正常执行所需的操作系统
        action_cmd = request.POST.get('action_cmd', None)  # 操作
        if action_cmd == None or action_cmd == '':
            if request.FILES:
                f = request.FILES['file']           
                sh = f.read()       
                try:
                    action_cmd = sh.decode('utf-8-sig')
                except:           
                    action_cmd = sh.decode('gb2312')
                f.close()
        
        action = Action.objects.filter(action_type__iexact=action_type, name__iexact=name)
        if action:
            return HttpResponse(simplejson.dumps({"statusCode": 302,
                                                  "navTabId": request.POST.get('navTabId', 'actionindex'),
                                                  "callbackType": request.POST.get('callbackType', None),
                                                  "message": u'此操作模板已存在，不能添加',
                                                  "info": u'此操作模板已存在，不能添加',
                                                  "result": u'此操作模板已存在，不能添加'}),
                                mimetype='application/json')
        action = Action(action_type=action_type, name=name,
                        run_os=run_os, action_cmd=action_cmd)
        action.save()
        Log(username=request.user.username,
            content=u"操作模板添加成功，服务名称是：" + name).save()          
        return render_to_response('action/uploadsuccess.html', {'name': action.name})
    return render_to_response('action/add_action.html', context_instance=RequestContext(request))
    
@login_required
def edit_action(request, id):
    '''
    编辑操作模板
    '''
    action = get_object_or_404(Action, pk=int(id))
    if request.POST:
        run_os = request.POST.get('run_os', None)  # 操作模板正常执行所需的操作系统
        action_cmd = request.POST.get('action_cmd', None)  # 操作
        action.run_os = run_os
        action.action_cmd = action_cmd
        action.save()
        return HttpResponse(simplejson.dumps({"statusCode": 200,
                                              "navTabId": request.POST.get('navTabId', 'actionindex'),
                                              "callbackType": request.POST.get('callbackType', 'closeCurrent'),
                                              "message": u'操作模板“' + action.name + u'”编辑成功'}),
                            mimetype='application/json')
    return render_to_response('action/edit_action.html', {'action': action})        

@login_required
def delete_action(request, id):
    '''
    删除操作模板
    '''
    action = Action.objects.get(id=id)
    action.delete()
    Log(username = request.user.username,
        content = u"操作模板" + action.name + u"删除成功").save()
    return HttpResponse(simplejson.dumps({"statusCode": 200,
                                          "navTabId": request.POST.get('navTabId', 'actionindex'),
                                          "callbackType": request.POST.get('callbackType', ''),
                                          "message": u'操作模板“' + action.name + u'”删除成功'}),
                        mimetype='application/json')

@login_required
def selecteddelete_action(request):
    '''
    批量删除操作模板
    '''
    ids = request.POST.get('ids', None)
    if ids:
        actions = Action.objects.extra(where=['id IN (' + ids + ')'])
        for action in actions:
            Log(username=request.user.username,
                content=u"操作模板" + action.name + u"删除成功").save()
        actions.delete()
    return HttpResponse(simplejson.dumps({"statusCode": 200,
                                          "navTabId": request.POST.get('navTabId', 'actionindex'),
                                          "callbackType": request.POST.get('callbackType', ''),
                                          "message": u'选中操作模板删除成功'}),
                        mimetype='application/json')
    
@login_required
def detail_action(request, id):
    '''
    显示操作模板详情
    '''
    action = get_object_or_404(Action, pk=int(id))
    return render_to_response('action/detail_action.html', {'action': action})


@login_required
def index_actiongroup(request):
    '''
    索引，查询操作组，查询条件是操作组名称
    '''
    retdir = {}    
    actiongroups = ActionGroup.objects.order_by('name')
    if 'name' in request.POST and request.POST['name']:
        name = request.POST['name']
        retdir['name'] = name
        actiongroups = actiongroups.filter(name__icontains=name)
    orderField = request.POST.get('orderField', None)
    orderDirection = request.POST.get('orderDirection', None)
    if orderField != None and orderField != '' and orderDirection != None and orderDirection != '':
        retdir['orderField'] = orderField
        retdir['orderDirection'] = orderDirection
        if orderDirection == 'asc':
            actiongroups = actiongroups.order_by(orderField)
        elif orderDirection == 'desc':
            actiongroups = actiongroups.order_by('-' + orderField)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(actiongroups, numPerPage)  # 每页显示数目
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        actiongroups = paginator.page(page)
    except (EmptyPage, InvalidPage):
        actiongroups = paginator.page(paginator.num_pages)
    tmpdir = {'actiongroups': actiongroups, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('action/basepage_actiongroup.html', retdir, 
                              context_instance=RequestContext(request)) 


@login_required
def add_actiongroup(request):
    '''
    新增操作组
    '''    
    actions = Action.objects.order_by('action_type')
    if request.POST:
        name = request.POST.get('name', None)  # 名称。如，LSE4部署。
        desc = request.POST.get('desc', None)  # 说明。
        actionids = request.POST.getlist('actionids', None)  # 操作
        
        actiongroup = ActionGroup.objects.filter(name__iexact=name)
        if actiongroup:
            return HttpResponse(simplejson.dumps({"statusCode": 302,
                                                  "navTabId": request.POST.get('navTabId', 'actiongroupindex'),
                                                  "callbackType": request.POST.get('callbackType', None),
                                                  "message": u'此操作组已存在，不能添加',
                                                  "info": u'此操作组已存在，不能添加',
                                                  "result": u'此操作组已存在，不能添加'}),
                                mimetype='application/json')
        actiongroup = ActionGroup(name=name, desc=desc)
        actiongroup.save()
        action_group = ActionGroup.objects.get(name=name, desc=desc)
        
        if actionids != None and len(actionids) != 0:
            order = 0
            for actionid in actionids:
                action = Action.objects.get(id__exact = actionid)
                action_order = ActionOrder(action = action, group = action_group, order = order)
                action_order.save()
                order = order + 1
        
        Log(username = request.user.username,
            content = u"操作组添加成功，组名称是：" + name).save()
        return HttpResponse(simplejson.dumps({"statusCode": 200,
                                              "navTabId": request.POST.get('navTabId', 'actiongroupindex'),
                                              "callbackType": request.POST.get('callbackType', 'closeCurrent'),
                                              "message": u'操作组' + name + u'添加成功'}),
                            mimetype='application/json')
    return render_to_response('action/add_actiongroup.html', {'actions': actions})
    
@login_required
def edit_actiongroup(request, id):
    '''
    编辑操作组
    '''
    actiongroup = get_object_or_404(ActionGroup, pk = int(id))
    actionorders = ActionOrder.objects.filter(group__id__exact = id).order_by('order')
    sql = ''
    for actionorder in actionorders:
        sql += '~Q(id=' + str(actionorder.action.id) + ') & '
    if sql != '':
        sql = sql[0:-2]
        actions = Action.objects.filter(eval(sql)).order_by('action_type')
    else :
        actions = Action.objects.order_by('action_type')   
    if request.POST:
        desc = request.POST.get('desc', None)  # 说明。
        actionids = request.POST.getlist('actionids', None)  # 操作        
        
        actiongroup.desc = desc
        if actionids != None and len(actionids) != 0:
            actionorders.delete()  # 删除操作组中已有的操作序列
            order = 0
            for actionid in actionids:
                action = Action.objects.get(id__exact = actionid)
                action_order = ActionOrder(action = action, group = actiongroup, order = order)
                action_order.save()
                order = order + 1
        actiongroup.save()
        Log(username = request.user.username,
            content = u"操作组编辑成功，组名称是：" + actiongroup.name).save()
        return HttpResponse(simplejson.dumps({"statusCode": 200,
                                              "navTabId": request.POST.get('navTabId', 'actiongroupindex'),
                                              "callbackType": request.POST.get('callbackType', 'closeCurrent'),
                                              "message": u'操作组“' + actiongroup.name + u'”编辑成功'}),
                            mimetype='application/json')
    return render_to_response('action/edit_actiongroup.html', 
                              {'actions': actions, 'actiongroup':actiongroup, 
                               'actionorders': actionorders})        

@login_required
def delete_actiongroup(request, id):
    '''
    删除操作组
    '''
    actionorders = ActionOrder.objects.filter(group__id = id)
    actionorders.delete()
    actiongroup = ActionGroup.objects.get(id = id)
    actiongroup.delete()
    Log(username = request.user.username,
        content = u"操作组：" + actiongroup.name + u"删除成功").save()
    return HttpResponse(simplejson.dumps({"statusCode": 200,
                                          "navTabId": request.POST.get('navTabId', 'actiongroupindex'),
                                          "callbackType": request.POST.get('callbackType', ''),
                                          "message": u'操作组“' + actiongroup.name + u'”删除成功'}),
                        mimetype='application/json')

@login_required
def selecteddelete_actiongroup(request):
    '''
    批量删除操作组
    '''
    ids = request.POST.get('ids', None)
    if ids:
        actiongroups = ActionGroup.objects.extra(where = ['id IN (' + ids + ')'])
        actionorders = ActionOrder.objects.filter(group__in = actiongroups)
        for actiongroup in actiongroups:
            Log(username = request.user.username,
                content = u"操作组：" + actiongroup.name + u"删除成功").save()
        actionorders.delete()
        actiongroups.delete()
    return HttpResponse(simplejson.dumps({"statusCode": 200,
                                          "navTabId": request.POST.get('navTabId', 'actiongroupindex'),
                                          "callbackType": request.POST.get('callbackType', ''),
                                          "message": u'选中操作组删除成功'}),
                        mimetype='application/json')


@login_required
def detail_actiongroup(request, id):
    '''
    显示操作组详情
    '''
    actiongroup = get_object_or_404(ActionGroup, pk=int(id))
    actionorders = ActionOrder.objects.filter(group__id__exact = id).order_by('order')
    return render_to_response('action/detail_actiongroup.html', 
                              {'actiongroup': actiongroup, 'actionorders': actionorders})
