#!usr/bin/env python
#coding: utf-8
'''
Created on 2013-3-27

@author: jingwen.wu

应用
'''
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import os
import stat

from log.models import Log
from apppackage.models import AppPackage
from utils.constants import down_type_dict


@login_required
def index(request):
    '''
    索引，查询应用，查询条件是报名处和软件包名称
    '''
    retdir = {}
    apppackages = AppPackage.objects.order_by('-id')
    if 'package_name' in request.POST and request.POST['package_name']:
        package_name = request.POST['package_name']
        retdir['package_name'] = package_name
        apppackages = apppackages.filter(package_name__icontains = package_name)
    orderField = request.POST.get('orderField', None)
    orderDirection = request.POST.get('orderDirection', None)
    if orderField != None and orderField != '' and orderDirection != None and orderDirection != '':
        retdir['orderField'] = orderField
        retdir['orderDirection'] = orderDirection
        if orderDirection == 'asc':
            apppackages = apppackages.order_by(orderField)
        elif orderDirection == 'desc':
            apppackages = apppackages.order_by('-' + orderField)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(apppackages, numPerPage)  # 每页显示数目
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        apppackages = paginator.page(page)
    except (EmptyPage, InvalidPage):
        apppackages = paginator.page(paginator.num_pages)
    tmpdir = {'apppackages': apppackages, 'currentPage':page, 'numPerPage':numPerPage, 'down_type_dict': down_type_dict}
    retdir.update(tmpdir)
    return render_to_response('apppackage/basepage.html', retdir, context_instance = RequestContext(request))


