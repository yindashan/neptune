#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-2-28

@author: jingwen.wu

上线计划管理

'''

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from log.models import Log
from server.models import Server
from softform.models import SoftForm
from apppackage.models import AppPackage
from action.models import Action, ActionGroup, ActionOrder
from testcase.models import Testcase
from schedule.models import Schedule, ScheduleLog

from utils.constants import executive_state_dict, case_type_dict

# Import our libs
from djangosalt.control import (
    wildcardtarget,
    get_salt_client,
    get_api_client,
    )
from djangosalt.forms import LowdataForm

import threading
import yaml

from neptune.settings import SCHEDULE_LOG_DIR
import time
import os




@login_required
def index_schedule(request):
    '''
    索引，查询上线计划，查询条件是上线计划单号,服务名称和状态
    '''
    retdir = {}    
    schedules = Schedule.objects.order_by('-create_time')
    if 'schedule_id' in request.POST and request.POST['schedule_id']:
        schedule_id = request.POST['schedule_id']
        retdir['schedule_id'] = schedule_id
        schedules = schedules.filter(schedule_id__icontains = schedule_id)    
    if 'service_name' in request.POST and request.POST['service_name']:
        service_name = request.POST['service_name']
        retdir['service_name'] = service_name
        schedules = schedules.filter(service_name__icontains = service_name)
    if 'executive_state' in request.POST and request.POST['executive_state']:
        executive_state = request.POST['executive_state']
        if executive_state == '0':
            retdir['executive_state'] = int(executive_state)
        else:
            retdir['executive_state'] = int(executive_state)
            schedules = schedules.filter(executive_state__iexact = int(executive_state))
    orderField = request.POST.get('orderField', None)
    orderDirection = request.POST.get('orderDirection', None)
    if orderField != None and orderField != '' and orderDirection != None and orderDirection != '':
        retdir['orderField'] = orderField
        retdir['orderDirection'] = orderDirection
        if orderDirection == 'asc':
            schedules = schedules.order_by(orderField)
        elif orderDirection == 'desc':
            schedules = schedules.order_by('-' + orderField)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(schedules, numPerPage)  # 每页显示数目
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        schedules = paginator.page(page)
    except (EmptyPage, InvalidPage):
        schedules = paginator.page(paginator.num_pages)
    tmpdir = {'schedules': schedules, 'currentPage':page, 'numPerPage':numPerPage, 'executive_state_dict': executive_state_dict}
    retdir.update(tmpdir)
    return render_to_response('schedule/basepage.html', retdir, 
                              context_instance = RequestContext(request))
    
@login_required
def add_schedule(request):
    '''
    新增上线计划
    '''   
    servers = Server.objects.order_by('saltid')
    softforms = SoftForm.objects.order_by('soft_type')
    apppackages = AppPackage.objects.order_by('package_name')
    actiongroupss = ActionGroup.objects.order_by('name')
    testcases = Testcase.objects.order_by('name')
    if request.POST:
        schedule_id = request.POST.get('schedule_id', None)  # 上线计划单号。唯一标识
        service_name = request.POST.get('service_name', None)  # 服务名称。唯一标识
        department = request.POST.get('department', None)  # 上线部署部门
        department_dep = request.POST.get('department_dep', None)  # 研发部门
        contact = request.POST.get('contact', None)  # 联系人
        contact_info = request.POST.get('contact_info', None)  # 联系信息
        auto_rollback = request.POST.get('auto_rollback', None)  # 自动回滚标识。 0：自动回滚；1：不自动回滚；
        
        server_ids = request.POST.getlist('server_ids', None)  # 服务器组 
        softform_ids = request.POST.getlist('softform_ids', None)  # 基础应用模板组
        apppackage_ids = request.POST.getlist('apppackage_ids', None)  # 应用服务组
        actiongroup_ids = request.POST.getlist('actiongroup_ids', None)  # 操作流程
        testcase_ids = request.POST.getlist('testcase_ids', None)  # 测试用例组


        
        schedule = Schedule.objects.filter(schedule_id__exact = schedule_id)
        if schedule:
            return HttpResponse(simplejson.dumps({"statusCode": 302,
                                                  "navTabId": request.POST.get('navTabId', 'scheduleindex'),
                                                  "callbackType": request.POST.get('callbackType', None),
                                                  "message": u'此上线计划已存在，不能添加',
                                                  "info": u'此上线计划已存在，不能添加',
                                                  "result": u'此上线计划已存在，不能添加'}),
                                mimetype='application/json')


        schedule = Schedule(schedule_id = schedule_id, service_name=service_name,
                            user_name = request.user.username, 
                            department = department, department_dep = department_dep, 
                            contact = contact, contact_info = contact_info, 
                            auto_rollback = auto_rollback, executive_state = 1)
        schedule.save()        
        if server_ids != None and len(server_ids) != 0:
            for server_id in server_ids:
                server = Server.objects.get(id__exact = server_id)
                schedule.server_group.add(server)
        if softform_ids != None and len(softform_ids) != 0:
            for softform_id in softform_ids:
                softform = SoftForm.objects.get(id__exact = softform_id)
                schedule.softform_group.add(softform)
        if apppackage_ids != None and len(apppackage_ids) != 0:
            for apppackage_id in apppackage_ids:
                apppackage = AppPackage.objects.get(id__exact = apppackage_id)
                schedule.apppackage_group.add(apppackage)
        if actiongroup_ids != None and len(actiongroup_ids) != 0:
            for actiongroup_id in actiongroup_ids:
                actiongroup = ActionGroup.objects.get(id__exact = actiongroup_id)
                schedule.actiongroups.add(actiongroup)
        if testcase_ids != None and len(testcase_ids) != 0:
            for testcase_id in testcase_ids:
                testcase = Testcase.objects.get(id__exact = testcase_id)
                schedule.testcase_group.add(testcase)                            
        
        Log(username = request.user.username,
            content = u"上线计划" + schedule_id + u"添加成功").save()
        return HttpResponse(simplejson.dumps({"statusCode": 200,
                                              "navTabId": request.POST.get('navTabId', 'scheduleindex'),
                                              "callbackType": request.POST.get('callbackType', 'closeCurrent'),
                                              "message": u'上线计划' + schedule_id + u'添加成功'}),
                            mimetype='application/json')
    return render_to_response('schedule/add.html', {'servers': servers, 
                                                    'softforms': softforms, 
                                                    'apppackages': apppackages, 
                                                    'actiongroupss': actiongroupss, 
                                                    'testcases': testcases})
    
    
@login_required
def edit_schedule(request, id):
    '''
    编辑上线计划
    '''
    schedule = get_object_or_404(Schedule, pk=int(id))
    
    '''过滤已选server'''
    servergroup = schedule.server_group.all().order_by('saltid')
    if servergroup.count() > 0:
        sql = ''
        for server in servergroup:
            sql += '~Q(id=' + str(server.id )+ ') & '
        sql = sql[0:-2]
        servers = Server.objects.filter(eval(sql)).order_by('saltid')
    else :
        servers = Server.objects.order_by('saltid')
    
    '''过滤已选softform'''
    softformgroup = schedule.softform_group.all().order_by('soft_type')
    if softformgroup.count() > 0:
        sql = ''
        for softform in softformgroup:
            sql += '~Q(id=' + str(softform.id) + ') &'
        sql = sql[0:-2]
        softforms = SoftForm.objects.filter(eval(sql)).order_by('soft_type')  
    else :
        softforms = SoftForm.objects.order_by('soft_type')      
    
    '''过滤已选apppackage'''
    apppackagegroup = schedule.apppackage_group.all().order_by('package_name')
    if apppackagegroup.count() > 0:
        sql = ''
        for apppackage in apppackagegroup:
            sql += '~Q(id=' + str(apppackage.id) + ') & '
        sql = sql[0:-2]
        apppackages = AppPackage.objects.filter(eval(sql)).order_by('package_name')
    else :
        apppackages = AppPackage.objects.order_by('package_name')
    
    '''过滤已选actiongroup'''
    actiongroup_s = schedule.actiongroups.all().order_by('name')
    if actiongroup_s.count() > 0:
        sql = ''
        for actiongroup in actiongroup_s:
            sql += '~Q(id=' + str(actiongroup.id) + ') & '
        sql = sql[0:-2]
        actiongroupss = ActionGroup.objects.filter(eval(sql)).order_by('name')
    else :
        actiongroupss = ActionGroup.objects.order_by('name')
    
    '''过滤已选testcase'''
    testcasegroup = schedule.testcase_group.all().order_by('name')
    if testcasegroup.count() > 0:
        sql = ''
        for testcase in testcasegroup:
            sql += '~Q(id=' + str(testcase.id) + ') &'
        sql = sql[0:-2]
        testcases = Testcase.objects.filter(eval(sql)).order_by('name')
    else :
        testcases = Testcase.objects.order_by('name')
    
    
    if request.POST:
        department_dep = request.POST.get('department_dep', None)  # 研发部门
        contact = request.POST.get('contact', None)  # 联系人
        contact_info = request.POST.get('contact_info', None)  # 联系信息
        auto_rollback = request.POST.get('auto_rollback', None)  # 自动回滚标识    
        
        server_ids = request.POST.getlist('server_ids', None)  # 服务器组 
        softform_ids = request.POST.getlist('softform_ids', None)  # 基础应用模板组
        apppackage_ids = request.POST.getlist('apppackage_ids', None)  # 应用服务组
        actiongroup_ids = request.POST.getlist('actiongroup_ids', None)  # 操作流程
        testcase_ids = request.POST.getlist('testcase_ids', None)  # 测试用例组 
        
        schedule.department_dep = department_dep
        schedule.contact = contact
        schedule.contact_info = contact_info
        schedule.auto_rollback = auto_rollback
        schedule.user_name = request.user.username  # 操作用户。执行自动上线部署的操作人员。
        schedule.save()
        
        schedule.server_group.clear()
        schedule.softform_group.clear()
        schedule.apppackage_group.clear()
        schedule.actiongroups.clear()
        schedule.testcase_group.clear()
        if server_ids != None and len(server_ids) != 0:
            for server_id in server_ids:
                server = Server.objects.get(id__exact = server_id)
                schedule.server_group.add(server)
        if softform_ids != None and len(softform_ids) != 0:
            for softform_id in softform_ids:
                softform = SoftForm.objects.get(id__exact = softform_id)
                schedule.softform_group.add(softform)
        if apppackage_ids != None and len(apppackage_ids) != 0:
            for apppackage_id in apppackage_ids:
                apppackage = AppPackage.objects.get(id__exact = apppackage_id)
                schedule.apppackage_group.add(apppackage)
        if actiongroup_ids != None and len(actiongroup_ids) != 0:
            for actiongroup_id in actiongroup_ids:
                actiongroup = ActionGroup.objects.get(id__exact = actiongroup_id)
                schedule.actiongroups.add(actiongroup)
        if testcase_ids != None and len(testcase_ids) != 0:
            for testcase_id in testcase_ids:
                testcase = Testcase.objects.get(id__exact = testcase_id)
                schedule.testcase_group.add(testcase)        
        
        Log(username = request.user.username,
            content = u"上线计划" + schedule.schedule_id + u"编辑成功").save()
        return HttpResponse(simplejson.dumps({"statusCode": 200,
                                              "navTabId": request.POST.get('navTabId', 'scheduleindex'),
                                              "callbackType": request.POST.get('callbackType', 'closeCurrent'),
                                              "message": u'上线计划' + schedule.schedule_id + u'编辑成功'}),
                            mimetype='application/json')
    return render_to_response('schedule/edit.html', 
                              {'schedule': schedule, 
                               'servers': servers, 'servergroup': servergroup, 
                               'softforms': softforms, 'softformgroup': softformgroup, 
                               'apppackages': apppackages, 'apppackagegroup': apppackagegroup, 
                               'actiongroupss': actiongroupss, 'actiongroup_s': actiongroup_s, 
                               'testcases': testcases, 'testcasegroup': testcasegroup})            


@login_required
def delete_schedule(request, id):
    '''
    删除上线计划
    '''
    schedule = Schedule.objects.get(id = id)
    ScheduleLog.objects.filter(schedule_id__exact = schedule.schedule_id).update(state = 1)
    schedule.delete()
    Log(username = request.user.username,
        content = u"上线计划" + schedule.schedule_id + u"删除成功").save()
    return HttpResponse(simplejson.dumps({"statusCode": 200,
                                          "navTabId": request.POST.get('navTabId', 'scheduleindex'),
                                          "callbackType": request.POST.get('callbackType', ''),
                                          "message": u'上线计划' + schedule.schedule_id + u'删除成功'}),
                        mimetype='application/json')

@login_required
def selecteddelete_schedule(request):
    '''
    批量删除上线计划
    '''
    ids = request.POST.get('ids', None)
    if ids:
        schedules = Schedule.objects.extra(where = ['id IN (' + ids + ')'])
        for schedule in schedules:
            ScheduleLog.objects.filter(schedule_id__exact = schedule.schedule_id).update(state = 1)
            Log(username = request.user.username,
                content = u"上线计划" + schedule.schedule_id + u"删除成功").save()
        schedules.delete()
    return HttpResponse(simplejson.dumps({"statusCode": 200,
                                          "navTabId": request.POST.get('navTabId', 'scheduleindex'),
                                          "callbackType": request.POST.get('callbackType', ''),
                                          "message": u'选中上线计划删除成功'}),
                        mimetype='application/json')
    
@login_required
def detail_schedule(request, id):
    '''
    显示上线计划详情
    '''
    schedule = get_object_or_404(Schedule, pk=int(id))
    servers = schedule.server_group.all().order_by('saltid')
    softforms = schedule.softform_group.all().order_by('soft_type')
    apppackages = schedule.apppackage_group.all().order_by('package_name')
    actiongroupss = schedule.actiongroups.all().order_by('name')
    testcases = schedule.testcase_group.all().order_by('name')    
    return render_to_response('schedule/detail.html', {'schedule': schedule, 
                                                       'servers': servers, 
                                                       'softforms': softforms, 
                                                       'apppackages': apppackages, 
                                                       'actiongroupss': actiongroupss, 
                                                       'testcases': testcases, 
                                                       'case_type_dict': case_type_dict 
                                                       })





def __pkg_install(target, argument):
    '''
    安装第三方软件
    '''
    shell_result = {}
    client = get_salt_client()
    target = 'L@' + ','.join(target)
    func = 'state.high'
    arg = [argument]
    
    shell_result = client.cmd(target, func, arg, expr_form = 'compound', ret = 'json')    
    yaml_str = yaml.dump(shell_result, default_flow_style=False)
    return yaml_str


def __file_transfer(target, apppackage):
    '''
        文件传输
    '''
    shell_result = {}
    client = get_salt_client()
    minion_list = target
    
    # 把文件传送到所有的跳板机上
    minion_list_syndic = []
    try:
        for saltid in minion_list:
            server = Server.objects.get(saltid=saltid)
            if server.agent_flag == 1:
                if server.agent_server.saltid not in minion_list_syndic:
                        minion_list_syndic.append(server.agent_server.saltid)
    except Exception, e:
        print e
    
    if minion_list_syndic:
        target_syndic = 'L@' + ','.join(minion_list_syndic)
        func = 'cp.get_file'
        arg = ['salt://webserver/sites.d/' + apppackage.package_name, '/srv/salt/webserver/sites.d/' + apppackage.package_name]
        shell_ret = client.cmd(target_syndic, func, arg, expr_form = 'compound', ret = 'json')
        shell_result.update(shell_ret)
        
    
    # 把文件传送到所有的minion上面(包括跳板机下面的minion)
    target = 'L@' + ','.join(target)
    func = 'cp.get_file'
    arg = ['salt://webserver/sites.d/' + apppackage.package_name, apppackage.package_path + apppackage.package_name]
    shell_ret = client.cmd(target, func, arg, expr_form = 'compound', ret = 'json')
    shell_result.update(shell_ret)
    yaml_str = yaml.dump(shell_result, default_flow_style=False)
    return yaml_str


def __actiongroup_execute(target, shell_str):
    '''
        操作组执行
    '''
    shell_result = {}
    client = get_salt_client()
    target = 'L@' + ','.join(target)
    func = 'cmd.run'
    arg = [shell_str]
    shell_result = client.cmd(target, func, arg, expr_form = 'compound', ret = 'json')    
    yaml_str = yaml.dump(shell_result, default_flow_style=False)
    return yaml_str

    
def __schedule_log(schedule_id, content):
    '''
    记录执行结果
    '''
    if os.path.isdir(SCHEDULE_LOG_DIR): 
        pass 
    else: 
        os.makedirs(SCHEDULE_LOG_DIR)
    time_temp = time.strftime("%Y%m%d", time.localtime())
    filename = SCHEDULE_LOG_DIR + schedule_id + '_' + str(time_temp) + '.log'
    file = open(filename, 'a')
    file.write('\n')
    file.write(content)
    file.write('\n')
    file.close()
    
    # 在数据库中记录日志名称
    schedule_log = ScheduleLog.objects.filter(log_name__exact = filename, state = 0)
    if schedule_log:
        pass
    else:
        pre_log = ScheduleLog.objects.filter(schedule_id__exact = schedule_id, next_id = 0, state = 0)
        if pre_log:
            pre_log = ScheduleLog.objects.get(schedule_id__exact = schedule_id, next_id = 0, state = 0)
            schedule_log = ScheduleLog(log_name = filename, schedule_id = schedule_id, pre_id = pre_log.id)
            schedule_log.save()
            pre_log.next_id = schedule_log.id
            pre_log.save()
        else:
            schedule_log = ScheduleLog(log_name = filename, schedule_id = schedule_id)
            schedule_log.save()
    

@login_required
@wildcardtarget
def go_schedule(request, id):
    '''
   执行上线计划
    '''
    client = get_salt_client()
    schedule = get_object_or_404(Schedule, pk=int(id))
    
    '''过滤已选server'''
    servergroup = schedule.server_group.all().order_by('saltid')
    if servergroup.count() > 0:
        sql = ''
        for server in servergroup:
            sql += '~Q(id=' + str(server.id )+ ') & '
        sql = sql[0:-2]
        servers = Server.objects.filter(eval(sql)).order_by('saltid')
    else :
        servers = Server.objects.order_by('saltid')
    
    '''过滤已选softform'''
    softformgroup = schedule.softform_group.all().order_by('soft_type')
    if softformgroup.count() > 0:
        sql = ''
        for softform in softformgroup:
            sql += '~Q(id=' + str(softform.id) + ') &'
        sql = sql[0:-2]
        softforms = SoftForm.objects.filter(eval(sql)).order_by('soft_type')  
    else :
        softforms = SoftForm.objects.order_by('soft_type')      
    
    '''过滤已选apppackage'''
    apppackagegroup = schedule.apppackage_group.all().order_by('package_name')
    if apppackagegroup.count() > 0:
        sql = ''
        for apppackage in apppackagegroup:
            sql += '~Q(id=' + str(apppackage.id) + ') & '
        sql = sql[0:-2]
        apppackages = AppPackage.objects.filter(eval(sql)).order_by('package_name')
    else :
        apppackages = AppPackage.objects.order_by('package_name')
    
    '''过滤已选actiongroup'''
    actiongroup_s = schedule.actiongroups.all().order_by('name')
    if actiongroup_s.count() > 0:
        sql = ''
        for actiongroup in actiongroup_s:
            sql += '~Q(id=' + str(actiongroup.id) + ') & '
        sql = sql[0:-2]
        actiongroupss = ActionGroup.objects.filter(eval(sql)).order_by('name')
    else :
        actiongroupss = ActionGroup.objects.order_by('name')
    
    '''过滤已选testcase'''
    testcasegroup = schedule.testcase_group.all().order_by('name')
    if testcasegroup.count() > 0:
        sql = ''
        for testcase in testcasegroup:
            sql += '~Q(id=' + str(testcase.id) + ') &'
        sql = sql[0:-2]
        testcases = Testcase.objects.filter(eval(sql)).order_by('name')
    else :
        testcases = Testcase.objects.order_by('name')
    
    
    if request.POST:
        department_dep = request.POST.get('department_dep', None)  # 研发部门
        contact = request.POST.get('contact', None)  # 联系人
        contact_info = request.POST.get('contact_info', None)  # 联系信息
        auto_rollback = request.POST.get('auto_rollback', None)  # 自动回滚标识    
        
        server_ids = request.POST.getlist('server_ids', None)  # 服务器组 
        softform_ids = request.POST.getlist('softform_ids', None)  # 基础应用模板组
        apppackage_ids = request.POST.getlist('apppackage_ids', None)  # 应用服务组
        actiongroup_ids = request.POST.getlist('actiongroup_ids', None)  # 操作流程
        testcase_ids = request.POST.getlist('testcase_ids', None)  # 测试用例组 
        
        schedule.department_dep = department_dep
        schedule.contact = contact
        schedule.contact_info = contact_info
        schedule.auto_rollback = auto_rollback
        schedule.user_name = request.user.username  # 操作用户。执行自动上线部署的操作人员。
        schedule.executive_state = 3  # 全上执行中
        schedule.save()
        
        schedule.server_group.clear()
        schedule.softform_group.clear()
        schedule.apppackage_group.clear()
        schedule.actiongroups.clear()
        schedule.testcase_group.clear()
        target = []
        if server_ids != None and len(server_ids) != 0:
            for server_id in server_ids:
                server = Server.objects.get(id__exact = server_id)
                schedule.server_group.add(server)
                target.append(server.saltid)
        else:
            return HttpResponse(simplejson.dumps({"statusCode": 302,
                                                  "navTabId": request.POST.get('navTabId', 'scheduleindex'),
                                                  "callbackType": request.POST.get('callbackType', None),
                                                  "message": u'服务器列表不能为空',
                                                  "info": u'服务器列表不能为空',
                                                  "result": u'服务器列表不能为空'}),
                                mimetype='application/json')            
        argument = '{'    
        if softform_ids != None and len(softform_ids) != 0:
            for softform_id in softform_ids:
                softform = SoftForm.objects.get(id__exact = softform_id)
                schedule.softform_group.add(softform)
                # 基础应用模板版本为空时，默认在线安装
                if softform.version == '' or softform.version == None:
                    argument += '\"' + softform.soft_name + '\": {\"pkg\": [\"installed\"]}, '
                    
        apppackage_list = []
        if apppackage_ids != None and len(apppackage_ids) != 0:
            for apppackage_id in apppackage_ids:
                apppackage = AppPackage.objects.get(id__exact = apppackage_id)
                schedule.apppackage_group.add(apppackage)
                apppackage_list.append(apppackage)
                
        actiongroup_list = []
        if actiongroup_ids != None and len(actiongroup_ids) != 0:
            for actiongroup_id in actiongroup_ids:
                actiongroup = ActionGroup.objects.get(id__exact = actiongroup_id)
                schedule.actiongroups.add(actiongroup)
                actiongroup_list.append(actiongroup)
                
        if testcase_ids != None and len(testcase_ids) != 0:
            for testcase_id in testcase_ids:
                testcase = Testcase.objects.get(id__exact = testcase_id)
                schedule.testcase_group.add(testcase)        
        
        '''
            在线安装软件包
        '''
        if target and len(argument) > 1:
            argument = argument[0:-2] + '}'
            ret_pkg_install = __pkg_install(target, argument)
            __schedule_log(schedule.schedule_id, ret_pkg_install)
            
        
        '''
            文件传输
        '''
        for apppackage in apppackage_list:
            ret_file_transfer = __file_transfer(target, apppackage)
            __schedule_log(schedule.schedule_id, ret_file_transfer)
        
        
        '''
            操作组执行
        '''
        shell_str = ''
        for actiongroup in actiongroup_list:
            actionorders = actiongroup.actionorder_set.all()
            count = actionorders.count()
            for i in range(count):
                actionorder = ActionOrder.objects.get(group_id=actiongroup.id, order=i)
                action = actionorder.action
                action_cmd = action.action_cmd
                action_cmd_list = action_cmd.split('\r\n')
                action_cmd_str = ' && '.join([line for line in action_cmd_list if not line.startswith('#') and line != ''])
                shell_str = shell_str + action_cmd_str + ' && '
        if shell_str != '' or shell_str != None:
            shell_str = shell_str[0:-4]
            ret_actiongroup_execute = __actiongroup_execute(target, shell_str)
            __schedule_log(schedule.schedule_id, ret_actiongroup_execute)
        
            
        schedule.executive_state = 5  # 全上完成
        schedule.save()
        Log(username = request.user.username,
            content = u"上线计划" + schedule.schedule_id + u"执行成功").save()
        return HttpResponse(simplejson.dumps({"statusCode": 200,
                                              "navTabId": request.POST.get('navTabId', 'scheduleindex'),
                                              "callbackType": request.POST.get('callbackType', 'closeCurrent'),
                                              "message": u'上线计划' + schedule.schedule_id + u'执行成功'}),
                            mimetype='application/json')
    return render_to_response('schedule/go.html', 
                              {'schedule': schedule, 
                               'servers': servers, 'servergroup': servergroup, 
                               'softforms': softforms, 'softformgroup': softformgroup, 
                               'apppackages': apppackages, 'apppackagegroup': apppackagegroup, 
                               'actiongroupss': actiongroupss, 'actiongroup_s': actiongroup_s, 
                               'testcases': testcases, 'testcasegroup': testcasegroup})            


@login_required
def show_log(request, id):
    '''
    显示上线计划执行日志
    '''
    schedule = get_object_or_404(Schedule, pk = int(id))
    schedule_log = ScheduleLog.objects.filter(schedule_id__exact = schedule.schedule_id, state = 0)
    log = ''
    if schedule_log:
        schedule_log = ScheduleLog.objects.get(schedule_id__exact = schedule.schedule_id, next_id = 0, state = 0)
        log_name = schedule_log.log_name
        name = os.path.basename(log_name)
        file = open(log_name, 'r')
        log = file.read()
        file.close()
        return render_to_response('schedule/schedule_log.html', 
                                  {'schedule': schedule, 
                                   'schedule_log': schedule_log, 
                                   'name': name, 'log': log})
    else:
        return render_to_response('schedule/schedule_log_null.html', 
                                  {'schedule':schedule})

@login_required
def show_pre_next_log(request, id):
    '''
    显示上线计划的前一次或后一次执行日志
    '''
    log = ''
    schedule_log = ScheduleLog()
    schedule = Schedule()
    if int(id) > 0:
        schedule_log = get_object_or_404(ScheduleLog, pk = int(id))
        log_name = schedule_log.log_name
        name = os.path.basename(log_name)
        file = open(log_name, 'r')
        log = file.read()
        file.close()
        schedule = Schedule.objects.get(schedule_id__exact = schedule_log.schedule_id)
    return render_to_response('schedule/schedule_pre_next_log.html', 
                              {'schedule': schedule, 
                               'schedule_log': schedule_log, 
                               'name': name, 'log': log})



