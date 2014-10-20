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

from organization.models import Organization

from neptune.settings import DEFAULT_FROM_EMAIL
from_email = DEFAULT_FROM_EMAIL
from django.template import loader
from utils.utils import send_mail

from utils.constants import applyonline_status_dict
from utils import utils

import time
import datetime

from log.models import Log
from applyonline.models import ApplyOnline

from utils.utils import isEquipmentStatus, isDate, isInt

@login_required
def index(request):
    '''判断是否具备管理功能,如果具备则可以查看所有的申请单，如果不具备只能查看当前用户自己提交的申请单'''
    buttonlist = request.session["authority_list_button"]
    if 'applyonlinemanage' in buttonlist:
        applyonlines = ApplyOnline.objects.filter(flag=1).order_by('-id')
    else:
        applyonlines = ApplyOnline.objects.filter(flag=1, apply_user__iexact=request.user.username).order_by('-id')
        
    retdir = {}
    if 'applyid' in request.POST and request.POST['applyid']:
        applyid = request.POST['applyid']
        retdir['applyid'] = applyid
        applyonlines = applyonlines.filter(applyid__icontains = applyid)
    if 'status' in request.POST and request.POST['status']:
        status = request.POST['status']
        if status == 'all':
            retdir['status'] = status
        else:
            retdir['status'] = int(status)
            applyonlines = applyonlines.filter(status__iexact = int(status))
    if 'dateStart' in request.POST and request.POST['dateStart']:
        dateStart = request.POST['dateStart']
        retdir['dateStart'] = dateStart
        dateStart = time.strptime(dateStart, "%Y-%m-%d")
        dateStart = time.strftime("%Y-%m-%d %H:%M:%S", dateStart)
        dateStart = utils.secs2datestr(utils.datestr2secs(dateStart))
        applyonlines = applyonlines.filter(Q(apply_time__gte = dateStart))
    if 'dateEnd' in request.POST and request.POST['dateEnd']:
        dateEnd = request.POST['dateEnd']
        retdir['dateEnd'] = dateEnd
        dateEnd = time.strptime(dateEnd, "%Y-%m-%d")
        dateEnd = time.strftime("%Y-%m-%d %H:%M:%S", dateEnd)
        dateEnd = utils.secs2datestr(utils.datestr2secs(dateEnd) + 23*60*60 + 59*60 + 59)
        applyonlines = applyonlines.filter(Q(apply_time__lte = dateEnd))
    
    orderField = request.POST.get('orderField', None)
    orderDirection = request.POST.get('orderDirection', None)
    if orderField != None and orderField != '' and orderDirection != None and orderDirection != '':
        retdir['orderField'] = orderField
        retdir['orderDirection'] = orderDirection
        if orderDirection == 'asc':
            applyonlines = applyonlines.order_by(orderField)
        elif orderDirection == 'desc':
            applyonlines = applyonlines.order_by('-' + orderField)
    
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(applyonlines, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        applyonlines = paginator.page(page)
    except (EmptyPage, InvalidPage):
        applyonlines = paginator.page(paginator.num_pages)
    tmpdir = {'applyonlines':applyonlines, 'currentPage':page, 'numPerPage':numPerPage, 'applyonline_status_dict':applyonline_status_dict}
    retdir.update(tmpdir)
    return render_to_response('applyonline/basepage.html', retdir, context_instance=RequestContext(request))
        


@login_required
def detail(request, id):
    # 显示申请单的详情
    applyonline = ApplyOnline.objects.get(id = id)
    return render_to_response('applyonline/detail.html', {'applyonline':applyonline, 'applyonline_status_dict':applyonline_status_dict}, context_instance=RequestContext(request))   


@login_required
def add(request):
    if request.POST:
#        applyid = request.POST.get('applyid', None)

        service_name = request.POST.get('service_name', None)
        service_domainname = request.POST.get('service_domainname', None)
        version = request.POST.get('version', None)
#        apply_user = request.POST.get('apply_user', None)
        apply_user = request.user.username
        apply_time = request.POST.get('apply_time', None)
        priority = request.POST.get('priority', None)
        file_name = request.POST.get('file_name', None)
        file_url = request.POST.get('file_url', None)
        online_time = request.POST.get('online_time', None)
        develop_user = request.POST.get('develop_user', None)
        test_user = request.POST.get('test_user', None)
        operate_user = request.POST.get('operate_user', None)
        
        is_system_test = request.POST.get('is_system_test', None)
        is_function_test = request.POST.get('is_function_test', None)
        is_capability_test = request.POST.get('is_capability_test', None)
        is_pressure_test = request.POST.get('is_pressure_test', None)
        is_ui_test = request.POST.get('is_ui_test', None)
        is_special_test = request.POST.get('is_special_test', None)
        is_uat_test = request.POST.get('is_uat_test', None)
        is_stability_test = request.POST.get('is_stability_test', None)
        is_version_control = request.POST.get('is_version_control', None)
        is_train_complete = request.POST.get('is_train_complete', None)
        is_datatransfer_complete = request.POST.get('is_datatransfer_complete', None)
        is_document_complete = request.POST.get('is_document_complete', None)
        is_environment_complete = request.POST.get('is_environment_complete', None)
        is_backup_plan = request.POST.get('is_backup_plan', None)
        is_paramconf_complete = request.POST.get('is_paramconf_complete', None)
        is_can_online = request.POST.get('is_can_online', None)
        is_check_url = request.POST.get('is_check_url', None)
        
        check_url = request.POST.get('check_url', None)
        
        deploy_step = request.POST.get('deploy_step', None)
        backup_method = request.POST.get('backup_method', None)
        update_check = request.POST.get('update_check', None)
        
        
        '''自动生成申请单号'''
        prefix = 'OP-SR-'
        time_list = apply_time.split('-')
        timestr = ''.join(time_list)
        applyonline_count = ApplyOnline.objects.filter(apply_time=datetime.date(int(time_list[0]), int(time_list[1]), int(time_list[2]))).count()
        applyid = prefix + timestr + '-' + str(applyonline_count+1)
        
        '''验证重复申请单号'''
        applyids = ApplyOnline.objects.filter(applyid__iexact=applyid)
        if applyids:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'applyonlineindex'), "callbackType":request.POST.get('callbackType',None), "message":u'申请单号已经存在不能添加'}), mimetype='application/json')
        applyonline = ApplyOnline(applyid=applyid, service_name=service_name, service_domainname=service_domainname, 
                                  version=version, apply_user=apply_user, apply_time=apply_time, file_name=file_name, 
                                  file_url=file_url, online_time=online_time, develop_user=develop_user, test_user=test_user,
                                  operate_user=operate_user, check_url=check_url, deploy_step=deploy_step, backup_method=backup_method, 
                                  update_check=update_check, status=0, flag=1)
        
        applyonline.save()
        
        applyonline.priority = int(priority)
        applyonline.is_system_test = int(is_system_test)
        applyonline.is_function_test = int(is_function_test)
        applyonline.is_capability_test = int(is_capability_test)
        applyonline.is_pressure_test = int(is_pressure_test)
        applyonline.is_ui_test = int(is_ui_test)
        applyonline.is_special_test = int(is_special_test)
        applyonline.is_uat_test = int(is_uat_test)
        applyonline.is_stability_test = int(is_stability_test)
        applyonline.is_version_control = int(is_version_control)
        applyonline.is_train_complete = int(is_train_complete)
        applyonline.is_datatransfer_complete = int(is_datatransfer_complete)
        applyonline.is_document_complete = int(is_document_complete)
        applyonline.is_environment_complete = int(is_environment_complete)
        applyonline.is_backup_plan = int(is_backup_plan)
        applyonline.is_paramconf_complete = int(is_paramconf_complete)
        applyonline.is_can_online = int(is_can_online)
        applyonline.is_check_url = int(is_check_url)
        
        applyonline.save()
        
        
        '''申请人添加完申请单后向运维相关人员发送邮件提示'''
        subject = u'服务上线申请'
        to_mail_list = []
        if operate_user != None and operate_user != '':
            usernamelist = operate_user.split(',')
            for username in usernamelist:
                username += '@autonavi.com'
                to_mail_list.append(username)
        # 定义邮件内容
        email = u"您好，现在已向您发送了服务器上线申请,以下是基本信息,详细信息请登录CMDB系统查询："
        body = loader.render_to_string('applyonline/mail_operate.html', {'email':email, 'applyonline':applyonline})
        send_mail(subject, body, from_email, to_mail_list, html="text/html")
        
        
        Log(username=request.user.username, content="execute add applyonline:" + applyonline.applyid + " success!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'equipmentindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
    else:
        # 弹出新建窗口
        return render_to_response('applyonline/add.html', {'applyonline_status_dict':applyonline_status_dict})

@login_required
def edit(request, id):
    applyonline = get_object_or_404(ApplyOnline, pk=int(id))
    if request.POST:
        applyonline_desc = request.POST.get('applyonline_desc', None)
        applyonline.applyonline_desc = applyonline_desc
        applyonline.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','applyonlineindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    return render_to_response('applyonline/edit.html', {'applyonline':applyonline, 'applyonline_status_dict':applyonline_status_dict})        

@login_required
def deploy_success(request, id):
    applyonline = get_object_or_404(ApplyOnline, pk=int(id))
    if request.POST:
        applyonline_desc = request.POST.get('applyonline_desc', None)
        if applyonline.applyonline_desc != None:
            applyonline.applyonline_desc += '\n' + applyonline_desc
        else:
            applyonline.applyonline_desc = applyonline_desc
        applyonline.status = 1
        applyonline.save()
        
        
        '''运维人员部署成功后向相关人员发送邮件提示，提醒相关人员进行验证'''
        subject = u'服务上线验证'
        to_mail_list = []
        if applyonline.apply_user != None and applyonline.apply_user != '':
            usernamelist = applyonline.apply_user.split(',')
            for username in usernamelist:
                username += '@autonavi.com'
                to_mail_list.append(username)
        # 定义邮件内容
        email = u"您好，服务部署成功，请进行相应的验证："
        body = loader.render_to_string('applyonline/mail_deploy_success.html', {'email':email, 'applyonline':applyonline})
        send_mail(subject, body, from_email, to_mail_list, html="text/html")
        
        
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','applyonlineindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'操作成功'}), mimetype='application/json')
    return render_to_response('applyonline/deploy_success.html', {'applyonline':applyonline, 'applyonline_status_dict':applyonline_status_dict})        

