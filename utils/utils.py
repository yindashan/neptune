#!usr/bin/env python
#coding: utf-8
'''
Created on Jun 27, 2012

@author: dashan.yin
'''
from django.core.mail import EmailMultiAlternatives
import threading

import time
import datetime
import re

'''
* 匹配IP地址
* @param ip
* @return MatchObject ip地址正确;
*         None ip地址错误;
'''
def isIP(ip):
    return re.search(r'^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$', ip)

'''
* 匹配电话号码，
* 如：(010)-12345678， (010)12345678，(010)12345678， 010-12345678，010 12345678， 01012345678 
*    (0913)-1234567， (0913)1234567，(0913)1234567， 0913-1234567，0913 1234567， 09131234567
*    (86-10)67860053
* @param tel
* @return MatchObject tel正确;
*         None tel错误;
'''
def isTel(tel):
    return re.search(r'^\(0\d{2}\)[- ]?\d{8}|0\d{2}[- ]?\d{8}|\(0\d{3}\)[- ]?\d{7}|0\d{3}[- ]?\d{7}|\(86-\d{2}\)[- ]?\d{8}$', tel)

'''
* 匹配手机号码
* @param mobile
* @return MatchObject mobile正确;
*         None mobile错误; 
'''
def isMobile(mobile):
    return re.search(r'^1[358]\d{9}$', mobile)      

'''
* 匹配端口号0~65535
* @param port
* @return MatchObject port正确;
*         None port错误; 
'''   
def isPort(port):
    return re.search(r'^6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0$', port)

'''
* 匹配电流，单位：“ma”，范围：0~13000
* @param amp
* @return MatchObject amp正确;
*         None amp错误;
* 
'''
def isAmp(amp):
    return re.search(r'^13000|1[0-2]\d{3}|[1-9]\d{0,3}|0$', amp)

'''
* os位数，只有32、64两种
* @param osbyte
* @return MatchObject osbyte正确;
*         None osbyte错误; 
'''
def isOSByte(osbyte):
    return re.search(r'^32|64$', osbyte)

'''
* 日期格式 ：“yyyy/MM/dd”， 范围：2000/01/01~2999/12/31 或  2000/1/1~2999/12/31
* @param date
* @return MatchObject date正确;
*         None date错误; 
'''
def isDate(date):
    return re.search(r'^2\d{3}[/-]([1-9]|0[1-9]|1[0-2])[/-]([1-9]|0[1-9]|[1-2]\d|3[0-1])$', date)


def isInt(num):
    return re.search(r'^[1-9]\d*|0', num)
'''
* 机房状态： 0:'备用', 1:'使用', 2:'报废'
* @param status
* @return MatchObject status正确;
*         None status错误; 
'''
def isNOCStatus(status):
    return re.search(r'^[0-2]{1}$', status)

'''
* 机架状态： 0:'备用', 1:'使用', 2:'报废'
* @param status
* @return MatchObject status正确;
*         None status错误; 
''' 
def isRackStatus(status):
    return re.search(r'^[0-2]{1}$', status)

'''
* 机架总空间，只有42、48两种
* @param space
* @return MatchObject space正确;
*         None space错误; 
'''
def isRackSpace(space):
    return re.search(r'^42|48$', space)

'''
* 设备状态： 0:'备用', 1:'使用', 2:'报废', 3:'报修', 4:'修理', 5:'闲置'
* @param status
* @return MatchObject status正确;
*         None status错误; 
'''
def isEquipmentStatus(status):
    return re.search(r'^[0-5]{1}$', status)

'''
* IP地址类型： 0:'内网', 1:'外网'
* @param type
* @return MatchObject type正确;
*         None type错误; 
'''
def isIPType(iptype):
    return re.search(r'^[0,1]{1}$', iptype)

'''
* IP地址状态：0:'备用', 1:'使用'
* @param status
* @return MatchObject status正确;
*         None status错误; 
'''
def isIPStatus(status):
    return re.search(r'^[0,1]{1}$', status)

'''
* datestr转换成secs
* 将时间字符串转化为秒("2012-07-20 00:00:00"->1342713600.0)
* @param datestr;
* @return secs;
*
'''
def datestr2secs(datestr):
    tmlist = []
    array = datestr.split(' ')
    array1 = array[0].split('-')
    array2 = array[1].split(':')
    for v in array1:
        tmlist.append(int(v))
    for v in array2:
        tmlist.append(int(v))
    tmlist.append(0)
    tmlist.append(0)
    tmlist.append(0)
    if len(tmlist) != 9:
        return 0
    return int(time.mktime(tmlist))


'''
* secs转换成datestr
* 将秒转化为时间字符串(1342713600.0->"2012-07-20 00:00:00")
* @param secs;
* @return datestr;
*
'''
def secs2datestr(secs):
    if int(secs) < 0:
        return ""
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(secs)))


'''
* datestr转换成datestr
* 将时间字符串转化为时间字符串("2012-07-20"->"2012-07-20 00:00:00")
* @param datestr;
* @return datestr;
*
'''
def datestr2datestr(datestr):
    # 字符串->time
    datestr = time.strptime(datestr, "%Y-%m-%d")
    # time->字符串
    datestr = time.strftime("%Y-%m-%d %H:%M:%S", datestr)
    # 字符串->time
#    datestr = time.strptime(datestr, "%Y-%m-%d %X")
    # time->datetime
#    datestr=datetime.datetime(datestr[0],datestr[1],datestr[2],datestr[3],datestr[4],datestr[5])
    return datestr

#把datetime转成字符串
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")

#把时间戳转成字符串形式
def timestamp_toString(stamp):
    return time.strftime("%Y-%m-%d-%H", time.localtime(stamp))

#把datetime类型转外时间戳形式
def datetime_toTimestamp(dateTim):
    return time.mktime(dateTim.timetuple())

'''
* 获得状态
* @param status;
* @return status;
*
'''
def get_status(status):
    if int(status) == 0:
        return u'备用'
    elif int(status) == 1:
        return u'使用'
    elif int(status) == 2:
        return u'报废'
    elif int(status) == 3:
        return u'报修'
    elif int(status) == 4:
        return u'修理'
    elif int(status) == 5:
        return u'闲置'
    elif int(status) == 6:
        return u'闲置'

'''
* 多线程发送邮件
*
'''
class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)
    def run(self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.body, self.html)
            msg.send(self.fail_silently)
def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()



