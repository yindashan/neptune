#!usr/bin/env python
#coding: utf-8
from fabric.api import local, env, run, execute
from fabric.api import *
from fabric.contrib import django

django.project('neptune')
from server.models import Server

#env.hosts = ['127.0.0.1']
env.user = 'root'
#env.password = 'root_password'


def print_instances():
    for instance in Server.objects.all():
        print(instance)

@hosts('127.0.0.1')
def print_production_instances():
    with cd('/usr/local/workspace/neptune'):
        run('fab print_instances')


'''
    get salt-minion status
'''
def getstatus():
    print 'get salt-minion status'
    sudo('service salt-minion status')
    
    
'''
    start salt-minion
'''
def start():
    print 'start salt-minion'
    sudo('service salt-minion start')


'''
    stop salt-minion
'''
def stop():
    print 'stop salt-minion'
    sudo('service salt-minion stop')


'''
    restart salt-minion
'''
def restart():
    print 'restart salt-minion'
    sudo('service salt-minion restart')


'''
    获取操作系统类型，当前只考虚两种系统：CentOS和Ubuntu
'''
def getos():
    print 'get os'
    sudo('whoami')
    sudo('cat /etc/issue')


'''
    setup salt-minion in Ubuntu
'''
def setup_ubuntu(master="10.2.161.15", minionid="minion_10.2.161.15"):
    sudo('echo deb http://ppa.launchpad.net/saltstack/salt/ubuntu `lsb_release -sc` main | sudo tee /etc/apt/sources.list.d/saltstack.list')
    sudo("sed -i 's/us.archive.ubuntu.com/mirrors.163.com/g' /etc/apt/sources.list") 
    sudo('apt-get update')
    sudo('apt-get install salt-minion')
    print 'edit salt minion config'
    sudo("sed -i 's/#master: salt/master: %s/g' /etc/salt/minion"%master)
    sudo("sed -i 's/#id:/id: %s/g' /etc/salt/minion"%minionid)
    print 'restart salt-minion'
    sudo('service salt-minion restart')


'''
    setup salt-minion in CentOS
'''
def setup_centos(master="10.2.161.15", minionid="minion_10.2.161.15"):
    #sudo('echo deb http://ppa.launchpad.net/saltstack/salt/ubuntu `lsb_release -sc` main | sudo tee /etc/apt/sources.list.d/saltstack.list')
    #sudo("sed -i 's/us.archive.ubuntu.com/mirrors.163.com/g' /etc/apt/sources.list") 
    #sudo('yum update')
    sudo('yum -y install salt-minion')
    print 'edit salt minion config'
    sudo("sed -i 's/#master: salt/master: %s/g' /etc/salt/minion"%master)
    sudo("sed -i 's/#id:/id: %s/g' /etc/salt/minion"%minionid)
    print 'restart salt-minion'
    sudo('service salt-minion restart')


def hello(name="world", age="20"):
    print ("Hello %s!" %name)
    print ("I'M %s!" %age)
    print 'restart salt-minion'
    sudo('service salt-minion status')

    
    #sudo("sed -i 's/#master: salt/master: 192.168.56.11/g' /etc/salt/minion")
    #sn = 'minion1001'
    #sudo("sed -i 's/#id:/id: %s/g' /etc/salt/minion"%sn)
    #print 'restart salt-minion'
    #sudo('service salt-minion restart')

def test():
    local("ls -l")

def remote():
    #env.hosts = ['127.0.0.1']
    execute(host_type)

def host_type():
    run('uname -a')

def init_salt():
    sudo('echo deb http://ppa.launchpad.net/saltstack/salt/ubuntu `lsb_release -sc` main | sudo tee /etc/apt/sources.list.d/saltstack.list')

    sudo("sed -i 's/us.archive.ubuntu.com/mirrors.163.com/g' /etc/apt/sources.list") 

    #hostname = HOST_DICT.get(env.host_string)
    #if not hostname:
    #    return
    hostname = '127.0.0.1'

    sudo('echo "%s" > /etc/hostname'%hostname)
    sudo('hostname %s'%hostname)

    sudo('apt-get update')

    sudo('apt-get install salt-minion')
    print 'edit salt minion config'

    sudo("sed -i 's/#master: salt/master: 192.168.56.11/g' /etc/salt/minion")
    get('/etc/serial','/tmp/serial')
    sn = open('/tmp/serial').read().strip()
    sudo("sed -i 's/#id:/id: %s/g' /etc/salt/minion"%sn)
    print 'restart salt-minion'
    sudo('service salt-minion restart')
    