@login_required
def deploy_failure(request, id):
    applyonline = get_object_or_404(ApplyOnline, pk=int(id))
    if request.POST:
        applyonline_desc = request.POST.get('applyonline_desc', None)
        if applyonline.applyonline_desc != None:
            applyonline.applyonline_desc += '\n' + applyonline_desc
        else:
            applyonline.applyonline_desc = applyonline_desc
        applyonline.status = 3
        applyonline.save()
        
        '''运维人员部署失败后向申请人发送邮件提示'''
        subject = u'服务上线失败'
        to_mail_list = []
        if applyonline.apply_user != None and applyonline.apply_user != '':
            usernamelist = applyonline.apply_user.split(',')
            for username in usernamelist:
                username += '@autonavi.com'
                to_mail_list.append(username)
        # 定义邮件内容
        email = u"您好，服务器上线失败，请检查申请单并重新填写一份申请单："
        body = loader.render_to_string('applyonline/mail_deploy_failure.html', {'email':email, 'applyonline':applyonline})
        send_mail(subject, body, from_email, to_mail_list, html="text/html")
        
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','applyonlineindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'操作成功'}), mimetype='application/json')
    return render_to_response('applyonline/deploy_failure.html', {'applyonline':applyonline, 'applyonline_status_dict':applyonline_status_dict})        

