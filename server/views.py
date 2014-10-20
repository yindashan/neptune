#!usr/bin/env python
#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import httplib
import urllib
import urllib2
import datetime

import os

from log.models import Log
from server.models import Server
from softform.models import SoftForm

from utils.constants import salt_status_dict



@login_required
def index(request):
    servers = Server.objects.order_by('-id')
    retdir = {}
    if 'nocid' in request.POST and request.POST['nocid']:
        nocid = request.POST['nocid']
        retdir['nocid'] = nocid
        servers = servers.filter(nocid__icontains = nocid)
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        servers = servers.filter(elementid__icontains = query)
    if 'saltid' in request.POST and request.POST['saltid']:
        saltid = request.POST['saltid']
        retdir['saltid'] = saltid
        servers = servers.filter(saltid__icontains = saltid)
    if 'in_ip' in request.POST and request.POST['in_ip']:
        in_ip = request.POST['in_ip']
        retdir['in_ip'] = in_ip
        servers = servers.filter(in_ip__icontains = in_ip)
    if 'service_name' in request.POST and request.POST['service_name']:
        service_name = request.POST['service_name']
        retdir['service_name'] = service_name
        servers = servers.filter(service_name__icontains = service_name)
    if 'salt_status' in request.POST and request.POST['salt_status']:
        salt_status = request.POST['salt_status']
        if salt_status == '0':
            retdir['salt_status'] = int(salt_status)
        else:
            retdir['salt_status'] = int(salt_status)
            servers = servers.filter(salt_status__iexact = int(salt_status))
