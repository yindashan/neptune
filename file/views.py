#!usr/bin/env python
#coding: utf-8

from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext

# Imaginary function to handle an uploaded file.
from file.forms import UploadFileForm
import csv  

def upload_file(request):

    if request.POST:
        if request.FILES:
            handle_uploaded_file(request.FILES['file'])
            return render_to_response('file/success.html')
#            return HttpResponse(simplejson.dumps({"statusCode":200, "navTabId":request.POST.get('navTabId', 'serverindex'), "callbackType":request.POST.get('callbackType','closeCurrent'), "message":u'添加成功'}), mimetype='application/json')
    return render_to_response('file/upload.html', context_instance=RequestContext(request))
#    return render_to_response('file/upload.html', {'form': form}, context_instance=RequestContext(request))
    
'''
将f中的内容写到salt-vim-master.zip
'''
def handle_uploaded_file(f):
    destination = open('/usr/local/workspace/neptune/static/static/shell/neptune.sql', 'wb+')
#    destination = open('/usr/local/workspace/neptune/static/static/shell/salt-vim-master.zip', 'wb+')
#    lines = f.readlines()
#    destination.writelines(lines)
#    s2 = f.read()
#    for line in lines:
#        destination.writelines(line)
    for chunk in f.chunks():
        destination.write(chunk)
    destination.flush()
    destination.close()


def download_file(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=d:\my.csv'
    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    return response
    