@login_required
def validate_success(request, id):
    applyonline = get_object_or_404(ApplyOnline, pk=int(id))
    if request.POST:
        applyonline_desc = request.POST.get('applyonline_desc', None)
        if applyonline.applyonline_desc != None:
            applyonline.applyonline_desc += '\n' + applyonline_desc
        else:
            applyonline.applyonline_desc = applyonline_desc
        applyonline.status = 2
        applyonline.save()
        
        
        '''申请人验证成功后向运维人员发送邮件提示'''
        subject = u'服务验证成功'
        to_mail_list = []
        if applyonline.apply_user != None and applyonline.apply_user != '':
            usernamelist = applyonline.apply_user.split(',')
            for username in usernamelist:
                username += '@autonavi.com'
                to_mail_list.append(username)
        # 定义邮件内容
        email = u"您好，服务验证成功，谢谢您的大力支持！"
        body = loader.render_to_string('applyonline/mail_validate_success.html', {'email':email, 'applyonline':applyonline})
        send_mail(subject, body, from_email, to_mail_list, html="text/html")
        
        
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','applyonlineindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'操作成功'}), mimetype='application/json')
    return render_to_response('applyonline/validate_success.html', {'applyonline':applyonline, 'applyonline_status_dict':applyonline_status_dict})        