#    if 'dateStart' in request.POST and request.POST['dateStart']:
#        dateStart = request.POST['dateStart']
#        retdir['dateStart'] = dateStart
#        dateStart = time.strptime(dateStart, "%Y-%m-%d")
#        dateStart = time.strftime("%Y-%m-%d %H:%M:%S", dateStart)
#        dateStart = utils.secs2datestr(utils.datestr2secs(dateStart))
#        equipments = equipments.filter(Q(buy_time__gte = dateStart) | Q(deadline__gte = dateStart))
#    if 'dateEnd' in request.POST and request.POST['dateEnd']:
#        dateEnd = request.POST['dateEnd']
#        retdir['dateEnd'] = dateEnd
#        dateEnd = time.strptime(dateEnd, "%Y-%m-%d")
#        dateEnd = time.strftime("%Y-%m-%d %H:%M:%S", dateEnd)
#        dateEnd = utils.secs2datestr(utils.datestr2secs(dateEnd) + 23*60*60 + 59*60 + 59)
#        equipments = equipments.filter(Q(buy_time__lte = dateEnd) | Q(deadline__lte = dateEnd))
    
    orderField = request.POST.get('orderField', None)
    orderDirection = request.POST.get('orderDirection', None)
    if orderField != None and orderField != '' and orderDirection != None and orderDirection != '':
        retdir['orderField'] = orderField
        retdir['orderDirection'] = orderDirection
        if orderDirection == 'asc':
            servers = servers.order_by(orderField)
        elif orderDirection == 'desc':
            servers = servers.order_by('-' + orderField)
    
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(servers, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        servers = paginator.page(page)
    except (EmptyPage, InvalidPage):
        servers = paginator.page(paginator.num_pages)
    tmpdir = {'servers':servers, 'currentPage':page, 'numPerPage':numPerPage, 'salt_status_dict':salt_status_dict}
    retdir.update(tmpdir)
    return render_to_response('server/basepage.html', retdir, context_instance=RequestContext(request))


@login_required
def add(request):
    if request.POST:
        nocid = request.POST.get('org.nocid', None)
        nocname = request.POST.get('org.nocname', None)
        elementid = request.POST.get('org.elementid', None)
        in_ip = request.POST.get('org.in_ip', None)
        out_ip = request.POST.get('org.out_ip', None)
        manage_account = request.POST.get('org.manage_account', None)
        manage_password = request.POST.get('org.manage_password', None)
        manage_port = request.POST.get('org.manage_port', None)
        virtual_flag = request.POST.get('org.virtual_flag', None)
        
        saltid = request.POST.get('saltid', None)
        service_name = request.POST.get('service_name', None)
        ids = request.POST.get('org.softid', None)
        
        agent_flag = request.POST.get('agent_flag', None)
        agent_saltid = request.POST.get('org.agent_saltid', None)
        
        
        '''验证机房编号,内网IP,saltid是否为空'''
        if not nocid or not in_ip or not saltid:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',None), "message":u'机房编号或内网IP为空不能添加'}), mimetype='application/json')
        
#        '''验证重复资产编号'''
#        servers = Server.objects.filter(elementid__iexact=elementid)
#        if servers:
#            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',None), "message":u'资产编号已经存在不能添加'}), mimetype='application/json')
        
        '''验证机房编号+内网IP是否唯一'''
        servers = Server.objects.filter(nocid__iexact=nocid, in_ip__iexact=in_ip)
        if servers:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',None), "message":u'当前服务器已经存在不能添加'}), mimetype='application/json')
        
        '''验证saltid是否唯一'''
        servers = Server.objects.filter(saltid__iexact=saltid)
        if servers:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',None), "message":u'saltid已经存在不能添加'}), mimetype='application/json')
        
        server = Server(nocid=nocid, 
                        nocname=nocname, 
                        elementid=elementid, 
                        in_ip=in_ip, 
                        out_ip=out_ip, 
                        manage_account=manage_account, 
                        manage_password=manage_password, 
                        saltid=saltid, 
                        service_name=service_name, 
                        salt_status=1)
        
        if agent_flag != None and agent_flag != '':
            server.agent_flag = agent_flag
            if agent_flag == '1':
                try:
                    agent_server = Server.objects.get(saltid=agent_saltid)
                    server.agent_server = agent_server
                    server.save()
                except:
                    return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',None), "message":u'代理服务器选择错误请重新选择'}), mimetype='application/json')
                
        server.save()
        if manage_port != None and manage_port != '':
            server.manage_port = manage_port
        else:
            server.manage_port = None
        if virtual_flag != None and virtual_flag != '':
            server.virtual_flag = virtual_flag
        else:
            server.virtual_flag = None
        server.save()
        
        # 添加基础应用
        if ids != None and ids != '':
            id_list = ids.split(',')
            for softid in id_list:
                softform = get_object_or_404(SoftForm, pk = int(softid))
                server.softforms.add(softform)
        server.save()
        
        
        Log(username=request.user.username, content=u"添加服务器:" + server.elementid + u" 成功!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
    else:
        return render_to_response('server/add.html')



@login_required
def edit(request, id):
    server = get_object_or_404(Server, pk=int(id))
    
    softid_list = []
    soft_name_list = []
    version_list = []
    softforms = server.softforms.all()
    for softform in softforms:
        softid_list.append(softform.id)
        soft_name_list.append(softform.soft_name)
        version_list.append(softform.version)
        
    if request.POST:
        server.out_ip = request.POST.get('org.out_ip', None)
        server.manage_account = request.POST.get('org.manage_account', None)
        server.manage_password = request.POST.get('org.manage_password', None)
        server.manage_port = request.POST.get('org.manage_port', None)
        server.saltid = request.POST.get('saltid', None)
        server.service_name = request.POST.get('service_name', None)
        
        # 添加是否需要代理以及代理设置
        agent_flag = request.POST.get('agent_flag', None)
        agent_saltid = request.POST.get('org.agent_saltid', None)
        if agent_flag != None and agent_flag != '':
            server.agent_flag = int(agent_flag)
            if agent_flag == '1':
                try:
                    agent_server = Server.objects.get(saltid=agent_saltid)
                    server.agent_server = agent_server
                    server.save()
                except:
                    return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',None), "message":u'代理服务器选择错误请重新选择'}), mimetype='application/json')
            else: # 不需要代理
                server.agent_server = None
                server.save()
            
        # 修改基础应用,先清空再添加
        server.softforms.clear()
        ids = request.POST.get('org.softid', None)
        if ids != None and ids != '':
            id_list = ids.split(',')
            for softid in id_list:
                softform = get_object_or_404(SoftForm, pk = int(softid))
                server.softforms.add(softform)
        server.save()
        
        Log(username=request.user.username, content=u"修改服务器:" + server.elementid + u" 成功!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    return render_to_response('server/edit.html', {'server': server, 'softid_list':softid_list, 'soft_name_list':soft_name_list, 'version_list':version_list})


@login_required
def delete(request,id):
    server = Server.objects.get(id=id)
    Log(username=request.user.username, content=u"删除服务器:" + server.elementid + u" 成功!", level=1).save()
    server.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'删除成功'}), mimetype='application/json')

