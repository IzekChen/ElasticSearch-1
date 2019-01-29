#coding: UTF-8 
#########################################################################################
# Developer: Deiner Zapata Silva.
# Date: 29/11/2018
# Description: Codigo util, para uso general
# sys.setdefaultencoding('utf-8') #reload(sys)
#########################################################################################
import sys, requests, json, csv
from datetime import datetime, timedelta
from flask import Flask, request, abort
import time, os, socket
from subprocess import Popen, PIPE
########################################################################################
def print_json(json_obj):
    print(json.dumps(json_obj, indent=2, sort_keys=True))
    return
#######################################################################################
def print_list(lista):
    num = 0
    for item in lista:
        print("\t{0:03d}. {1} ".format( num, item) )
        num+=1
    return
#######################################################################################
def fileTXT_save(text, nameFile = "fileTXT_save.txt"):
    fnew  = open(nameFile,"wb")
    fnew.write(text.encode('utf-8')) # str(aux=[line])+'\n'
    fnew.close() 
    return
#######################################################################################
def count_elapsed_time(f,*args,**kwargs):
    """
    Decorator.
    Calculate the elapsed time of a function.
    """
    def wrapper(*args):
        #from time import time
        start_time = time.time()
        ret = f(*args,**kwargs)
        elapsed_time = time.time() - start_time
        print("[count_elapsed_time] "+f.__name__+"Elapsed time: %0.10f seconds." % elapsed_time)
        return ret
    return wrapper
#######################################################################################
def list2json(list_field, list_value,remove_char=None):
    data_json = {}
    len_field = len(list_field)
    len_value = len(list_value)
    if (len_field>len_value):
        print("[ERROR] list2json len_field:{0} > len_value:{1}".format(len_field,len_value))
        print(str(list_field))
        print(str(list_value))
    else:
        for i in range(0,len_field):
            if (len(list_field[i])>0):
                if (len(list_value[i])>0):
                    if(remove_char!=None):
                        list_value[i]=list_value[i].replace(remove_char,"")
                    data_json.update({list_field[i] : list_value[i]})
                else:
                    print("[WARN] field value lost [{0}]".format(list_value[i]))
    return data_json
#######################################################################################
def loadCSVtoJSON(path):
    csvfile = open(path)
    data = csv.DictReader(csvfile)
    list_data = []
    
    for row in data:
        list_data.append(row)
    
    print("["+str(path)+"] -> Datos cargados:" + str(len(list_data)))
    return list_data
#######################################################################################
def isAliveIP(host, count=1, timeout=1000):
    if sys.platform == 'win32':
        count_arg = '-n'
        timeout_arg = '-w'
    else:
        count_arg = '-c'
        timeout_arg = '-W'

    args = map(str, [ 'ping', count_arg, count, timeout_arg, timeout, host ])

    p = Popen(args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    # success
    val = p.returncode
    if p.returncode == 0:
        #try:
            #m = re.search("time=(\d+(?:\.\d+){0,1})\s*ms", output)
            #time = float(m.group(1))
            #time = 1
        #except Exception, e:
        #	time = -1
        return True
    else:
        #time = None
        return False    
    #return (time, p.returncode)
###############################################################################
def send_json(msg, IP="0.0.0.0", PORT = 2233):
    """
        #Configuracion en /etc/logstash/conf.d/logstash-syslog.conf
        input{
            tcp{
                port => [PORT_NUMBER]
                codec => json
            }
        }
    """
    if(type(PORT)==str):
        PORT = int(PORT)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect( (IP,PORT) )
        #print("sending message: "+str(msg))
        datajs = json.dumps(msg)
        sock.sendall( datajs.encode() )
    except:
        print("Error inesperado: "+sys.exc_info()[0])
        #sys.exit(1)
        return
    finally:
        sock.close()
        return
#######################################################################################