'''
    新增应用
'''
@login_required
def add_apppackage(request):
    if request.POST:
        down_type  = request.POST.get('down_type', None)  # 文件获取方式。0：“http”；1：“ftp”；2：“svn”；3:u“上传”
        down_path = request.POST.get('down_path', None)  # 文件获取链接
        username = request.POST.get('username', None)  # 用户名
        password = request.POST.get('password', None)  # 密码
        package_path = request.POST.get('package_path', None)  # 文件保存路径
        desc = request.POST.get('desc', None)  # 说明
        
        
        # 指定filedir路径，为了把生成的应用包传送到minion上面
        filedir = '/srv/salt/webserver/sites.d/'
        if(os.path.exists(filedir) == False):
            os.makedirs(filedir)
        # 修改权限777
        os.chmod(filedir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        
        # 根据不同的文件获取方式获取相应的文件
        if down_type == '0': # http
            url = down_path
            i = url.rfind('/')
            filename = url[i+1:]
            
            apppackage = AppPackage.objects.filter(package_name__iexact = filename)
            if apppackage:
                return render_to_response('apppackage/error_exist.html')
#                return HttpResponse(simplejson.dumps({"statusCode": 302, 
#                                                      "navTabId": request.POST.get('navTabId', 'apppackageindex'), 
#                                                      "callbackType": request.POST.get('callbackType', None), 
#                                                      "message": u'此应用包已经存在不能添加'}),
#                                    mimetype='application/json')
            
            try:
                # wget -O /home/dashan.yin/tomcat6.0.20-zhijian.tar.gz http://10.2.161.14/src/tomcat6.0.20-zhijian.tar.gz
                cmdstr = 'wget -O ' + filedir + filename + ' ' + url
                result_file = os.popen(cmdstr)
                result = result_file.readlines()
                result_file.close()
                print result
            except:
                return render_to_response('apppackage/error_file.html')
#                return HttpResponse(simplejson.dumps({"statusCode": 302, 
#                                                      "navTabId": request.POST.get('navTabId', 'apppackageindex'), 
#                                                      "callbackType": request.POST.get('callbackType', None), 
#                                                      "message": u'获取文件时发生错误，请检查后重新提交'}),
#                                    mimetype='application/json')
                
        elif down_type == '1': # ftp
            pass
        elif down_type == '2': # svn
            pass
        elif down_type == '3': # 上传
            if request.FILES:
                try:
                    f = request.FILES['file']
                    filename = f.name
                    
                    apppackage = AppPackage.objects.filter(package_name__iexact = filename)
                    if apppackage:
                        return render_to_response('apppackage/error_exist.html')
#                        return HttpResponse(simplejson.dumps({"statusCode": 302, 
#                                                              "navTabId": request.POST.get('navTabId', 'apppackageindex'), 
#                                                              "callbackType": request.POST.get('callbackType', None), 
#                                                              "message": u'此应用包已经存在不能添加'}),
#                                            mimetype='application/json')
                        
                    destination = open(filedir + filename, 'wb+')
                    for chunk in f.chunks():
                        destination.write(chunk)
                    destination.flush()
                    destination.close()
                except:
                    return render_to_response('apppackage/error_file.html')
#                    return HttpResponse(simplejson.dumps({"statusCode": 302, 
#                                                      "navTabId": request.POST.get('navTabId', 'apppackageindex'), 
#                                                      "callbackType": request.POST.get('callbackType', None), 
#                                                      "message": u'获取文件时发生错误，请检查后重新提交'}),
#                                    mimetype='application/json')
        
        
        
        
        apppackage = AppPackage(package_name = filename, 
                                down_type = down_type, 
                                down_path = down_path, 
                                username = username, 
                                password = password, 
                                package_path = package_path, 
                                status = 1, 
                                desc = desc)
        
        apppackage.save()
        Log(username = request.user.username, 
            content = u"应用包添加成功，名称是：" + filename).save()
        return render_to_response('apppackage/success.html')
#        return HttpResponse(simplejson.dumps({"statusCode": 200, 
#                                              "navTabId": request.POST.get('navTabId', 'apppackageindex'), 
#                                              "callbackType": request.POST.get('callbackType', 'closeCurrent'), 
#                                              "message": u'应用包' + apppackage.package_name + u'添加成功'}), 
#                            mimetype='application/json')
    return render_to_response('apppackage/add.html', {'down_type_dict': down_type_dict}, context_instance=RequestContext(request))
    
    
    
@login_required
def edit_apppackage(request, id):
    apppackage = get_object_or_404(AppPackage, pk = int(id))
    if request.POST:
        apppackage.down_type  = request.POST.get('down_type', None)  # 文件获取方式。0：“http”；1：“ftp”；2：“svn”；3:u“上传”
        apppackage.down_path = request.POST.get('down_path', None)  # 文件获取链接
        apppackage.username = request.POST.get('username', None)  # 用户名
        apppackage.password = request.POST.get('password', None)  # 密码
        apppackage.package_path = request.POST.get('package_path', None)  # 文件保存路径
        apppackage.desc = request.POST.get('desc', None)  # 说明
        
        apppackage.save()
        Log(username = request.user.username, 
            content = u"应用包修改成功，名称是：" + apppackage.package_name).save()
        return HttpResponse(simplejson.dumps({"statusCode": 200, 
                                              "navTabId": request.POST.get('navTabId', 'apppackageindex'), 
                                              "callbackType": request.POST.get('callbackType', 'closeCurrent'), 
                                              "message": u'应用包' + apppackage.package_name + u'修改成功'}), 
                            mimetype='application/json')
    return render_to_response('apppackage/edit.html', {'apppackage': apppackage, 'down_type_dict': down_type_dict}, context_instance=RequestContext(request))        


@login_required
def delete_apppackage(request,id):
    '''
    删除应用
    '''
    apppackage = AppPackage.objects.get(id = id)
    Log(username = request.user.username, 
        content = u"应用" + apppackage.package_name + u"删除成功").save()
    apppackage.delete()
    return HttpResponse(simplejson.dumps({"statusCode": 200, 
                                          "navTabId": request.POST.get('navTabId', 'apppackageindex'), 
                                          "callbackType": request.POST.get('callbackType', ''), 
                                          "message": u'删除成功'}), 
                        mimetype='application/json')

@login_required
def selecteddelete_apppackage(request):
    ids = request.POST.get('ids', None)
    if ids:
        apppackages = AppPackage.objects.extra(where = ['id IN (' + ids + ')'])
        for apppackage in apppackages:
            Log(username = request.user.username, 
                content = u"应用" + apppackage.name + u"删除成功").save()
        apppackages.delete()
    return HttpResponse(simplejson.dumps({"statusCode": 200, 
                                          "navTabId": request.POST.get('navTabId', 'apppackageindex'), 
                                          "callbackType": request.POST.get('callbackType', ''), 
                                          "message": u'选中应用删除成功'}), 
                        mimetype='application/json')