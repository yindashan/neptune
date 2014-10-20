#!usr/bin/env python
#coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from utils.authority_data import authority_data

from authority.models import Module
from authority.models import ModuleField
from authority.models import Button
from authority.models import Role


'''根据用户名获取用户所属角色'''
def get_roles(request, username):
    # 对用户名进行解码
    username = username.replace("____", ".")
    user = User.objects.get(username__exact=username)
    roles = user.role_set.all()
    role_str = "role_list"
    for role in roles:
        # print unicode(role.id) + ":" + role.role_name
        role_str += "::" + unicode(role.id) + "::" + role.role_name
    return HttpResponse(role_str)


'''从配置文件中获取所有模块'''
def get_modules(request):
    module_json_list = authority_data['modules']['module']
    '''获取模块数据'''
    module_str = "module_list"
    for module in module_json_list:
        module_type = module['module_type']
        module_name =  module['module_name']
        module_str += "::" + module_type + "::" + module_name
    return HttpResponse(module_str)

'''从数据库中获取所有模块'''
def get_modules_db(request):
    modules = Module.objects.all()
    '''获取模块数据'''
    module_str = "module_list"
    for module in modules:
        module_str += "::" + module.module_type + "::" + module.module_name
    return HttpResponse(module_str)



'''根据模块类型获取相应的功能按钮'''
def get_buttons(request, module_type):
    module_json_list = authority_data['modules']['module']
    '''根据模块类型获取功能按钮数据'''
    button_str = "button_list"
    for module in module_json_list:
        # module是一个字典
        if module['module_type'] == module_type:
            '''获取功能按钮数据'''
            button_json_list = module['buttons']['button']
            for button in button_json_list:
                button_type = button['button_type']
                button_name = button['button_name']
                button_str += "::" + button_type + "::" + button_name
            break
    return HttpResponse(button_str)

'''根据模块类型获取相应的模块字段'''
def get_modulefields(request, module_type):
    module_json_list = authority_data['modules']['module']
    '''根据模块类型获取模块字段数据'''
    modulefield_str = "modulefield_list"
    for module in module_json_list:
        # module是一个字典
        if module['module_type'] == module_type:
            '''获取模块字段数据'''
            modulefield_json_list = module['fields']['field']
            for modulefield in modulefield_json_list:
                modulefield_type = modulefield['field_type']
                modulefield_name = modulefield['field_name']
                modulefield_str += "::" + modulefield_type + "::" + modulefield_name
            break
    return HttpResponse(modulefield_str)



