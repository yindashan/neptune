# -*- coding: utf-8 -*-
#from __future__ import absolute_import

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


# Import our libs
from .control import (
    wildcardtarget,
    get_salt_client,
    get_api_client,
    )
from .forms import LowdataForm

# Import Python libs
import json
import os
import stat
import sys
import threading

# Import third party libs
import yaml

# Import Django libs
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse

# Import REST libs
from rest_framework import status

from server.models import Server


'''
    线程类
'''
class SaltRequest_Salt(threading.Thread):
    def __init__(self, client, shell_result, minion, func, arg, lock, threadName):
        '''''@summary: 初始化对象。 
        @param client: salt client。
        @param shell_result: 返回结果字典。
        @param minion: minionid。
        @param func: func。
        @param arg: arg。
        @param lock: 琐对象。
        @param threadName: 线程名称。
        '''
        super(SaltRequest_Salt, self).__init__(name=threadName)
        self.client = client
        self.shell_result = shell_result
        self.minion = minion
        self.func = func
        self.arg = arg
        self.lock = lock
        
    def run(self):
        '''''@summary: 重写父类run方法，在线程启动后执行该方法内的代码.
        '''
        #self.lock.acquire()
        client = self.client
        shell_result = self.shell_result
        minion = self.minion
        func = self.func
        arg = self.arg
        shell_ret = client.cmd(minion, func, arg, ret='json')
        shell_result.update(shell_ret)
        #self.lock.release()



'''
    线程类
'''
class SaltRequest(threading.Thread):
    def __init__(self, client, shell_result, minion, shell_str, lock, threadName):
        '''''@summary: 初始化对象。 
        @param client: salt client。
        @param shell_result: 返回结果字典。
        @param minion: minionid。
        @param shell_str: shell_str。
        @param lock: 琐对象。
        @param threadName: 线程名称。
        '''
        super(SaltRequest, self).__init__(name=threadName)
        self.client = client
        self.shell_result = shell_result
        self.minion = minion
        self.shell_str = shell_str
        self.lock = lock
        
    def run(self):
        '''''@summary: 重写父类run方法，在线程启动后执行该方法内的代码.
        '''
        #self.lock.acquire()
        client = self.client
        shell_result = self.shell_result
        minion = self.minion
        shell_str = self.shell_str
        shell_ret = client.cmd(minion, 'cmd.run', [shell_str], ret='json')
        shell_result.update(shell_ret)
        #self.lock.release()



def JsonResponse(content, **kwargs):
    return HttpResponse(
        content=json.dumps(content),
        content_type='application/json',
        **kwargs)

# Externally accessible functions

#@login_required
@wildcardtarget
def ping(request, tgt):
    client = get_salt_client()
    ret = client.cmd(tgt, 'test.ping', ret='json')
    return JsonResponse(ret)

'''
    dashan.yin
'''
'''
Output data in YAML, this outputter defaults to printing in YAML block mode
for better readability.
'''




def __virtual__():
    return 'yaml'


def output(data):
    '''
    Print out YAML using the block mode
    '''
#    if 'output_indent' in __opts__:
#        if __opts__['output_indent'] >= 0:
#            return yaml.dump(
#                data, default_flow_style=False,
#                indent=__opts__['output_indent']
#            )
#        # Disable indentation
#        return yaml.dump(data, default_flow_style=True, indent=0)
    yaml_str = yaml.dump(data, default_flow_style=False)
    print yaml_str
    yaml_obj = yaml.load(yaml_str)
    print yaml_obj
    return HttpResponse(yaml_str)
    #return yaml.dump(data, default_flow_style=False)
    
    # yaml to json
    #render(yaml_str)
    
    
def testoutput(data):
    #response = HttpResponse(mimetype="text/html")
    response = HttpResponse(mimetype="text/plain")
    yaml_str = yaml.dump(data, default_flow_style=False)
    print yaml_str
    response.write(yaml_str)
    #response.write("<p>minion01:</p>")
    #response.write("<p>----------</p>")
    #response.write("<p>    State: - pkg</p>")
    #response.write("<p>    Name:      libpam-cracklib</p>")
    #response.write("<p>    Function:  installed</p>")
    #response.write("<p>        Result:    True</p>")
    #response.write("<p>        Comment:   Package libpam-cracklib is already installed</p>")
    #response.write("<p>        Changes:</p>")
    return response


@wildcardtarget
def pingoutput(request, tgt):
    client = get_salt_client()
    ret = client.cmd(tgt, 'state.highstate', ret='yaml')
    print ret
    #return output(ret)
    return testoutput(ret)



#@login_required
@wildcardtarget
def echo(request, tgt, arg):
    client = get_salt_client()
    ret = client.cmd(tgt, 'test.echo', arg, ret='json')
    return JsonResponse(ret)

#@login_required
def minions_list(request):
    client = get_salt_client()
    ret = client.cmd('*', 'grains.items', ret='json')
    return JsonResponse(ret)

#@login_required
def minions_details(request, tgt):
    client = get_salt_client()
    ret = client.cmd(tgt, 'grains.items', ret='json')
    return JsonResponse(ret)

#@login_required
def jobs_list(request):
    client = get_api_client()
    lowdata = {
        'client': 'runner',
        'fun': 'jobs.list_jobs',
        }
    ret = client.run(lowdata)
    return JsonResponse(ret)