@login_required
def selecteddelete(request):
    ids = request.POST.get('ids', None)
    if ids:
        servers = Server.objects.extra(where=['id IN ('+ ids +')'])
        for server in servers:
            Log(username=request.user.username, content=u"批量删除服务器:" + server.elementid + u" 成功!", level=1).save()
        servers.delete()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'选中项删除成功'}), mimetype='application/json')


'''
    通过API访问CMDB获取server信息
'''
@login_required
def searchback(request):
    retdir = {}
#    url = 'http://127.0.0.1:8080/equipment/equipment_list/'
#    url = 'http://10.2.134.3/equipment/equipment_list/'
    url = 'http://opcmdb.autonavi.com/equipment/equipment_list/'
    try:
        pageNum = None
        if request.POST:
            pageNum = request.POST.get('pageNum', None)
            nocid = request.POST.get('nocid', None)
            elementid = request.POST.get('elementid', None)
            in_ip = request.POST.get('in_ip', None)
            url = url + "?nocid=" + nocid.strip() + "&elementid=" + elementid.strip()  + "&in_ip=" + in_ip.strip()
            retdir['nocid'] = nocid
            retdir['elementid'] = elementid
            retdir['in_ip'] = in_ip
            
        numPerPage = 10
        # 从session中取出总条数
        if "totalcount" in request.session and request.session["totalcount"]:
            # 计算总页数
            if request.session["totalcount"]%numPerPage:
                totalpage = request.session["totalcount"]/numPerPage+1
            else:
                totalpage = request.session["totalcount"]/numPerPage
            retdir['totalpage'] = totalpage
        if pageNum == None or pageNum == '':
            pageNum = 1
        elif int(pageNum) > totalpage:
            pageNum = totalpage
        page = pageNum
        if '?' in url:
            url = url + "&page=" + unicode(page)
        else:
            url = url + "?page=" + unicode(page)
        retdir['currentPage'] = page
        retdir['numPerPage'] = numPerPage
        
        # 获得Token
        result_token = get_token(request)
        request_token = urllib2.Request(url)
        request_token.add_header("Authorization", "Token " + result_token['token'])
#        request.add_header("Authorization", "Token cc87b7a55a602572b3ea88965088178a0bf9b534")
        response_token = urllib2.urlopen(request_token)
        result_str = response_token.read()
        result_json = simplejson.loads(result_str)
        
        # 把总条数放到session里面
        if result_json['count'] != None and result_json['count'] != '':
            request.session["totalcount"] = result_json['count']
            if request.session["totalcount"]%numPerPage:
                totalpage = request.session["totalcount"]/numPerPage+1
            else:
                totalpage = request.session["totalcount"]/numPerPage
            retdir['totalpage'] = totalpage
        
        retdir['result_json'] = result_json
        # 用render_to_response会报错，不知 道为什么? 不能带context_instance=RequestContext(request)
        return render_to_response('server/searchback.html', retdir)
    except:
        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',None), "message":u'远程服务提供的API不能使用'}), mimetype='application/json')