'''功能节点(模块)'''
@login_required
def index_module(request):
    retdir = {}
    modules = Module.objects.all()
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        modules = modules.filter(module_name__icontains = query)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(modules, numPerPage)
    page = request.POST.get('pageNum',1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        modules = paginator.page(page)
    except (EmptyPage, InvalidPage):
        modules = paginator.page(paginator.num_pages)
        
    tmpdir = {'modules':modules, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('authority/module/basepage.html', retdir)


@login_required
def add_module(request):
    if request.POST:
        # 由于下拉框的设置request.POST.get('module_name')就表示module_type
        module_type = request.POST.get('module_name', None)
        
        if module_type == '' or module_type == None or module_type == '-1':
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','moduleindex'), "callbackType":request.POST.get('callbackType', None), "message":u'请选择关联模块！'}), mimetype='application/json')
        
        module_name = ''
        module_json_list = authority_data['modules']['module']
        for module in module_json_list:
            if module['module_type'] == module_type:
                module_name =  module['module_name']
                break
        order = request.POST.get('order', None)
        module_desc = request.POST.get('module_desc', None)
        
        '''验证重复模块名'''
        module_names = Module.objects.filter(module_name__iexact=module_name)
        if module_names:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','moduleindex'), "callbackType":request.POST.get('callbackType', None), "message":u'模块名已经存在不能添加'}), mimetype='application/json')
        
        module = Module(module_name=module_name, module_type=module_type, order=int(order), module_desc=module_desc)
        module.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','moduleindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
    else:
        # 弹出新建窗口
        return render_to_response('authority/module/add.html')

@login_required
def edit_module(request, id):
    module=get_object_or_404(Module,pk=int(id))
    if request.POST:
        module.module_name = request.POST.get('module_name', None)
        module.module_type = request.POST.get('module_type', None)
        module.order = request.POST.get('order', None)
        module.module_desc = request.POST.get('module_desc', None)
        
        module.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','moduleindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    return render_to_response('authority/module/edit.html', {'module': module})        

@login_required
def delete_module(request, id):
    module = Module.objects.get(id=id)
    buttons = module.button_set.all()
    modulefields = module.modulefield_set.all()
    if buttons:
        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','moduleindex'), "callbackType":request.POST.get('callbackType', None), "message":u'该模块下面有关联按钮不能删除'}), mimetype='application/json')
    if modulefields:
        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','moduleindex'), "callbackType":request.POST.get('callbackType', None), "message":u'该模块下面有关联模块字段不能删除'}), mimetype='application/json')
    module.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','moduleindex'), "callbackType":request.POST.get('callbackType',''), "message":u'删除成功'}), mimetype='application/json')

@login_required
def selecteddelete_module(request):
    ids = request.POST.get('ids', None)
    if ids:
        buttons = Button.objects.extra(where=['module_id IN ('+ ids +')'])
        if buttons:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','moduleindex'), "callbackType":request.POST.get('callbackType',None), "message":u'选中模块下面有关联按钮不能批量删除'}), mimetype='application/json')
        modulefields = ModuleField.objects.extra(where=['module_id IN ('+ ids +')'])
        if modulefields:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','moduleindex'), "callbackType":request.POST.get('callbackType',None), "message":u'选中模块下面有关联模块字段不能批量删除'}), mimetype='application/json')
        modules = Module.objects.extra(where=['id IN ('+ ids +')'])
        modules.delete()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','moduleindex'), "callbackType":request.POST.get('callbackType',''), "message":u'选中项删除成功'}), mimetype='application/json')



'''节点里的字段'''
@login_required
def index_modulefield(request):
    retdir = {}
    modulefields = ModuleField.objects.all()
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        modulefields = modulefields.filter(modulefield_name__icontains = query)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
        
    paginator = Paginator(modulefields, numPerPage)
    page = request.POST.get('pageNum',1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        modulefields = paginator.page(page)
    except (EmptyPage, InvalidPage):
        modulefields = paginator.page(paginator.num_pages)
        
    tmpdir = {'modulefields':modulefields, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('authority/modulefield/basepage.html', retdir)


@login_required
def add_modulefield(request):
    if request.POST:
        # 由于下拉框的设置request.POST.get('module_name')就表示module_type
        module_type = request.POST.get('module_name', None)
        '''通过模块类型验证模块是否存在'''
        try:
            module_obj = Module.objects.get(module_type__iexact=module_type)
        except:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'modulefieldindex'), "callbackType":request.POST.get('callbackType', None), "message":u'请选择关联模块！'}), mimetype='application/json')
        # 由于下拉框的设置request.POST.get('button_name')就表示button_type
        modulefield_type = request.POST.get('modulefield_name', None)
        if modulefield_type == '' or modulefield_type == None:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'modulefieldindex'), "callbackType":request.POST.get('callbackType', None), "message":u'该模块下不存在关联字段不能添加'}), mimetype='application/json')
            
        '''通过模块类型和模块字段类型验证该模块字段是否已经存在'''
        modulefields = ModuleField.objects.filter(modulefield_type__iexact=modulefield_type, module__module_type__iexact=module_type)
        if modulefields:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'modulefieldindex'), "callbackType":request.POST.get('callbackType', None), "message":u'该模块字段已添加请添加其他字段'}), mimetype='application/json')
        flag = False
        modulefield_name = ''
        module_json_list = authority_data['modules']['module']
        for module in module_json_list:
            if module['module_type'] == module_type:
                '''根据modulefield_type获取modulefield_name'''
                modulefield_json_list = module['fields']['field']
                for modulefield in modulefield_json_list:
                    if modulefield['field_type'] == modulefield_type:
                        modulefield_name = modulefield['field_name']
                        flag = True
                        break
            if flag == True:
                break
        
        order = request.POST.get('order', None)
        modulefield = ModuleField(modulefield_name=modulefield_name, modulefield_type=modulefield_type, order=int(order))
        modulefield.module = module_obj
        modulefield.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','modulefieldindex'), "callbackType":request.POST.get('callbackType', 'closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
    else:
        # 弹出新建窗口
        return render_to_response('authority/modulefield/add.html')

