#!usr/bin/env python
#coding: utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

import ldap
import json
from neptune.settings import DEFAULT_FROM_EMAIL
from_email = DEFAULT_FROM_EMAIL
#from django.conf import settings
#from_email = settings.DEFADEFAULT_FROM_EMAIL
from django.template import loader

from utils.utils import send_mail

from log.models import Log
from authority.models import Role
from organization.models import Organization

from dynamicconf.views import get_ldapconf

from utils.constants import account_usertype_dict

# 导入在forms.py 中定义的所有表单类。
from forms import *
from account.models import UserProfile

@login_required
def index(request):
    retdir = {}
    users = User.objects.order_by('-id')
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        users = users.filter(username__icontains = query)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(users, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)
    tmpdir = {'users':users,'currentPage':page, 'numPerPage':numPerPage, 'account_usertype_dict':account_usertype_dict}
    retdir.update(tmpdir)
    return render_to_response('account/welcome.html', retdir, context_instance=RequestContext(request))
    

@login_required
def info(request, id):
    user=get_object_or_404(User,pk=int(id))
    return render_to_response('account/info.html', {'user': user, 'account_usertype_dict':account_usertype_dict}, context_instance=RequestContext(request))

@login_required
def register(request):

    if request.POST:
        username = request.POST.get('org.username',None)
        password = request.POST.get('password',None)
        confirmpwd = request.POST.get('confirmpwd',None)
        password = username
        confirmpwd = username
        email = request.POST.get('org.email',None)
        
        role_name_str = request.POST.get('org.role_name', None)
        
        department = request.POST.get('org.parent_organization_name',None)
        if department:
            try:
                organization = Organization.objects.get(organization_name__iexact=department)
            except:
                return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'部门无效请重新选择或置空'}), mimetype='application/json')
        
        
        phone = request.POST.get('phone',None)
        '''验证重复帐号名'''
        usernames = User.objects.filter(username__iexact=username)
        '''验证重复email'''
        emails = User.objects.filter(email__iexact=email)
        if usernames:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'用户名已经存在不能添加', "info":u'用户名已经存在不能添加',"result":u'用户名已经存在不能添加'}), mimetype='application/json')
        
        '''验证用户名是否存在于LDAP中'''
        if not add_validate_ldap(username):
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'用户名无效不能填加'}), mimetype='application/json')
        
        '''验证两次输入密码是否一致'''
        if password != confirmpwd:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'两次密码输入不一致', "info":u'两次密码输入不一致',"result":u'两次密码输入不一致'}), mimetype='application/json')
        
        if emails:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'EMAIL已经存在不能添加', "info":u'EMAIL已经存在不能添加',"result":u'EMAIL已经存在不能添加'}), mimetype='application/json')
        if password != None and password != '':
            password = make_password(password, salt=None, hasher='default')
            user = User(username=username, password=password, email=email)
        else:
            user = User(username=username, email=email)
        user.save()
        userprofile = UserProfile(user=user, department=department, phone=phone)
        userprofile.save()
        
        if role_name_str != None and role_name_str != '':
            role_name_list = role_name_str.split(',')
            for role_name in role_name_list:
                if role_name != None and role_name != '':
                    try:
                        role = Role.objects.get(role_name__exact=role_name)
                        role.users.add(user)
                    except:
                        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'存在无效角色名请重新选择或置空'}), mimetype='application/json')
        
        '''用户添加成功后给它发送邮件提示'''
        subject = u'创建用户成功'
        to_mail_list = ['dashan.yin@autonavi.com', 'shandayin@foxmail.com']
        # 定义邮件内容
        email = u"您好，现在已为您创建了登录运维自动化系统的用户！"
        url = u"运维自动化系统地址: 10.2.161.15:89"
        loginusername = u"用户名: " + user.username
        loginpassword = u"密码为公司邮件系统中的密码"
        body = loader.render_to_string('account/mail.html', {'email':email, 'url':url, 'loginusername':loginusername, 'loginpassword':loginpassword})
        send_mail(subject, body, from_email, to_mail_list, html="text/html")
        
        Log(username=request.user.username, content=u"成功创建用户: " + username, level=1).save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
    else:
        return render_to_response('account/register.html', {'account_usertype_dict':account_usertype_dict})
    