@login_required
def validate_failure(request, id):
    applyonline = get_object_or_404(ApplyOnline, pk=int(id))
    if request.POST:
        applyonline_desc = request.POST.get('applyonline_desc', None)
        if applyonline.applyonline_desc != None:
            applyonline.applyonline_desc += '\n' + applyonline_desc
        else:
            applyonline.applyonline_desc = applyonline_desc
        applyonline.status = 3
        applyonline.save()
        
        '''申请人验证失败后向运维人员发送邮件提示'''
        subject = u'服务验证失败'
        to_mail_list = []
        if applyonline.apply_user != None and applyonline.apply_user != '':
            usernamelist = applyonline.apply_user.split(',')
            for username in usernamelist:
                username += '@autonavi.com'
                to_mail_list.append(username)
        # 定义邮件内容
        email = u"您好，服务验证失败，我会重新发一份申请单，请您重新部署："
        body = loader.render_to_string('applyonline/mail_validate_failure.html', {'email':email, 'applyonline':applyonline})
        send_mail(subject, body, from_email, to_mail_list, html="text/html")
        
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','applyonlineindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'操作成功'}), mimetype='application/json')
    return render_to_response('applyonline/validate_failure.html', {'applyonline':applyonline, 'applyonline_status_dict':applyonline_status_dict})        

@login_required
def delete(request,id):
    applyonline = ApplyOnline.objects.get(id=id)
    Log(username=request.user.username, content="execute delete applyonline:" + applyonline.applyid + " success!", level=1).save()
    applyonline.flag = 0
    applyonline.save()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','applyonlineindex'), "callbackType":request.POST.get('callbackType',''), "message":u'删除成功'}), mimetype='application/json')

@login_required
def selecteddelete(request):
    ids = request.POST.get('ids', None)
    if ids:
        applyonlines = ApplyOnline.objects.extra(where=['id IN ('+ ids +')'])
        applyonlines.update(flag=0)
        for applyonline in applyonlines:
            Log(username=request.user.username, content="execute selecteddelete applyonline:" + applyonline.applyid + " success!", level=1).save()
            applyonline.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','applyonlineindex'), "callbackType":request.POST.get('callbackType',''), "message":u'选中项删除成功'}), mimetype='application/json')