@login_required
def edit_modulefield(request, id):
    modulefield=get_object_or_404(ModuleField, pk=int(id))
    if request.POST:
        modulefield.modulefield_name = request.POST.get('modulefield_name', None)
        modulefield.modulefield_type = request.POST.get('modulefield_type', None)
        modulefield.order = request.POST.get('order', None)
        
        modulefield.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','modulefieldindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    return render_to_response('authority/modulefield/edit.html', {'modulefield': modulefield})        

@login_required
def delete_modulefield(request,id):
    modulefield = ModuleField.objects.get(id=id)
    modulefield.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','modulefieldindex'), "callbackType":request.POST.get('callbackType',''), "message":u'删除成功'}), mimetype='application/json')

@login_required
def selecteddelete_modulefield(request):
    ids = request.POST.get('ids', None)
    if ids:
        id_list = ids.split(",")
        for id_tmp in id_list:
            modulefield = ModuleField.objects.get(id=int(id_tmp))
            modulefield.delete()
        #modulefields = ModuleField.objects.extra(where=['id IN ('+ ids +')'])
        #modulefields.delete()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','modulefieldindex'), "callbackType":request.POST.get('callbackType',''), "message":u'选中项删除成功'}), mimetype='application/json')



'''功能按钮(添加、修改、删除等)'''
@login_required
def index_button(request):
    retdir = {}
    buttons = Button.objects.all()
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        buttons = buttons.filter(button_name__icontains = query)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
        
    paginator = Paginator(buttons, numPerPage)
    page = request.POST.get('pageNum',1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        buttons = paginator.page(page)
    except (EmptyPage, InvalidPage):
        buttons = paginator.page(paginator.num_pages)
        
    tmpdir = {'buttons':buttons, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('authority/button/basepage.html', retdir)


@login_required
def add_button(request):
    if request.POST:
        # 由于下拉框的设置request.POST.get('module_name')就表示module_type
        module_type = request.POST.get('module_name', None)
        '''通过模块类型验证模块是否存在'''
        try:
            module_obj = Module.objects.get(module_type__iexact=module_type)
        except:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'buttonindex'), "callbackType":request.POST.get('callbackType', None), "message":u'请选择关联模块！'}), mimetype='application/json')
        
        # 由于下拉框的设置request.POST.get('button_name')就表示button_type
        button_type = request.POST.get('button_name', None)
        if button_type == '' or button_type == None:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'buttonindex'), "callbackType":request.POST.get('callbackType', None), "message":u'该模块下不存在功能按钮不能添加'}), mimetype='application/json')
            
        '''通过模块类型和功能按钮类型验证该功能按钮是否已经存在'''
        buttons = Button.objects.filter(button_type__iexact=button_type, module__module_type__iexact=module_type)
        if buttons:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'buttonindex'), "callbackType":request.POST.get('callbackType', None), "message":u'该功能按钮已添加请添加其他按钮'}), mimetype='application/json')
        
        flag = False
        button_name = ''
        module_json_list = authority_data['modules']['module']
        for module in module_json_list:
            if module['module_type'] == module_type:
                '''根据button_type获取button_name'''
                button_json_list = module['buttons']['button']
                for button in button_json_list:
                    if button['button_type'] == button_type:
                        button_name = button['button_name']
                        flag = True
                        break
            if flag == True:
                break
         
        order = request.POST.get('order', None)
        
        button = Button(button_name=button_name, button_type=button_type, order=order)
        button.module = module_obj
        button.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'buttonindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
    else:
        # 弹出新建窗口
        return render_to_response('authority/button/add.html')