@login_required
def edit(request, id):
    user = get_object_or_404(User,pk=int(id))
    userprofile=get_object_or_404(UserProfile,user_id=int(id))
    if request.POST:
        user.username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        password = user.username
        if password != None and password != '':
            user.password = make_password(password, salt=None, hasher='default')
        
        role_name_str = request.POST.get('org.role_name', None)
        
        user.email = request.POST.get('email',None)
        department = request.POST.get('org.parent_organization_name',None)
        if department:
            try:
                organization = Organization.objects.get(organization_name__iexact=department)
            except:
                return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'部门无效请重新选择或置空'}), mimetype='application/json')
        
        userprofile.department = department
        userprofile.phone = request.POST.get('phone',None)
        user.save()
        userprofile.save()
        
        roles = user.role_set.all()
        for role in roles:
            role.users.remove(user)
        if role_name_str != None and role_name_str != '':
            role_name_list = role_name_str.split(',')
            for role_name in role_name_list:
                if role_name != None and role_name != '':
                    try:
                        role = Role.objects.get(role_name__exact=role_name)
                        role.users.add(user)
                    except:
                        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'存在无效角色名请重新选择或置空'}), mimetype='application/json')
            
        Log(username=request.user.username, content=u"成功修改用户: " + user.username, level=1).save()
        return HttpResponse(simplejson.dumps({"status":1, "statusCode":200, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功', "info":u'编辑成功',"result":u'编辑成功'}), mimetype='application/json')
    
    roles = user.role_set.all()
    role_list = []
    for role in roles:
        role_list.append(role.role_name)
    retdir = {'user': user, 'account_usertype_dict':account_usertype_dict, 'role_list':role_list}
    return render_to_response('account/edit.html', retdir, context_instance=RequestContext(request))
    
        
def login(request):
    '''登陆视图'''
    template_var={}
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST.copy())
        if form.is_valid():
            ret = False
            ret = _login(request,form.cleaned_data["username"],form.cleaned_data["password"])
            if ret:
                '''
                       获取用户对应的所有角色,根据角色生成相应的权限列表并把权限列表放到session里面
                '''
                roles = request.user.role_set.all()
                # 模块权限列表
                authority_list_module = []
                # 功能按钮权限列表
                authority_list_button = []
                # 模块字段权限列表
                authority_list_modulefield = []
                
                for role in roles:
                    modules = role.modules.all()
                    buttons = role.buttons.all()
                    modulefields = role.modulefields.all()
                    for module in modules:
                        auth_identify = module.module_type
                        if auth_identify not in authority_list_module:
                            authority_list_module.append(auth_identify)
                    for button in buttons:
                        auth_identify = button.module.module_type + button.button_type
                        if auth_identify not in authority_list_button:
                            authority_list_button.append(auth_identify)
                    for modulefield in modulefields:
                        auth_identify = modulefield.module.module_type + modulefield.modulefield_type
                        if auth_identify not in authority_list_modulefield:
                            authority_list_modulefield.append(auth_identify)
                        
                # 把权限列表放到session里面
                request.session["authority_list_module"] = authority_list_module
                request.session["authority_list_button"] = authority_list_button
                request.session["authority_list_modulefield"] = authority_list_modulefield
                    
                    
                # 获取登录IP
                RemoteIp = request.META.get('REMOTE_ADDR')
                Log(username=request.user.username, content=u"成功登录用户: " + request.user.username + u"，对应ip地址: " + RemoteIp, level=1).save()
                return render_to_response("common/index.html", {'account_usertype_dict':account_usertype_dict}, context_instance=RequestContext(request))
            else:
                vardict = {
                    "message": u"登录失败！"
                }
                Log(username=form.cleaned_data["username"], content=u"用户登录失败！", level=1).save()
                return render_to_response("account/login.html", vardict, context_instance=RequestContext(request))
                
    template_var["form"]=form        
    return render_to_response("account/login.html", template_var, context_instance=RequestContext(request))


def _login(request,username,password):
    if username == 'admin':
        pass
    else:
        # LDAP验证
        if login_ldap(username,password):
            pass
        else:
            return False
    '''登陆核心方法'''
    ret = False
    user = authenticate(username=username,password=username)
    if user:
        if user.is_active:
            auth_login(request, user)
            ret = True
        else:
            messages.add_message(request, messages.INFO, _(u'用户没有激活'))
    else:
        messages.add_message(request, messages.INFO, _(u'用户不存在'))
    return ret

@login_required
def logout(request):
    username = request.user.username
    '''注销视图'''
    auth_logout(request)
    Log(username=username, content=u"用户注销成功!", level=1).save()
    return render_to_response("account/login.html", {}, context_instance=RequestContext(request))

@login_required
def delete(request,id):
    user = User.objects.get(id=id)
    if request.user.is_authenticated():
        if request.user.username == user.username:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'不能删除自己'}), mimetype='application/json')
        else:
            Log(username=request.user.username, content=u"成功删除用户: " + user.username, level=1).save()
            user.delete()
    return HttpResponse(simplejson.dumps({"status":1, "statusCode":200, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'删除成功', "info":u'删除成功',"result":u'删除成功'}), mimetype='application/json')

