#!usr/bin/env python
#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from utils.constants import log_level_dict


from log.models import Log

import time
from utils import utils

@login_required
def index(request):
    retdir = {}
    logs = Log.objects.order_by('-start_time')
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        logs = logs.filter(username__icontains = query)
    if 'dateStart' in request.POST and request.POST['dateStart']:
        dateStart = request.POST['dateStart']
        retdir['dateStart'] = dateStart
        dateStart = time.strptime(dateStart, "%Y-%m-%d")
        dateStart = time.strftime("%Y-%m-%d %H:%M:%S", dateStart)
        dateStart = utils.secs2datestr(utils.datestr2secs(dateStart))
        logs = logs.filter(start_time__gte = dateStart)
    if 'dateEnd' in request.POST and request.POST['dateEnd']:
        dateEnd = request.POST['dateEnd']
        retdir['dateEnd'] = dateEnd
        dateEnd = time.strptime(dateEnd, "%Y-%m-%d")
        dateEnd = time.strftime("%Y-%m-%d %H:%M:%S", dateEnd)
        dateEnd = utils.secs2datestr(utils.datestr2secs(dateEnd) + 23*60*60 + 59*60 + 59)
        logs = logs.filter(start_time__lte = dateEnd)
    
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(logs, numPerPage)
    page = request.POST.get('pageNum',1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        logs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        logs = paginator.page(paginator.num_pages)
    tmpdir = {'logs':logs, 'currentPage':page, 'numPerPage':numPerPage, 'log_level_dict':log_level_dict}
    retdir.update(tmpdir)
    return render_to_response('log/basepage.html', retdir, context_instance=RequestContext(request))


@login_required
def changerecord(request, log_type, relate_id):
    pass
#    # 计算sequence
#    sequence = None
#    if int(log_type) == 1: # 表示运营商日志
#        sequence = relate_id
#    elif int(log_type) == 2: # 表示机房日志
#        nocinfo = get_object_or_404(NOCInfo, pk=int(relate_id))
#        sequence = unicode(nocinfo.isp.id) + '.' + relate_id
#    elif int(log_type) == 3: # 表示机架日志
#        rack = get_object_or_404(Rack, pk=int(relate_id))
#        sequence = unicode(rack.nocinfo.isp.id) + '.' + unicode(rack.nocinfo.id) + '.' + relate_id
#    elif int(log_type) == 4: # 表示物理机日志
#        equipment = get_object_or_404(Equipment, pk=int(relate_id))
#        sequence = unicode(equipment.rack.nocinfo.isp.id) + '.' + unicode(equipment.rack.nocinfo.id) + '.' + unicode(equipment.rack.id) + '.' + relate_id
#    elif int(log_type) == 5: # 表示虚拟机日志
#        virtualmachine = get_object_or_404(VirtualMachine, pk=int(relate_id))
#        sequence = unicode(virtualmachine.equipment.rack.nocinfo.isp.id) + '.' + unicode(virtualmachine.equipment.rack.nocinfo.id) + '.' + unicode(virtualmachine.equipment.rack.id) + '.' + unicode(virtualmachine.equipment.id) + '.' + relate_id
#    
#    retdir = {}
#    '''单个查询'''
#    #logs = Log.objects.filter(Q(log_type__exact=log_type), Q(relate_id__exact=relate_id)|Q(sequence__startswith=sequence)).order_by('-start_time')
#    '''级联查询'''
#    logs = Log.objects.filter(Q(log_type__exact=log_type) & Q(relate_id__exact=relate_id) | Q(sequence__startswith=sequence)).order_by('-start_time')
#
#    if 'query' in request.POST and request.POST['query']:
#        query = request.POST['query']
#        retdir['query'] = query
#        logs = logs.filter(username__icontains = query)
#    if 'dateStart' in request.POST and request.POST['dateStart']:
#        dateStart = request.POST['dateStart']
#        retdir['dateStart'] = dateStart
#        dateStart = time.strptime(dateStart, "%Y-%m-%d")
#        dateStart = time.strftime("%Y-%m-%d %H:%M:%S", dateStart)
#        dateStart = utils.secs2datestr(utils.datestr2secs(dateStart))
#        logs = logs.filter(start_time__gte = dateStart)
#    if 'dateEnd' in request.POST and request.POST['dateEnd']:
#        dateEnd = request.POST['dateEnd']
#        retdir['dateEnd'] = dateEnd
#        dateEnd = time.strptime(dateEnd, "%Y-%m-%d")
#        dateEnd = time.strftime("%Y-%m-%d %H:%M:%S", dateEnd)
#        dateEnd = utils.secs2datestr(utils.datestr2secs(dateEnd) + 23*60*60 + 59*60 + 59)
#        logs = logs.filter(start_time__lte = dateEnd)
#    
#    if 'numPerPage' in request.POST and request.POST['numPerPage']:
#        numPerPage = request.POST['numPerPage']
#    else:
#        numPerPage = 10
#    paginator = Paginator(logs, numPerPage)
#    page = request.POST.get('pageNum',1)
#    try:
#        if int(page) > paginator.num_pages:
#            page = str(paginator.num_pages)
#        logs = paginator.page(page)
#    except (EmptyPage, InvalidPage):
#        logs = paginator.page(paginator.num_pages)
#    tmpdir = {'logs':logs, 'currentPage':page, 'numPerPage':numPerPage, 'log_level_dict':log_level_dict, 'log_type':log_type, 'relate_id':relate_id}
#    retdir.update(tmpdir)
#    return render_to_response('log/changerecord.html', retdir)


@login_required
def add(request):
    if request.POST:
        username = request.POST.get('username',None)
        content = request.POST.get('content',None)
        level = request.POST.get('level',None)
        log = Log(username=username, content=content, level=level)
        log.save()
        
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','logindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
    else:
        # 弹出新建窗口
        return render_to_response('log/add.html', {'log_level_dict':log_level_dict})


@login_required
def edit(request, id):
    log = get_object_or_404(Log, pk=int(id))
    if request.POST:
        log.username = request.POST.get('username',None)
        log.content = request.POST.get('content',None)
        log.level = request.POST.get('level',None)
        
        log.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','logindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    
    return render_to_response('log/edit.html', {'log': log, 'log_level_dict':log_level_dict})


@login_required
def detail(request, id):
    log = get_object_or_404(Log, pk=int(id))
#    if request.POST:
#        log.username = request.POST.get('username',None)
#        log.content = request.POST.get('content',None)
#        log.level = request.POST.get('level',None)
#        
#        log.save()
#        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','logindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    
    return render_to_response('log/detail.html', {'log': log, 'log_level_dict':log_level_dict})


@login_required
def delele(request,id):
    Log.objects.get(id=id).delete()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','logindex'), "callbackType":request.POST.get('callbackType',''), "message":u'删除成功'}), mimetype='application/json')

@login_required
def selecteddelete(request):
    ids = request.POST.get('ids', None)
    if ids:
        Log.objects.extra(where=['id IN ('+ ids +')']).delete() 
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','logindex'), "callbackType":request.POST.get('callbackType',''), "message":u'选中项删除成功'}), mimetype='application/json')