@login_required
def edit_button(request, id):
    button=get_object_or_404(Button, pk=int(id))
    if request.POST:
        module_name = request.POST.get('org.module_name', None)
        module = Module.objects.get(module_name__exact=module_name)
        button.module = module
        button.button_name = request.POST.get('button_name', None)
        button.button_type = request.POST.get('button_type', None)
        button.order = request.POST.get('order', None)
        
        button.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','buttonindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    return render_to_response('authority/button/edit.html', {'button': button})        

@login_required
def delete_button(request, id):
    button = Button.objects.get(id=id)
    button.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','buttonindex'), "callbackType":request.POST.get('callbackType',''), "message":u'删除成功'}), mimetype='application/json')

@login_required
def selecteddelete_button(request):
    ids = request.POST.get('ids', None)
    if ids:
        id_list = ids.split(",")
        for id_tmp in id_list:
            button = Button.objects.get(id=int(id_tmp))
            button.delete()
        #buttons = Button.objects.extra(where=['id IN ('+ ids +')'])
        #buttons.delete()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','buttonindex'), "callbackType":request.POST.get('callbackType',''), "message":u'选中项删除成功'}), mimetype='application/json')



@login_required
def searchback_button(request):
    retdir = {}
    modules = Module.objects.all()
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        modules = modules.filter(module_name__icontains = query)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(modules, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        modules = paginator.page(page)
    except (EmptyPage, InvalidPage):
        modules = paginator.page(paginator.num_pages)
    tmpdir = {'modules':modules,'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('authority/button/searchback.html', retdir, context_instance=RequestContext(request))



'''角色'''
@login_required
def index_role(request):
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
    page = request.POST.get('pageNum',1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        roles = paginator.page(page)
    except (EmptyPage, InvalidPage):
        roles = paginator.page(paginator.num_pages)
        
    tmpdir = {'roles':roles, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('authority/role/basepage.html', retdir)


@login_required
def add_role(request):
    if request.POST:
        role_name = request.POST.get('role_name', None)
        role_desc = request.POST.get('role_desc', None)
        
        '''验证重复角色名'''
        role_names = Role.objects.filter(role_name__iexact=role_name)
        if role_names:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','roleindex'), "callbackType":request.POST.get('callbackType', None), "message":u'角色名已经存在不能添加'}), mimetype='application/json')
        
        role = Role(role_name=role_name, role_desc=role_desc)
        role.save()
        
        username_str = request.POST.get('org.username', None)
        if username_str != None and username_str != '':
            username_list = username_str.split(',')
            for username in username_list:
                if username != None and username != '':
                    try:
                        user = User.objects.get(username__exact=username)
                        role.users.add(user)
                    except:
                        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','roleindex'), "callbackType":request.POST.get('callbackType', None), "message":u'存在无效用户名请重新选择或置空'}), mimetype='application/json')

        module_list = request.POST.getlist('modulecheckbox', None)
        for module_id in module_list:
            module = get_object_or_404(Module, pk=int(module_id))
            role.modules.add(module)
        button_list = request.POST.getlist('buttoncheckbox', None)
        for button_id in button_list:
            button = get_object_or_404(Button, pk=int(button_id))
            role.buttons.add(button)
        modulefield_list = request.POST.getlist('modulefieldcheckbox', None)
        for modulefield_id in modulefield_list:
            modulefield = get_object_or_404(ModuleField, pk=int(modulefield_id))
            role.modulefields.add(modulefield)
            
        role.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','roleindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
    else:
        # 弹出新建窗口
        retdir = {}
        modules = Module.objects.all()
        tmpdir = {'modules':modules}
        retdir.update(tmpdir)
        return render_to_response('authority/role/add.html', retdir)

@login_required
def edit_role(request, id):
    role = get_object_or_404(Role, pk=int(id))
    if request.POST:
        role.role_name = request.POST.get('role_name', None)
        role.role_desc = request.POST.get('role_desc', None)
        
        # 清空多对多关联
        username_str = request.POST.get('org.username', None)
        if username_str != None and username_str != '':
            role.users.clear()
            username_list = username_str.split(',')
            for username in username_list:
                if username != None and username != '':
                    try:
                        user = User.objects.get(username__exact=username)
                        role.users.add(user)
                    except:
                        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId','roleindex'), "callbackType":request.POST.get('callbackType', None), "message":u'存在无效用户名请重新选择或置空'}), mimetype='application/json')

        role.modules.clear()
        module_list = request.POST.getlist('modulecheckbox', None)
        for module_id in module_list:
            module = get_object_or_404(Module, pk=int(module_id))
            role.modules.add(module)
        role.buttons.clear()
        button_list = request.POST.getlist('buttoncheckbox', None)
        for button_id in button_list:
            button = get_object_or_404(Button, pk=int(button_id))
            role.buttons.add(button)
        role.modulefields.clear()
        modulefield_list = request.POST.getlist('modulefieldcheckbox', None)
        for modulefield_id in modulefield_list:
            modulefield = get_object_or_404(ModuleField, pk=int(modulefield_id))
            role.modulefields.add(modulefield)
        
        role.save()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','roleindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    
    users = role.users.all()
    user_list = []
    for user in users:
        user_list.append(user.username)
    retdir = {'role':role, 'user_list':user_list}
    #modules = role.modules.all()
    modules = Module.objects.all() # 注意这里的modules取的是全部的modules,而不只是当前角色所属的modules
    tmpdir = {'modules':modules}
    retdir.update(tmpdir)
    return render_to_response('authority/role/edit.html', retdir)

@login_required
def delete_role(request, id):
    role = Role.objects.get(id=id)
    role.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','roleindex'), "callbackType":request.POST.get('callbackType',''), "message":u'删除成功'}), mimetype='application/json')

@login_required
def selecteddelete_role(request):
    ids = request.POST.get('ids', None)
    if ids:
        roles = Role.objects.extra(where=['id IN ('+ ids +')'])
        roles.delete()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId','roleindex'), "callbackType":request.POST.get('callbackType',''), "message":u'选中项删除成功'}), mimetype='application/json')



@login_required
def searchback_role_user(request):
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
    tmpdir = {'users':users,'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('authority/role/searchbackuser.html', retdir, context_instance=RequestContext(request))


@login_required
def relate_role_user(request, id):
    role = get_object_or_404(Role, pk=int(id))
    users = role.users.all()
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
    return render_to_response('authority/role/relateuser.html', {'role':role, 'users':users, 'id':id, 'currentPage':page, 'numPerPage':numPerPage})


@login_required
def relate_role_module(request, id):
    role = get_object_or_404(Role, pk=int(id))
    modules = role.modules.all()
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(modules, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        modules = paginator.page(page)
    except (EmptyPage, InvalidPage):
        modules = paginator.page(paginator.num_pages)
    return render_to_response('authority/role/relatemodule.html', {'role':role, 'modules':modules, 'id':id, 'currentPage':page, 'numPerPage':numPerPage})


@login_required
def relate_role_button(request, id):
    role = get_object_or_404(Role, pk=int(id))
    buttons = role.buttons.all()
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(buttons, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        buttons = paginator.page(page)
    except (EmptyPage, InvalidPage):
        buttons = paginator.page(paginator.num_pages)
    return render_to_response('authority/role/relatebutton.html', {'role':role, 'buttons':buttons, 'id':id, 'currentPage':page, 'numPerPage':numPerPage})


@login_required
def relate_role_modulefield(request, id):
    role = get_object_or_404(Role, pk=int(id))
    modulefields = role.modulefields.all()
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(modulefields, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        modulefields = paginator.page(page)
    except (EmptyPage, InvalidPage):
        modulefields = paginator.page(paginator.num_pages)
    return render_to_response('authority/role/relatemodulefield.html', {'role':role, 'modulefields':modulefields, 'id':id, 'currentPage':page, 'numPerPage':numPerPage})


def autocomplete_module(request):
    if request.GET.has_key('q'):
        query = request.GET['q']
        if query != None:
            query = query.strip()
            modules = Module.objects.filter(module_name__icontains=query)
            return HttpResponse('\n'.join(module.module_name for module in modules))
    return HttpResponse()


def autocomplete_role(request):
    if request.GET.has_key('q'):
        query = request.GET['q']
        if query != None:
            query = query.strip()
            roles = Role.objects.filter(role_name__icontains=query)
            return HttpResponse('\n'.join(role.role_name for role in roles))
    return HttpResponse()
    




