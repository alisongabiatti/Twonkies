#!/bin/pyhton

import socket
import redis
import os
import time
import subprocess
import platform
from uuid import getnode as gma
from uuid import uuid4

'''
bin/chaosd attack process 
    Kill [-p (proccess name or id) -s (signal term)]
    stop [-p (proccess name or id)]


bin/chaosd attack cpu
 -l (load int default 10%)
 -w (workers default 1)

 subprocess.call(cmd, shell=True)
'''

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0)


# Get hostname
if socket.gethostname().find('.')>=0:
    hostname=socket.gethostname()
else:
    hostname=socket.gethostbyaddr(socket.gethostname())[0]

uid = "{}".format(uuid4())

def check_task_is_runing():
    cmd = "ps aux| grep chaosd| grep -v grep"
    cmd_is_not_runing=subprocess.call(cmd, shell=True)
    if cmd_is_not_runing:
        return False
    if not cmd_is_not_runing:
        return True


def alive():
    # Check alive
    if check_task_is_runing():
        status = "busy"
    else:
        status = "alive"
    host = {
        "hostname":"{}".format(hostname),
        "uuid": uid,
        "mac":"{}".format(gma()), 
        "platform": "{}".format(platform.platform()),
        "status":"{}".format(status),
        }
    
    r.hmset("host:{}".format(uid), host)
    r.expire("host:{}".format(uid), 5)
    return status


def stop(process):
    pass

def kill(process, signal):
    print("Killing {process} with signal {signal}...".format(process=process, signal=signal))
    os.system("./chaosd {process}".format(process=process))


while True:
    time.sleep(3)
    alive()
