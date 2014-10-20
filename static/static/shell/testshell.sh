#!/bin/sh

yesterday=`date -d last-day +%m-%d`
echo $yesterday
#cd /data1/360log/restapi/qingdao/119.167.231.156/
cd /srv/salt/lse/ 
size2=`ls -l Django-1.4.tar.gz | awk '{print $5}'`
echo $size2
#while [ true ];do
#        size1=$size2
#        sleep 5
#        size2=`ls -l Django-1.4.tar.gz | awk '{print $5}'`
#    if( test $size1 -eq $size2 );then  ssh 192.168.3.100 'cd /home/dashan.yin;./downlog.sh'
#	fi
#	exit 0
#done