@login_required
def selecteddelete(request):
    ids = request.POST.get('ids', None)
    if ids:
        users = User.objects.extra(where=['id IN ('+ ids +')'])
        for user in users:
            if request.user.username == user.username:
                return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'选中的用户组中包含自己不能批量删除'}), mimetype='application/json')
            Log(username=request.user.username, content=u"成功批量删除用户: " + user.username, level=1).save()
        users.delete()
        return HttpResponse(simplejson.dumps({"status":1, "statusCode":200, "navTabId":request.POST.get('navTabId','accountindex'), "callbackType":request.POST.get('callbackType',None), "message":u'删除成功', "info":u'删除成功',"result":u'删除成功'}), mimetype='application/json')


'''
** LDAP登录认证
'''
def login_ldap(username, password):
    ldapconf = get_ldapconf()
    if ldapconf == None:
        return False
    flag = False
    try:
#        Server = "ldap://10.2.145.102:389"
#        baseDN = "dc=autonavi,dc=com"
#        searchScope = ldap.SCOPE_SUBTREE
#        searchFilter = "sAMAccountName=" + username
#        username = 'autonavi\\' + username
        Server = ldapconf.server
        baseDN = ldapconf.base_dn
        searchScope = ldap.SCOPE_SUBTREE
        searchFilter = ldapconf.loginname + "=" + username
        username = ldapconf.domainname + "\\" + username
        retrieveAttributes = None
        conn = ldap.initialize(Server)
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.protocol_version = ldap.VERSION3
        conn.simple_bind_s(username, password)
        print "connect ldap success"
        flag = True
    except ldap.LDAPError, e:
        flag = False
    return flag


