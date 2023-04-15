from genericpath import isfile
import re
import subprocess
import os
import pandas as pd


def conversation_stat(file_path):
    
    option = ['tshark.exe','-n','-r',file_path,'-q','-z','conv,ip']

    if os.path.isfile(file_path):
        p = subprocess.Popen(option,stdout=subprocess.PIPE,stderr = subprocess.PIPE)
        stdout,stderr = p.communicate()
        assert not stderr,'tshark error'

        for line in stdout.splitlines():
            a = line.decode().split()
            regular = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
            if regular.match(a[0]):
                src = a[2]
                dst = a[0]
                size = a[4]+a[5]
                print(f'{src} -> {dst}, {size}')
                option = ['tshark.exe','-n','-r',file_path,'-Y',f'ip.addr=={src} && ip.addr=={dst}','-T', 'fields', 
                        '-e', 'frame.time_relative',
                        '-e', 'tcp.stream', 
                        '-e', 'tcp.srcport', 
                        '-e', 'tcp.dstport',    
                        '-e', 'udp.stream', 
                        '-e', 'udp.srcport', 
                        '-e', 'udp.dstport',
                        '-e', 'ip.src', 
                        '-e', 'ip.dst',   
                        '-e', 'ip.proto', 
                        '-e', 'tcp.len', 
                        '-e', 'udp.length', 
                        '-E', 'header=y', '-E' ,'separator=,']
                
                p = subprocess.Popen(option,stdout=subprocess.PIPE,stderr = subprocess.PIPE)
                stdout,stderr = p.communicate()

                assert not stderr,'tshark error'

                data = [i.decode().split(',') for i in stdout.splitlines()]
                data = pd.DataFrame(data[1:],columns=data[0])
                data2 = pd.DataFrame(columns=['time','streamid','protocol','src_address','src_port','dst_address','dst_port','length'] )
                data2['time'] = data['frame.time_relative']
                data2['streamid'] = data['tcp.stream']+data['udp.stream']
                data2['protocol'] = data['ip.proto']
                data2['src_address'] = data['ip.src']
                data2['src_port'] = data['tcp.srcport']+data['udp.srcport']
                data2['dst_address'] = data['ip.dst']
                data2['dst_port'] = data['tcp.dstport']+data['udp.dstport']
                data2['length'] = data['tcp.len']+data['udp.length']
                path = os.path.splitext(file_path)          
                data2.to_csv(path[0]+'.csv')
                #data.to_csv('D:\\result_bak\\2021-04-08_1\\42_BV1fp4y1b7Dc\BV1fp4y1b7Dc222.csv')
                break