'''
    验证API服务是否可用
'''
@login_required
def validate(request):
#    host = '127.0.0.1'
#    port = 8080
#    host = '10.2.134.3'
    host = 'opcmdb.autonavi.com'
    port = 80
    path = '/equipment/equipment_list/'
    try:
        # 获得Token
        result_token = get_token(request)
        
        conn = httplib.HTTPConnection(host, port)
        conn.request("HEAD", path, headers={"Authorization":"Token " + result_token['token']})
        response = conn.getresponse()
        status = response.status
        if status == 200:
            return HttpResponse('true')
        else:
            return HttpResponse('false')
    except:
        return HttpResponse('false')
    

'''
    获取Token
'''
@login_required
def get_token(request):
#    url = 'http://127.0.0.1:8080/api-token-auth/'
#    url = 'http://10.2.134.3/api-token-auth/'
    url = 'http://opcmdb.autonavi.com/api-token-auth/'
    data = {
            "username":"autonavi&token",
            "password":"autonavi&token"
    }
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    res = urllib2.urlopen(req)
    result_str = res.read()
    result_json = simplejson.loads(result_str)
    return result_json
    
    
    
@login_required
def searchback_softform(request):
    retdir = {}
    softforms = SoftForm.objects.order_by('-id')
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        softforms = softforms.filter(soft_name__icontains = query)
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
    paginator = Paginator(softforms, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        softforms = paginator.page(page)
    except (EmptyPage, InvalidPage):
        softforms = paginator.page(paginator.num_pages)
    tmpdir = {'softforms':softforms, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('server/searchback_softform.html', retdir, context_instance=RequestContext(request))



    
@login_required
def searchback_agent(request):
    retdir = {}
    servers = Server.objects.order_by('-id')
    if 'saltid' in request.POST and request.POST['saltid']:
        saltid = request.POST['saltid']
        retdir['saltid'] = saltid
        servers = servers.filter(saltid__icontains = saltid)
    if 'in_ip' in request.POST and request.POST['in_ip']:
        in_ip = request.POST['in_ip']
        retdir['in_ip'] = in_ip
        servers = servers.filter(in_ip__icontains = in_ip)
    orderField = request.POST.get('orderField', None)
    orderDirection = request.POST.get('orderDirection', None)
    if orderField != None and orderField != '' and orderDirection != None and orderDirection != '':
        retdir['orderField'] = orderField
        retdir['orderDirection'] = orderDirection
        if orderDirection == 'asc':
            servers = servers.order_by(orderField)
        elif orderDirection == 'desc':
            servers = servers.order_by('-' + orderField)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(servers, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        servers = paginator.page(page)
    except (EmptyPage, InvalidPage):
        servers = paginator.page(paginator.num_pages)
    tmpdir = {'servers':servers, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('server/searchback_agent.html', retdir, context_instance=RequestContext(request))



    

@login_required
def role(request):
    if request.POST:
        print "Hello"
        pass
    else:
        return render_to_response('server/role.html')


@login_required
def getsoftform(request):
    softforms = SoftForm.objects.all()
    soft_str = "soft_list"
    for softform in softforms:
        soft_str += "::" + unicode(softform.id) + "::" + softform.soft_type
    return HttpResponse(soft_str)




'''
    setup salt-minion
'''
@login_required
def setup(request, id):
    master = "10.2.161.15"
    server = Server.objects.get(id=id)
    in_ip = server.in_ip
    saltid = server.saltid
    cmdstr = 'cd /var/www/html/neptune/ && fab getos -H ' + in_ip + ' -u root'
    try:
        result_file = os.popen(cmdstr)
        result = result_file.readlines()
        print result
        result_file.close()
        result_str = ''.join(result)
        if 'out' not in result_str:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'连接超时，请确认是否通过SSH认证'}), mimetype='application/json')
        elif 'Ubuntu' in result_str:
            cmdstr_ubuntu = 'cd /var/www/html/neptune/ && fab setup_ubuntu:master=' + master + ',minionid=' + saltid + ' -H ' + in_ip + ' -u root'
            result_file_ubuntu = os.popen(cmdstr_ubuntu)
            result_ubuntu = result_file_ubuntu.readlines()
            print result_ubuntu
        elif 'CentOS' in result_str:
            cmdstr_centos = 'cd /var/www/html/neptune/ && fab setup_centos:master=' + master + ',minionid=' + saltid + ' -H ' + in_ip + ' -u root'
            result_file_centos = os.popen(cmdstr_centos)
            result_centos = result_file_centos.readlines()
            print result_centos
        else:
            cmdstr_centos = 'cd /var/www/html/neptune/ && fab setup_centos:master=' + master + ',minionid=' + saltid + ' -H ' + in_ip + ' -u root'
            result_file_centos = os.popen(cmdstr_centos)
            result_centos = result_file_centos.readlines()
            print result_centos
        server.salt_status = 2
        server.save()
    except:
        Log(username=request.user.username, content=u"安装:" + server.saltid + u" 失败!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'安装失败'}), mimetype='application/json')
    
    Log(username=request.user.username, content=u"安装:" + server.saltid + u" 成功!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'安装成功'}), mimetype='application/json')


'''
    start salt-minion
'''
@login_required
def start(request, id):
    server = Server.objects.get(id=id)
    in_ip = server.in_ip
    cmdstr = 'cd /var/www/html/neptune/ && fab getstatus -H ' + in_ip + ' -u root'
    try:
        result_file = os.popen(cmdstr)
        result = result_file.readlines()
        print result
        result_file.close()
        result_str = ''.join(result)
        
        if 'out' not in result_str:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'连接超时，请确认是否通过SSH认证'}), mimetype='application/json')
        elif 'start/running' in result_str:
            server.salt_status = 2
            server.save()
            return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'启动成功'}), mimetype='application/json')
        else:
            cmdstr_start = 'cd /var/www/html/neptune/ && fab start -H ' + in_ip + ' -u root'
            result_file_start = os.popen(cmdstr_start)
            result_start = result_file_start.readlines()
            print result_start
            result_file_start.close()
            server.salt_status = 2
            server.save()
    except:
        server.salt_status = 3
        server.save()
        Log(username=request.user.username, content=u"启动:" + server.saltid + u" 失败!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'启动失败'}), mimetype='application/json')

    Log(username=request.user.username, content=u"启动:" + server.saltid + u" 成功!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'启动成功'}), mimetype='application/json')


'''
    stop salt-minion
'''
@login_required
def stop(request, id):
    server = Server.objects.get(id=id)
    in_ip = server.in_ip
    cmdstr = 'cd /var/www/html/neptune/ && fab stop -H ' + in_ip + ' -u root'
    try:
        result_file = os.popen(cmdstr)
        result = result_file.readlines()
        print result
        result_file.close()
        result_str = ''.join(result)
        if 'out' not in result_str:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'连接超时，请确认是否通过SSH认证'}), mimetype='application/json')
        else:
            server.salt_status = 3
            server.save()
    except:
        server.salt_status = 2
        server.save()
        Log(username=request.user.username, content=u"关闭:" + server.saltid + u" 失败!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'关闭成功'}), mimetype='application/json')

    Log(username=request.user.username, content=u"关闭:" + server.saltid + u" 成功!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'关闭成功'}), mimetype='application/json')


'''
    restart salt-minion
'''
@login_required
def restart(request, id):
    server = Server.objects.get(id=id)
    in_ip = server.in_ip
    cmdstr = 'cd /var/www/html/neptune/ && fab restart -H ' + in_ip + ' -u root'
    try:
        result_file = os.popen(cmdstr)
        result = result_file.readlines()
        print result
        result_file.close()
        result_str = ''.join(result)
        if 'out' not in result_str:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'连接超时，请确认是否通过SSH认证'}), mimetype='application/json')
        else:
            server.salt_status = 2
            server.save()
    except:
        server.salt_status = 3
        server.save()
        Log(username=request.user.username, content=u"重新启动:" + server.saltid + u" 失败!", level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'重启失败'}), mimetype='application/json')

    Log(username=request.user.username, content=u"重新启动:" + server.saltid + u" 成功!", level=1).save()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','serverindex'), "callbackType":request.POST.get('callbackType',''), "message":u'重启成功'}), mimetype='application/json')





