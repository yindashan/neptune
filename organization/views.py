#!usr/bin/env python
#coding: utf-8

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from log.models import Log
from organization.models import Organization

@login_required
def index(request):
    retdir = {}
    organizations = Organization.objects.all()
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        organizations = organizations.filter(organization_name__icontains = query)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(organizations, numPerPage) # 每页显示数目
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        organizations = paginator.page(page)
    except (EmptyPage, InvalidPage):
        organizations = paginator.page(paginator.num_pages)
    tmpdir = {'organizations':organizations, 'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('organization/basepage.html', retdir, context_instance=RequestContext(request))
    
    
@login_required
def add(request):
    
    if request.POST:

        organization_name = request.POST.get('organization_name', None)
        organization_desc = request.POST.get('organization_desc', None)
        level = request.POST.get('level', None)
        parent_organization_name = request.POST.get('org.parent_organization_name', None)
        
        
        #验证重复组织机构名称
        organization_names = Organization.objects.filter(organization_name__iexact=organization_name)
        if organization_names:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'organizationindex'), "callbackType":request.POST.get('callbackType',None), "message":u'组织机构名称已经存在不能添加'}), mimetype='application/json')
        else:
            organization = Organization(organization_name=organization_name, organization_desc=organization_desc, level=level)
            organization.save()
            
            if parent_organization_name != None and parent_organization_name != '':
                try:
                    parent_organization = Organization.objects.get(organization_name__iexact=parent_organization_name)
                except:
                    return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'organizationindex'), "callbackType":request.POST.get('callbackType',None), "message":u'父级组织机构无效请重新选择或置空'}), mimetype='application/json')
                organization.parent_organization = parent_organization
            else:
                organization.parent_organization = organization
                
            organization.save()
            Log(username=request.user.username, content=u"成功添加组织机构信息: " + organization.organization_name, level=1).save()
            return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'organizationindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
        
    return render_to_response('organization/add.html')

@login_required
def edit(request, id):
    
    organization = get_object_or_404(Organization, pk=int(id))
    if request.POST:
        organization_name = request.POST.get('organization_name', None)
        organization_desc = request.POST.get('organization_desc', None)
        level = request.POST.get('level', None)
        parent_organization_name = request.POST.get('org.parent_organization_name', None)
        
        try:
            parent_organization = Organization.objects.get(organization_name__iexact=parent_organization_name)
        except:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'organizationindex'), "callbackType":request.POST.get('callbackType',None), "message":u'父级组织机构无效请重新选择或置空'}), mimetype='application/json')
        organization.parent_organization = parent_organization
        
        organization.organization_name = organization_name
        organization.organization_desc = organization_desc
        organization.level = level
        organization.save()
        
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'organizationindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'编辑成功'}), mimetype='application/json')
    
    return render_to_response('organization/edit.html', {'organization': organization})


@login_required
def delete(request, id):
    organization = Organization.objects.get(id=id)
    # 关联查询
    #organizations = organization.organization_set.all()
    organizations = Organization.objects.extra(where=['parent_organization_id IN ('+ str(organization.id) +') and id NOT IN ('+ str(organization.id) +')'])
    if organizations:
        return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'organizationindex'), "callbackType":request.POST.get('callbackType', None), "message":u'该组织机构有下属组织机构不能删除'}), mimetype='application/json')
    Log(username=request.user.username, content=u"成功删除组织机构信息: " + organization.organization_name, level=1).save()
    organization.delete()
    return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'organizationindex'), "callbackType":request.POST.get('callbackType', None), "message":u'删除成功'}), mimetype='application/json')

@login_required
def selecteddelete(request):
    ids = request.POST.get('ids', None)
    if ids:
        #organizations = Organization.objects.extra(where=['parent_organization_id IN ('+ ids +')'])
        organizations = Organization.objects.extra(where=['parent_organization_id IN ('+ ids +') and id NOT IN ('+ ids +')'])
        if organizations:
            return HttpResponse(simplejson.dumps({"statusCode":302, "navTabId":request.POST.get('navTabId', 'organizationindex'), "callbackType":request.POST.get('callbackType', None), "message":u'该组织机构有下属组织机构不能删除'}), mimetype='application/json')
        
        organizations = Organization.objects.extra(where=['id IN ('+ ids +')'])
        for organization in organizations:
            Log(username=request.user.username, content=u"成功批量删除组织机构信息: " + organization.organization_name, level=1).save()
        organizations.delete()
        return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'organizationindex'), "callbackType":request.POST.get('callbackType', None), "message":u'删除成功'}), mimetype='application/json')


@login_required
def searchback(request):
    retdir = {}
    organizations = Organization.objects.all()
    if 'query' in request.POST and request.POST['query']:
        query = request.POST['query']
        retdir['query'] = query
        organizations = organizations.filter(organization_name__icontains = query)
    if 'numPerPage' in request.POST and request.POST['numPerPage']:
        numPerPage = request.POST['numPerPage']
    else:
        numPerPage = 10
    paginator = Paginator(organizations, numPerPage)
    page = request.POST.get('pageNum', 1)
    try:
        if int(page) > paginator.num_pages:
            page = str(paginator.num_pages)
        organizations = paginator.page(page)
    except (EmptyPage, InvalidPage):
        organizations = paginator.page(paginator.num_pages)
    tmpdir = {'organizations':organizations,'currentPage':page, 'numPerPage':numPerPage}
    retdir.update(tmpdir)
    return render_to_response('organization/searchback.html', retdir, context_instance=RequestContext(request))



def autocomplete(request):
    if request.GET.has_key('q'):
        query = request.GET['q']
        if query != None:
            query = query.strip()
            organizations = Organization.objects.filter(organization_name__icontains=query)
            return HttpResponse('\n'.join(organization.organization_name for organization in organizations))
    return HttpResponse()
    
    