'''
** 添加用户时认证LDAP中是否有该用户名
'''
def add_validate_ldap(validateusername):
    ldapconf = get_ldapconf()
    if ldapconf == None:
        return False
    username = ldapconf.username
    password = ldapconf.password
    flag = False
    try:
        Server = ldapconf.server
        baseDN = ldapconf.base_dn
        searchScope = ldap.SCOPE_SUBTREE
        searchFilter = ldapconf.loginname + "=" + validateusername
        username = ldapconf.domainname + "\\" + username
        retrieveAttributes = None
        conn = ldap.initialize(Server)
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.protocol_version = ldap.VERSION3
        conn.simple_bind_s(username, password)
        print "connect ldap success"
        ldap_result_id = conn.search(baseDN, searchScope, searchFilter, retrieveAttributes)
        result_set = []
        while 1:
            result_type, result_data = conn.result(ldap_result_id, 0)
            if(result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
                    Name,Attrs = result_data[0]
                    if hasattr(Attrs, 'has_key') and Attrs.has_key('mail'):
                        print Attrs['mail'][0]
                    if hasattr(Attrs, 'has_key') and Attrs.has_key('sAMAccountName'):
                        print Attrs['sAMAccountName'][0]
                    flag = True  
        
    except ldap.LDAPError, e:
        flag = False
    return flag



@login_required
def searchback_role(request):
    retdir = {}
    roles = Role.objects.order_by('-id')
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        roles = roles.filter(role_name__icontains = query)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(roles, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        roles = paginator.page(page)
    except (EmptyPage, InvalidPage):
        roles = paginator.page(paginator.num_pages)
    tmpdir = {'roles':roles,'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('account/searchback.html', retdir)


@login_required
def searchback_ldap(request):
    retdir = {}
    ldapconf = get_ldapconf()
    username = ldapconf.domainname +'\\' + ldapconf.username 
    password = ldapconf.password
    baseDN = 'OU=高德集团,DC=autonavi,DC=com'
    
    if 'keyword_name' in request.POST and request.POST['keyword_name']:
        keyword_name = request.POST.get('keyword_name')
        keyword_name = keyword_name.strip().encode('utf-8')
#        searchFilter = '(|(CN=%s*)(mail=%s*))' % (keyword,keyword)
#        searchFilter = "mail=*" + keyword + "*"
        searchFilter = "name=*" + keyword_name + "*"
        retdir['keyword_name'] = keyword_name
    elif 'keyword_mail' in request.POST and request.POST['keyword_mail']:
        keyword_mail = request.POST.get('keyword_mail')
        keyword_mail = keyword_mail.strip().encode('utf-8')
        searchFilter = "mail=*" + keyword_mail + "*"
        retdir['keyword_mail'] = keyword_mail
    else:
        searchFilter = "sAMAccountName=*"
#        searchFilter = "sAMAccountName=''"
        
    retrieveAttributes = ['cn', 'title', 'telephoneNumber', 'physicalDeliveryOfficeName', 'department', 'mail', 'company', 'mailNickname']
    
    # 连接ldap服务器
    conn = ldap.initialize(ldapconf.server)
    conn.set_option(ldap.OPT_REFERRALS, 0)
    conn.protocol_version = ldap.VERSION3
    conn.simple_bind_s(username, password)
    try:
        result_list = conn.search_st(baseDN, ldap.SCOPE_SUBTREE, searchFilter, retrieveAttributes, timeout=10)
        user_list = []
        for item in result_list:
            temp = {}
            if item[1].has_key('cn'):
                temp['cn'] = item[1]['cn'][0]
            else:
                temp['cn'] = ""
            if item[1].has_key('title'):
                temp['title'] = item[1]['title'][0]
            else:
                temp['title'] = ""
            if item[1].has_key('telephoneNumber'):
                temp['telephoneNumber'] = item[1]['telephoneNumber'][0]
            else:
                temp['telephoneNumber'] = ""
            if item[1].has_key('physicalDeliveryOfficeName'):
                temp['physicalDeliveryOfficeName'] = item[1]['physicalDeliveryOfficeName'][0]
            else:
                temp['physicalDeliveryOfficeName'] = ""
            if item[1].has_key('department'):
                temp['department'] = item[1]['department'][0]
            else:
                temp['department'] = ""
            if item[1].has_key('mail'):
                temp['mail'] = item[1]['mail'][0]
            else:
                temp['mail'] = ""
            if item[1].has_key('company'):
                temp['company'] = item[1]['company'][0]
            else:
                temp['company'] = ""
            if item[1].has_key('mailNickname'):
                temp['mailNickname'] = item[1]['mailNickname'][0]
            else:
                temp['mailNickname'] = ""
            user_list.append(temp)
    except BaseException:
        return  HttpResponseBadRequest("搜索失败或超时请检查搜索条件后重新搜索")
    
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(user_list, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        user_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        user_list = paginator.page(paginator.num_pages)
    tmpdir = {'user_list':user_list, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('account/searchback_ldap.html', retdir)


def autocomplete(request):
    if request.GET.has_key('q'):
        query = request.GET['q']
        if query != None:
            query = query.strip()
            users = User.objects.filter(username__icontains=query)
            return HttpResponse('\n'.join(user.username for user in users))
    return HttpResponse()
    