#@login_required
def jobs_details(request, jid):
    client = get_api_client()
    lowdata = {
        'client': 'runner',
        'fun': 'jobs.lookup_jid',
        'jid': jid,
        }
    ret = client.run(lowdata)
    return JsonResponse(ret)

#@login_required
@csrf_exempt
def apiwrapper(request):
    if request.method == 'POST':
        form = LowdataForm(request.POST)

        if form.is_valid():
            client = get_api_client()
            lowdata = {
                'client': form.cleaned_data['client'],
                'tgt': form.cleaned_data['tgt'],
                'fun': form.cleaned_data['fun'],
                'arg': form.cleaned_data['arg'],
                }
            ret = client.run(lowdata)

            return JsonResponse(ret)
        else:
            ret = {
                'status': status.HTTP_400_BAD_REQUEST,
                'return': form.errors,
                }
            return JsonResponse(ret, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        return render(request, 'index.html')




'''
    dashan.yin
'''
@login_required
def index(request):
    retdir = {}
    return render_to_response('djangosalt/basepage.html', retdir, 
                              context_instance = RequestContext(request))


@wildcardtarget
def testping_original(request, tgt):
    client = get_salt_client()
    #ret = client.cmd(tgt, 'test.ping', ret='json')
    #ret = client.cmd(tgt, 'grains.items', ret='json') # true
    ret = client.cmd(tgt, 'state.highstate', ret='json') # true
    
    #ret = client.cmd(tgt, 'cmd.run', ['uname -a'], ret='yaml') # true
    
    # Import the Salt client library
    #import salt.client
    # create a local client object
    #client = salt.client.LocalClient()
    # make calls with the cmd method
    #ret = client.cmd(tgt, 'cmd.run', ['uname -a'], ret='yaml')
    
    
    #ret = client.cmd(tgt, 'test.echo', ret='json') # false
    #ret = client.cmd(tgt, 'uname -a', ret='json') # false
    #ret = client.cmd(tgt, 'cmd.run "uname -a"', ret='json') # false
    #return JsonResponse(ret)
    
    # 把json格式的数据转换成yaml格式的数据
    #yaml_str = yaml.dump(ret, default_flow_style=False)
    #print yaml_str
    
    
    retdir = {"result": ret}
    return render_to_response('djangosalt/basepage.html', retdir, 
                              context_instance = RequestContext(request))
    
    
    
@wildcardtarget
def testping(request, tgt):
    client = get_salt_client()
    #ret = client.cmd(tgt, 'test.ping', ret='json')
    #ret = client.cmd(tgt, 'grains.items', ret='json') # true
    ret = client.cmd(tgt, 'grains.item', ['os'], ret='json') # true
    #ret = client.cmd(tgt, 'state.highstate', ret='json') # true
    
    #ret = client.cmd(tgt, 'cmd.run', ['uname -a'], ret='json') # true
    #ret = client.cmd(tgt, 'cmd.run', ['cat /etc/issue'], ret='json') # true
    #ret = client.cmd(tgt, 'cmd.run', ['ls -l'], ret='json') # true
    
    # Import the Salt client library
    #import salt.client
    # create a local client object
    #client = salt.client.LocalClient()
    # make calls with the cmd method
    #ret = client.cmd(tgt, 'cmd.run', ['uname -a'], ret='yaml')
    
    
    #ret = client.cmd(tgt, 'test.echo', ret='json') # false
    #ret = client.cmd(tgt, 'uname -a', ret='json') # false
    #ret = client.cmd(tgt, 'cmd.run "uname -a"', ret='json') # false
    #return JsonResponse(ret)
    
    print ret
    response = HttpResponse(mimetype="text/plain") # 这行代码很重要text/plain而不是text/html
    # 把json格式的数据转换成yaml格式的数据
    yaml_str = yaml.dump(ret, default_flow_style=False)
    print yaml_str
    response.write(yaml_str)
    return response
    
    #retdir = {"result": ret}
    #return render_to_response('djangosalt/basepage.html', retdir, context_instance = RequestContext(request))

    
@wildcardtarget
def postping(request):
    ret = {}
    client = get_salt_client()
    if 'target' in request.POST and request.POST['target'] and 'func' in request.POST and request.POST['func']:
        target = request.POST['target']
        func = request.POST['func']
        if 'argument' in request.POST and request.POST['argument']:
            argument = request.POST['argument']
            ret = client.cmd(target, func, [argument], ret='json')
        else:
            ret = client.cmd(target, func, ret='json')
        
    #client = get_salt_client()
    #ret = client.cmd(tgt, 'test.ping', ret='json')
    #ret = client.cmd(tgt, 'grains.items', ret='json') # true
    #ret = client.cmd(tgt, 'grains.item', ['os'], ret='json') # true
    #ret = client.cmd(tgt, 'state.highstate', ret='json') # true
    
    #ret = client.cmd(tgt, 'cmd.run', ['uname -a'], ret='json') # true
    #ret = client.cmd(tgt, 'cmd.run', ['cat /etc/issue'], ret='json') # true
    #ret = client.cmd(tgt, 'cmd.run', ['ls -l'], ret='json') # true
    
    # Import the Salt client library
    #import salt.client
    # create a local client object
    #client = salt.client.LocalClient()
    # make calls with the cmd method
    #ret = client.cmd(tgt, 'cmd.run', ['uname -a'], ret='yaml')
    
    
    print ret
    response = HttpResponse(mimetype="text/plain") # 这行代码很重要text/plain而不是text/html
    # 把json格式的数据转换成yaml格式的数据
    yaml_str = yaml.dump(ret, default_flow_style=False)
    print yaml_str
    response.write(yaml_str)
    return response
    
    #retdir = {"result": ret}
    #return render_to_response('djangosalt/basepage.html', retdir, context_instance = RequestContext(request))


    
@wildcardtarget
def testpostping(request):
    ret = {}
    client = get_salt_client()
    
    ####################测试#####################
    if request.POST:
        target = request.POST.get('target', None)
        func = request.POST.get('func', None)
        argument = request.POST.get('argument', None)
        shellcontent = request.POST.get('shellcontent', None)
        print shellcontent
        
        # 用sessionid作为名称生成临时文件，因为sessionid是不可能重复的，所以生成的文件名不会重名
        sessionid = request.session.session_key
        currentdir = os.path.dirname(__file__) # 获取脚本的目录路径,__file__表示当前这个python脚本
        filedir = currentdir + '/shell'
        if os.path.exists(filedir) == False: # 判断目录是否存在
            os.makedirs(filedir) # 可以创建多层目录
#        tmpfile = filedir + '/tmp_' + sessionid + '.sh' # 这里用sessionid会出现一些问题
        tmpfile = filedir + '/tmp.sh'
#        tmpfile = '/usr/local/workspace/neptune/djangosalt/shell/tmp_' + sessionid + '.sh'
        
        try:
            file_output = open(tmpfile, 'w+')
            line2 = "echo 'Hello!'\r\necho 'Thanks!'"
            line2 = line2.replace('\r\n', '\n')
            line = shellcontent
            line = line.replace('\r\n', '\n')
            file_output.writelines(line)
        except:
            print "执行失败！"
        finally:
            file_output.flush()
            file_output.close()
        
        cmd_str = 'sh ' + tmpfile
        tmp_shellresult = client.cmd('*', 'cmd.run', [cmd_str], ret='json')
#        tmp_shellresult = client.cmd('*', 'cmd.run', ['sh /usr/local/workspace/neptune/djangosalt/shell/tmp_492050db7e8f3de28b197949f16606d5.sh'], ret='json')
#        tmp_shellresult = client.cmd('*', 'cmd.run', ['sh /usr/local/workspace/neptune/djangosalt/shell/testshell.sh'], ret='json')
        print tmp_shellresult
        tmp_shell_yaml_str = yaml.dump(tmp_shellresult, default_flow_style=False)
        print tmp_shell_yaml_str
        
        # 执行完后删除临时脚本文件
#        if os.path.isfile(tmpfile) == True:
#            os.remove(tmpfile)
        
        
        
        
        
        
        
        
        shellcontent_list = shellcontent.split('\r\n')
        print shellcontent_list
        shell_str = ' && '.join([line for line in shellcontent_list if not line.startswith('#')])
        
#        shellresult = client.cmd('*', 'cmd.run', ['cd / && ls -l'], ret='json')
        shell_str_shellresult = client.cmd('*', 'cmd.run', [shell_str], ret='json')
        print shell_str_shellresult
        shell_str__yaml_str = yaml.dump(shell_str_shellresult, default_flow_style=False)
        print shell_str__yaml_str
        
        
        
        
        
        
        
        tmpfile = '/usr/local/workspace/neptune/djangosalt/shell/tmp.sh'
        tmpdir = os.path.dirname(tmpfile)
        print ("tmpdir: %s " % tmpdir)
        
#        if(os.path.exists(tmpfile) == False):
#            os.makedirs(tmpdir)
        tmp_file_output = open(tmpfile, 'w+')
        try:
            
            tmp_file_output.writelines(shellcontent)
            
#            shellcontent_list = shellcontent.split('\r\n')
#            print shellcontent_list
#            for line in shellcontent_list:
#                tmp_file_output.writelines(line+'\r\n')
        except:
            print "执行失败!"
        finally:
            tmp_file_output.close()
        
        tmp_shellresult = client.cmd('*', 'cmd.run', ['sh /usr/local/workspace/neptune/djangosalt/shell/testdashan.sh'], ret='json')
        print tmp_shellresult
        tmp_shell_yaml_str = yaml.dump(tmp_shellresult, default_flow_style=False)
        print tmp_shell_yaml_str
        
        
    else:
        return render_to_response('djangosalt/testpostping.html', ret, context_instance = RequestContext(request))
    
    
    # execution shell
#    shellresult = client.cmd('*', 'cmd.run', ['cd / && ls -l'], ret='json')
#    shellresult = client.cmd('*', 'cmd.run', ['sh /usr/local/workspace/neptune/djangosalt/shell/test.sh'], ret='json')
    shellresult = client.cmd('*', 'cmd.run', ['sh /usr/local/workspace/neptune/djangosalt/shell/test2.sh zhangsan lisi'], ret='json')
    print shellresult
    shell_yaml_str = yaml.dump(shellresult, default_flow_style=False)
    print shell_yaml_str
    
    
    # make compound execution calls with the cmd method
    testresult = client.cmd('*', ['cmd.run', 'test.ping', 'test.echo'], [['cd / && ls -l'], [], ['foo']])
    test_yaml_str = yaml.dump(testresult, default_flow_style=False)
    print test_yaml_str
    
    ####################测试#####################
    
    if 'target' in request.POST and request.POST['target'] and 'func' in request.POST and request.POST['func']:
        target = request.POST['target']
        func = request.POST['func']
        if 'argument' in request.POST and request.POST['argument']:
            argument = request.POST['argument']
            ret = client.cmd(target, func, [argument], ret='json')
        else:
            ret = client.cmd(target, func, ret='json')
        
    #client = get_salt_client()
    #ret = client.cmd(tgt, 'test.ping', ret='json')
    #ret = client.cmd(tgt, 'grains.items', ret='json') # true
    #ret = client.cmd(tgt, 'grains.item', ['os'], ret='json') # true
    #ret = client.cmd(tgt, 'state.highstate', ret='json') # true
    
    #ret = client.cmd(tgt, 'cmd.run', ['uname -a'], ret='json') # true
    #ret = client.cmd(tgt, 'cmd.run', ['cat /etc/issue'], ret='json') # true
    #ret = client.cmd(tgt, 'cmd.run', ['ls -l'], ret='json') # true
    
    # Import the Salt client library
    #import salt.client
    # create a local client object
    #client = salt.client.LocalClient()
    # make calls with the cmd method
    #ret = client.cmd(tgt, 'cmd.run', ['uname -a'], ret='yaml')
    
    
    
    print ret
    response = HttpResponse(mimetype="text/plain") # 这行代码很重要text/plain而不是text/html
    # 把json格式的数据转换成yaml格式的数据
    yaml_str = yaml.dump(ret, default_flow_style=False)
    print yaml_str
    response.write(yaml_str)
    return response
    
    #retdir = {"result": ret}
    #return render_to_response('djangosalt/basepage.html', retdir, context_instance = RequestContext(request))




'''
    salt脚本执行
'''
@wildcardtarget
def salt_shell(request):
    retdir = {}
    shell_result = {}
    client = get_salt_client()
    
    if request.POST:
        if 'target' in request.POST and request.POST['target'] and 'func' in request.POST and request.POST['func']:
            target = request.POST['target']
            retdir['target'] = target
            target = 'L@' + target
            func = request.POST['func']
            retdir['func'] = func
            argument = request.POST['argument']
            retdir['argument'] = argument
            arg = []
            if argument != None and argument != '':
                arg = [argument]
            
            shell_result = client.cmd(target, func, arg, expr_form = 'compound', ret = 'json')    
        yaml_str = yaml.dump(shell_result, default_flow_style=False)
        retdir['result'] = yaml_str
        return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
    else:
        return render_to_response('djangosalt/salt_shell.html', retdir, context_instance = RequestContext(request))

#'''
#    salt脚本执行_多线程
#'''
#@wildcardtarget
#def salt_shell(request):
#    retdir = {}
#    shell_result = {}
#    client = get_salt_client()
#    
#    if request.POST:
#        if 'target' in request.POST and request.POST['target'] and 'func' in request.POST and request.POST['func']:
#            target = request.POST['target']
#            retdir['target'] = target
#            minion_list = target.split(',')
#            func = request.POST['func']
#            retdir['func'] = func
#            argument = request.POST['argument']
#            retdir['argument'] = argument
#            arg = []
#            if argument != None and argument != '':
#                arg = [argument]
#            
#            lock = threading.Lock()
#            i = 1
#            for minion in minion_list:
#                thread_id = SaltRequest_Salt(client, shell_result, minion, func, arg, lock, "thread-" + str(i))
#                thread_id.start()
#                i = i+1
#                thread_id.join()
#            
#        yaml_str = yaml.dump(shell_result, default_flow_style=False)
#        retdir['result'] = yaml_str
#        return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
#    else:
#        return render_to_response('djangosalt/salt_shell.html', retdir, context_instance = RequestContext(request))




'''
    简单脚本执行
'''
@wildcardtarget
def simple_shell(request):
    retdir = {}
    client = get_salt_client()
    
    if request.POST:
        target = request.POST.get('target', None)
        retdir['target'] = target
        target = 'L@' + target
        
        shellcontent = request.POST.get('shellcontent', None)
        retdir['shellcontent'] = shellcontent
        
#        shellcontent_list = shellcontent.split('\r\n')
        shellcontent_list = shellcontent.split('\n')
        shell_str = ' && '.join([line for line in shellcontent_list if not line.startswith('#') and line != ''])
        
        func = 'cmd.run'
        arg = [shell_str]
        shell_result = client.cmd(target, func, arg, expr_form = 'compound', ret = 'json')    
        
        yaml_str = yaml.dump(shell_result, default_flow_style=False)
        print yaml_str
        retdir['result'] = yaml_str
        return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
    else:
        return render_to_response('djangosalt/simple_shell.html', retdir, context_instance = RequestContext(request))
    
    

#'''
#    简单脚本执行_多线程
#'''
#@wildcardtarget
#def simple_shell(request):
#    retdir = {}
#    client = get_salt_client()
#    
#    if request.POST:
#        target = request.POST.get('target', None)
#        retdir['target'] = target
#        minion_list = target.split(',')
#        
#        shellcontent = request.POST.get('shellcontent', None)
#        retdir['shellcontent'] = shellcontent
#        
##        shellcontent_list = shellcontent.split('\r\n')
#        shellcontent_list = shellcontent.split('\n')
#        print shellcontent_list
#        shell_str = ' && '.join([line for line in shellcontent_list if not line.startswith('#') and line != ''])
#        print shell_str
#        
#        
#        shell_result = {}
#        lock = threading.Lock()
#        i = 1
#        for minion in minion_list:
#            thread_id = SaltRequest(client, shell_result, minion, shell_str, lock, "thread-" + str(i))
#            thread_id.start()
#            i = i+1
#            thread_id.join()
#        
#        yaml_str = yaml.dump(shell_result, default_flow_style=False)
#        print yaml_str
#        retdir['result'] = yaml_str
#        return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
#    else:
#        return render_to_response('djangosalt/simple_shell.html', retdir, context_instance = RequestContext(request))
#    
    


'''
    复杂脚本执行
'''
@wildcardtarget
def compound_shell(request):
    retdir = {}
    shell_result = {}
    client = get_salt_client()
    
    if request.POST:
        target = request.POST.get('target', None)
        retdir['target'] = target
        minion_list = target.split(',')
        shellcontent = request.POST.get('shellcontent', None)
        retdir['shellcontent'] = shellcontent
        
        # 用sessionid作为名称生成临时文件，因为sessionid是不可能重复的，所以生成的文件名不会重名
        sessionid = request.session.session_key
    
        # 指定filedir路径，为了把生成的shell脚本传送到minion上面
        filedir = '/srv/salt/webserver/sites.d/'
        filename = 'tmp_' + sessionid + '.sh'
        tmpfile = filedir + filename
        try:
            file_output = open(tmpfile, 'w+')
            line = shellcontent.encode('UTF-8')
            line = line.replace('\r\n', '\n')
            file_output.writelines(line)
        except:
            print "执行失败！"
        finally:
            file_output.flush()
            file_output.close()

        
        minion_list_syndic = []
        try:
            for saltid in minion_list:
                server = Server.objects.get(saltid=saltid)
                if server.agent_flag == 1:
                    if server.agent_server.saltid not in minion_list_syndic:
                        if server.agent_server.saltid not in minion_list_syndic:
                            minion_list_syndic.append(server.agent_server.saltid)
        except Exception, e:
            print e
            
        # 把文件传送到所有的跳板机上
        if minion_list_syndic:
            target_syndic = 'L@' + ','.join(minion_list_syndic)
            func = 'cp.get_dir'
            arg = ['salt://webserver/sites.d/', '/srv/salt/webserver']
            shell_ret = client.cmd(target_syndic, func, arg, expr_form = 'compound', ret = 'json')
            shell_result.update(shell_ret)
                
                
        # 把文件传送到所有的minion上面(包括跳板机下面的minion)
        target = 'L@' + target
        func = 'cp.get_dir'
        arg = ['salt://webserver/sites.d/', '/var/www']
        shell_ret = client.cmd(target, func, arg, expr_form = 'compound', ret = 'json')
        shell_result.update(shell_ret)        
            
    
        # 指定执行的shell脚本的目录，注意这个目录跟生成shell脚本的目录不一致
        execute_filedir = '/var/www/sites.d/'
        cmd_str = 'sh ' + execute_filedir + filename
        func = 'cmd.run'
        arg = [cmd_str]
        shell_ret = client.cmd(target, func, arg, expr_form = 'compound', ret = 'json')
        shell_result.update(shell_ret)
        
         
        yaml_str = yaml.dump(shell_ret, default_flow_style=False)
        retdir['result'] = yaml_str
        
        # 执行完后删除临时脚本文件
        #if os.path.isfile(tmpfile) == True:
        #    os.remove(tmpfile)
        
        return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
    else:
        return render_to_response('djangosalt/compound_shell.html', retdir, context_instance = RequestContext(request))

#
#'''
#    复杂脚本执行_多线程
#'''
#@wildcardtarget
#def compound_shell(request):
#    retdir = {}
#    client = get_salt_client()
#    
#    if request.POST:
#        target = request.POST.get('target', None)
#        retdir['target'] = target
#        minion_list = target.split(',')
#        shellcontent = request.POST.get('shellcontent', None)
#        retdir['shellcontent'] = shellcontent
#        
#        # 用sessionid作为名称生成临时文件，因为sessionid是不可能重复的，所以生成的文件名不会重名
#        sessionid = request.session.session_key
#    
#        # 指定filedir路径，为了把生成的shell脚本传送到minion上面
#        filedir = '/srv/salt/webserver/sites.d/'
#        filename = 'tmp_' + sessionid + '.sh'
#        tmpfile = filedir + filename
#        try:
#            file_output = open(tmpfile, 'w+')
#            line = shellcontent
#            line = line.replace('\r\n', '\n')
#            file_output.writelines(line)
#        except:
#            print "执行失败！"
#        finally:
#            file_output.flush()
#            file_output.close()
#        
#            
#
#        # 第一次执行同步操作，把文件由主master传送到各机房的跳板机上面(如果没有跳板机，则执行一次同步就行)
##        first__file_sync = client.cmd(target, 'cp.get_dir', ['salt://webserver/sites.d', '/srv/salt/webserver'], ret = 'json')
#        # 第二次执行同步操作，在所有的minion上面(包括跳板机下面的minion)按照配置文件执行相应的操作
##        second_file_sync = client.cmd(target, 'cp.get_dir', ['salt://webserver/sites.d', '/var/www'], ret = 'json')
#        
#        minion_list_syndic = []
#        try:
#            for saltid in minion_list:
#                server = Server.objects.get(saltid=saltid)
#                if server.agent_flag == 1:
#                    if server.agent_server.saltid not in minion_list_syndic:
#                        minion_list_syndic.append(server.agent_server.saltid)
#        except:
#            return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
#                
#        shell_result = {}
#        func = 'cp.get_dir'
#        arg = ['salt://webserver/sites.d', '/srv/salt/webserver']
#        lock = threading.Lock()
#        i = 1
##        minion_list_syndic = ['monitor_002']
#        for minion in minion_list_syndic:
#            thread_id = SaltRequest_Salt(client, shell_result, minion, func, arg, lock, "thread-" + str(i))
#            thread_id.start()
#            i = i+1
#            thread_id.join()
#            
#            
#        shell_result = {}
#        func = 'cp.get_dir'
#        arg = ['salt://webserver/sites.d', '/var/www']
#        lock = threading.Lock()
#        i = 1
#        for minion in minion_list:
#            thread_id = SaltRequest_Salt(client, shell_result, minion, func, arg, lock, "thread-" + str(i))
#            thread_id.start()
#            i = i+1
#            thread_id.join()
#        
#    
#        # 指定执行的shell脚本的目录，注意这个目录跟生成shell脚本的目录不一致
#        execute_filedir = '/var/www/sites.d/'
#        cmd_str = 'sh ' + execute_filedir + filename
#        
#        shell_result = {}
#        lock = threading.Lock()
#        i = 1
#        for minion in minion_list:
#            thread_id = SaltRequest(client, shell_result, minion, cmd_str, lock, "thread-" + str(i))
#            thread_id.start()
#            i = i+1
#            thread_id.join()
#        
#        yaml_str = yaml.dump(shell_result, default_flow_style=False)
#        retdir['result'] = yaml_str
#        
#        # 执行完后删除临时脚本文件
#        #if os.path.isfile(tmpfile) == True:
#        #    os.remove(tmpfile)
#        
#        return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
#    else:
#        return render_to_response('djangosalt/compound_shell.html', retdir, context_instance = RequestContext(request))





'''
    配置文件管理
'''
@wildcardtarget
def file_manager(request):
    retdir = {}
    shell_result = {}
    client = get_salt_client()
    
    if request.POST:
        target = request.POST.get('target', None)
        retdir['target'] = target
        minion_list = target.split(',')
        pathname = request.POST.get('pathname', None)
        retdir['pathname'] = pathname
        filecontent = request.POST.get('filecontent', None)
        retdir['filecontent'] = filecontent
        
        # 用sessionid作为名称生成临时文件，因为sessionid是不可能重复的，所以生成的文件名不会重名
        sessionid = request.session.session_key
        
        filedir = '/srv/salt/webserver/sites.d/'
        file_name = pathname.split('/')[-1]
    
#        # 指定filedir路径，为了把生成的配置文件传送到minion上面
#        filedir = '/srv/salt/webserver/sites.d/'
#        if(os.path.exists(filedir) == False):
#            os.makedirs(filedir)
#        # 修改权限777
#        os.chmod(filedir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        
        filename = 'tmp_' + sessionid + "_" + file_name
        tmpfile = filedir + filename
        try:
            file_output = open(tmpfile, 'w+')
            line = filecontent.encode("UTF-8")
            line = line.replace('\r\n', '\n')
            file_output.writelines(line)
        except:
            print "执行失败！"
        finally:
            file_output.flush()
            file_output.close()
        
        
        minion_list_syndic = []
        try:
            for saltid in minion_list:
                server = Server.objects.get(saltid=saltid)
                if server.agent_flag == 1:
                    if server.agent_server.saltid not in minion_list_syndic:
                        if server.agent_server.saltid not in minion_list_syndic:
                            minion_list_syndic.append(server.agent_server.saltid)
        except Exception, e:
            print e
                
        # 把文件传送到所有的跳板机上
        if minion_list_syndic:
            target_syndic = 'L@' + ','.join(minion_list_syndic)
            func = 'cp.get_file'
            arg = ['salt://webserver/sites.d/' + filename, '/srv/salt/webserver/sites.d/' + filename]
            shell_ret = client.cmd(target_syndic, func, arg, expr_form = 'compound', ret = 'json')
            shell_result.update(shell_ret)
            
        
        # 把文件传送到所有的minion上面(包括跳板机下面的minion)
        target = 'L@' + target
        func = 'cp.get_file'
        arg = ['salt://webserver/sites.d/' + filename, pathname]
        shell_ret = client.cmd(target, func, arg, expr_form = 'compound', ret = 'json')
        shell_result.update(shell_ret)
        
    
        yaml_str = yaml.dump(shell_ret, default_flow_style=False)
        retdir['result'] = yaml_str
        
        # 执行完后删除临时脚本文件
        #if os.path.isfile(tmpfile) == True:
        #    os.remove(tmpfile)
        
        return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
    else:
        return render_to_response('djangosalt/file_manager.html', retdir, context_instance = RequestContext(request))


#
#
#'''
#    配置文件管理_多线程
#'''
#@wildcardtarget
#def file_manager(request):
#    retdir = {}
#    client = get_salt_client()
#    
#    if request.POST:
#        target = request.POST.get('target', None)
#        retdir['target'] = target
#        minion_list = target.split(',')
#        pathname = request.POST.get('pathname', None)
#        retdir['pathname'] = pathname
#        filecontent = request.POST.get('filecontent', None)
#        retdir['filecontent'] = filecontent
#        
#        # 用sessionid作为名称生成临时文件，因为sessionid是不可能重复的，所以生成的文件名不会重名
#        sessionid = request.session.session_key
#        
#        filedir = '/srv/salt/webserver/sites.d/'
#        file_name = pathname.split('/')[-1]
#    
##        # 指定filedir路径，为了把生成的配置文件传送到minion上面
##        filedir = '/srv/salt/webserver/sites.d/'
##        if(os.path.exists(filedir) == False):
##            os.makedirs(filedir)
##        # 修改权限777
##        os.chmod(filedir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
#        
#        filename = 'tmp_' + sessionid + "_" + file_name
#        tmpfile = filedir + filename
#        try:
#            file_output = open(tmpfile, 'w+')
#            line = filecontent.encode("UTF-8")
#            line = line.replace('\r\n', '\n')
#            file_output.writelines(line)
#        except:
#            print "执行失败！"
#        finally:
#            file_output.flush()
#            file_output.close()
#        
#        
#        # 把文件传送到所有的跳板机上
#        minion_list_syndic = []
#        try:
#            for saltid in minion_list:
#                server = Server.objects.get(saltid=saltid)
#                if server.agent_flag == 1:
#                    if server.agent_server.saltid not in minion_list_syndic:
#                        minion_list_syndic.append(server.agent_server.saltid)
#        except:
#            return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
#                
#        shell_result = {}
#        func = 'cp.get_file'
#        arg = ['salt://webserver/sites.d/' + filename, '/srv/salt/webserver/sites.d/' + filename, 'makedirs=True']
#        lock = threading.Lock()
#        i = 1
#        for minion in minion_list_syndic:
#            thread_id = SaltRequest_Salt(client, shell_result, minion, func, arg, lock, "thread-" + str(i))
#            thread_id.start()
#            i = i+1
#            thread_id.join()
#            
#        
#        # 把文件传送到所有的minion上面(包括跳板机下面的minion)
#        shell_result = {}
#        func = 'cp.get_file'
#        arg = ['salt://webserver/sites.d/' + filename, pathname, 'makedirs=True']
#        lock = threading.Lock()
#        i = 1
#        for minion in minion_list:
#            thread_id = SaltRequest_Salt(client, shell_result, minion, func, arg, lock, "thread-" + str(i))
#            thread_id.start()
#            i = i+1
#            thread_id.join()
#        
#    
#        yaml_str = yaml.dump(shell_result, default_flow_style=False)
#        retdir['result'] = yaml_str
#        
#        # 执行完后删除临时脚本文件
#        #if os.path.isfile(tmpfile) == True:
#        #    os.remove(tmpfile)
#        
#        return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
#    else:
#        return render_to_response('djangosalt/file_manager.html', retdir, context_instance = RequestContext(request))
#



'''
    软件包管理
'''
@wildcardtarget
def package_manager(request):
    retdir = {}
    shell_result = {}
    client = get_salt_client()
    
    if request.POST:
        target = request.POST.get('target', None)
        retdir['target'] = target
        minion_list = target.split(',')
        down_type = request.POST.get('down_type', None)
        retdir['down_type'] = down_type
        down_path = request.POST.get('down_path', None)
        retdir['down_path'] = down_path
        pathname = request.POST.get('pathname', None)
        retdir['pathname'] = pathname
        
        # 用sessionid作为名称生成临时文件，因为sessionid是不可能重复的，所以生成的文件名不会重名
#        sessionid = request.session.session_key
        # /var/www/myfile/httpd-2.2.17.tar.gz
#        file_dir = os.path.dirname(pathname) # /var/www/myfile
#        file_name = pathname.split('/')[-1] # httpd-2.2.17.tar.gz
        
        
        # 指定filedir路径，为了把生成的软件包传送到minion上面
        filedir = '/srv/salt/webserver/sites.d/'
#        if(os.path.exists(filedir) == False):
#            os.makedirs(filedir)
#        # 修改权限777
#        os.chmod(filedir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        
        
        url = down_path
        i = url.rfind('/')
        filename = url[i+1:]
        try:
            # wget -O /home/dashan.yin/tomcat6.0.20-zhijian.tar.gz http://10.2.161.14/src/tomcat6.0.20-zhijian.tar.gz
            cmdstr = 'wget -O ' + filedir + filename + ' ' + url
            result_file = os.popen(cmdstr)
            result = result_file.readlines()
            result_file.close()
            print result
        except:
            return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
        
        
        minion_list_syndic = []
        try:
            for saltid in minion_list:
                server = Server.objects.get(saltid=saltid)
                if server.agent_flag == 1:
                    if server.agent_server.saltid not in minion_list_syndic:
                        if server.agent_server.saltid not in minion_list_syndic:
                            minion_list_syndic.append(server.agent_server.saltid)
        except Exception, e:
            print e
            
        # 把文件传送到所有的跳板机上
        if minion_list_syndic:
            target_syndic = 'L@' + ','.join(minion_list_syndic)
            func = 'cp.get_file'
            arg = ['salt://webserver/sites.d/' + filename, '/srv/salt/webserver/sites.d/' + filename]
            shell_ret = client.cmd(target_syndic, func, arg, expr_form = 'compound', ret = 'json')
            shell_result.update(shell_ret)

        
        # 把文件传送到所有的minion上面(包括跳板机下面的minion)
        target = 'L@' + target
        func = 'cp.get_file'
        arg = ['salt://webserver/sites.d/' + filename, pathname + filename]
        shell_ret = client.cmd(target, func, arg, expr_form = 'compound', ret = 'json')
        shell_result.update(shell_ret)
    
        yaml_str = yaml.dump(shell_ret, default_flow_style=False)
        retdir['result'] = yaml_str
        
        # 执行完后删除临时脚本文件
        #if os.path.isfile(tmpfile) == True:
        #    os.remove(tmpfile)
        
        return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
    else:
        return render_to_response('djangosalt/package_manager.html', retdir, context_instance = RequestContext(request))


#'''
#    软件包管理_多线程
#'''
#@wildcardtarget
#def package_manager(request):
#    retdir = {}
#    client = get_salt_client()
#    
#    if request.POST:
#        target = request.POST.get('target', None)
#        retdir['target'] = target
#        minion_list = target.split(',')
#        down_type = request.POST.get('down_type', None)
#        retdir['down_type'] = down_type
#        down_path = request.POST.get('down_path', None)
#        retdir['down_path'] = down_path
#        pathname = request.POST.get('pathname', None)
#        retdir['pathname'] = pathname
#        
#        # 用sessionid作为名称生成临时文件，因为sessionid是不可能重复的，所以生成的文件名不会重名
##        sessionid = request.session.session_key
#        # /var/www/myfile/httpd-2.2.17.tar.gz
##        file_dir = os.path.dirname(pathname) # /var/www/myfile
##        file_name = pathname.split('/')[-1] # httpd-2.2.17.tar.gz
#        
#        
#        # 指定filedir路径，为了把生成的软件包传送到minion上面
#        filedir = '/srv/salt/webserver/sites.d/'
##        if(os.path.exists(filedir) == False):
##            os.makedirs(filedir)
##        # 修改权限777
##        os.chmod(filedir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
#        
#        
#        url = down_path
#        i = url.rfind('/')
#        filename = url[i+1:]
#        try:
#            # wget -O /home/dashan.yin/tomcat6.0.20-zhijian.tar.gz http://10.2.161.14/src/tomcat6.0.20-zhijian.tar.gz
#            cmdstr = 'wget -O ' + filedir + filename + ' ' + url
#            result_file = os.popen(cmdstr)
#            result = result_file.readlines()
#            result_file.close()
#            print result
#        except:
#            return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
#        
#        
#        # 把文件传送到所有的跳板机上
#        minion_list_syndic = []
#        try:
#            for saltid in minion_list:
#                server = Server.objects.get(saltid=saltid)
#                if server.agent_flag == 1:
#                    if server.agent_server.saltid not in minion_list_syndic:
#                        minion_list_syndic.append(server.agent_server.saltid)
#        except:
#            return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
#                
#        shell_result = {}
#        func = 'cp.get_file'
#        arg = ['salt://webserver/sites.d/' + filename, '/srv/salt/webserver/sites.d/' + filename, 'makedirs=True']
#        lock = threading.Lock()
#        i = 1
#        for minion in minion_list_syndic:
#            thread_id = SaltRequest_Salt(client, shell_result, minion, func, arg, lock, "thread-" + str(i))
#            thread_id.start()
#            i = i+1
#            thread_id.join()
#            
#        
#        # 把文件传送到所有的minion上面(包括跳板机下面的minion)
#        shell_result = {}
#        func = 'cp.get_file'
#        arg = ['salt://webserver/sites.d/' + filename, pathname + filename, 'makedirs=True']
#        lock = threading.Lock()
#        i = 1
#        for minion in minion_list:
#            thread_id = SaltRequest_Salt(client, shell_result, minion, func, arg, lock, "thread-" + str(i))
#            thread_id.start()
#            i = i+1
#            thread_id.join()
#        
#    
#        yaml_str = yaml.dump(shell_result, default_flow_style=False)
#        retdir['result'] = yaml_str
#        
#        # 执行完后删除临时脚本文件
#        #if os.path.isfile(tmpfile) == True:
#        #    os.remove(tmpfile)
#        
#        return HttpResponse(simplejson.dumps(retdir), mimetype='application/json')
#    else:
#        return render_to_response('djangosalt/package_manager.html', retdir, context_instance = RequestContext(request))



    
@login_required
def searchback(request):
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
    return render_to_response('djangosalt/searchback.html', retdir, context_instance=RequestContext(request))





