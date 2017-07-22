# -*- coding: utf-8 -*-
#!/usr/bin Python
from __future__ import print_function
from collections import OrderedDict
import time
import urllib
import urllib2
import socket

url = 'http://api'

service_name = ''#服务器别称
service_ip = ''#服务器ip
cpu_rate = ''#cpu使用率
memory_rate = ''#内存使用率
cpu_num = ''#cpu使用量
memory_num = ''#内存使用量
datetime = ''#时间






def getname():
    myname = socket.getfqdn(socket.gethostname())
    return  myname
def getip():
    myname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    myaddr = socket.gethostbyname(myname)
    return  myaddr
def cpuinfo():
    lines = open('/proc/stat').readlines()
    for line in lines:
        ln = line.split()
        if ln[0].startswith('cpu'):
            return ln;
    return []
W = cpuinfo()
one_cpuTotal = long(W[1]) + long(W[2]) + long(W[3]) + long(W[4]) + long(W[5]) + long(W[6]) + long(W[7])
one_cpuused = long(W[1]) + long(W[2]) + long(W[3])
def CPUinfo():
    ''''' Return the information in /proc/CPUinfo
    as a dictionary in the following format:
    CPU_info['proc0']={...}
    CPU_info['proc1']={...}
    '''
    CPUinfo = OrderedDict()
    procinfo = OrderedDict()
    nprocs = 0
    f = open('/proc/cpuinfo')
    for line in f.readlines():
        if not line.strip():
            # end of one processor
            CPUinfo['proc%s' % nprocs] = procinfo
            nprocs = nprocs + 1
            # Reset
            procinfo = OrderedDict()
        else:
            if len(line.split(':')) == 2:
                procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
            else:
                procinfo[line.split(':')[0].strip()] = ''

    return CPUinfo
def meminfo():
    ''''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo = OrderedDict()
    f = open('/proc/meminfo')
    for line in f.readlines():
        meminfo[line.split(':')[0]] = line.split(':')[1].strip().replace(' kB','')
    return meminfo
def nowtime():
    time.localtime(time.time())
    timeres = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime(time.time()))
    return timeres



def post(service_name, service_ip, cpu_rate, memory_rate,cpu_num,memory_num,datetime):
    try:
        postdata = dict(service_name=service_name, service_ip=service_ip, cpu_rate=cpu_rate, memory_rate=memory_rate,cpu_num=cpu_num,memory_num=memory_num,datetime=datetime)
        postdata = urllib.urlencode(postdata)
        request = urllib2.Request(url, postdata)
        response = urllib2.urlopen(request)
        print ('发送状态:'+ str(response.read()))
        return str(response.read())
    except Exception as e:
        print(e)




if __name__ == '__main__':
    try:
        while True:
            time.sleep(5)
            mi = meminfo()
            W = cpuinfo()
            two_cpuTotal = long(W[1]) + long(W[2]) + long(W[3]) + long(W[4]) + long(W[5]) + long(W[6]) + long(W[7])
            two_cpuused = long(W[1]) + long(W[2]) + long(W[3])
            cpuused = float((two_cpuused - one_cpuused) / (two_cpuTotal - one_cpuTotal))

            service_name = getname()
            service_ip = getip()
            cpu_rate = cpuused *100#cpu使用率
            memory_rate = (long(mi['MemTotal']) - long(mi['MemFree'])) / long(mi['MemTotal']) * 100  #内存使用率
            cpu_num = two_cpuused - one_cpuused #cpu使用量
            memory_num = long(mi['MemTotal']) - long(mi['MemFree']) #使用量
            datetime = nowtime()

            '''
            print("名称: ", service_name)
            print("ip: ", service_ip)
            print("cpu使用率: ",cpu_rate)
            print("内存使用率: ", memory_rate)
            print("cpu使用量: ", cpu_rate)
            print("内存使用量: ", memory_rate)
            print("获取时间: ", datetime)
          '''
            post(service_name, service_ip, cpu_rate, memory_rate, cpu_num, memory_num, datetime)
            time.sleep(450)  #15分钟采样一次

    except KeyboardInterrupt as e:
        print("\ncpumonit exited")




