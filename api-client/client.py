#!/bin/pyhton

import socket
import redis
import os
import time
import subprocess
import platform
from uuid import getnode as gma
from uuid import uuid4
import logging

'''
bin/chaosd attack process 
    Kill [-p (proccess name or id) -s (signal term)]
    stop [-p (proccess name or id)]


bin/chaosd attack cpu
 -l (load int default 10%)
 -w (workers default 1)

 subprocess.call(cmd, shell=True)
'''

CHAOSD_PATH=os.getenv("CHAOSD_PATH", "bin/chaosd")

r = redis.from_url(url=os.getenv("DBAAS_REDIS_ENDPOINT", "redis://localhost:6379/0"), charset="utf-8", decode_responses=True)


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

def set_as_busy(uid, timer):
    r.hset('host:{}'.format(uid), 'status', 'busy')
    r.expire('host:{}'.format(uid), timer)

def set_task_as_executing(task):
    r.hset(task, 'status', 'executing')

def killAttackChaosd(process, signal):
    print("Killing {process} with signal {signal}...".format(process=process, signal=signal))
    set_task_as_executing(task)
    os.system("./{} attack process kill -p {} -s {} ".format(CHAOSD_PATH, process, signal))
    r.delete(task)

def cpuAttackChaosD(workers, load):
    print("CPU Attack with {workers} 5 workers and {load}\% load...".format(workers=workers, load=load))
    set_task_as_executing(task)
    os.system("./{} attack cpu -l {load} -w {workers}".format(CHAOSD_PATH, workers=workers, load=load))
    r.delete(task)

def cpuAttack(core, load,timer, task):
    print("CPU Attack  {core} core(s) and {load}\% load...".format(core=core, load=load))
    set_task_as_executing(task)
    os.system("stress-ng -c {core} -l {load} -t {timer}".format(CHAOSD_PATH, core=core, load=load, timer=timer))
    r.delete(task)

def memoryAttack(core, load,timer, task):
    print("Memory Attack with {core} core(s) and {load}\% load...".format(core=core, load=load))
    set_task_as_executing(task)
    os.system("stress-ng -vm {core} --vm-bytes {load} -t {timer}".format(CHAOSD_PATH, core=core, load=load, timer=timer))
    r.delete(task)

def check_channel():
    # task = {
    #     "uuid": uid,
    #     "command":"{}".format(gma()), 
    #     "opts": "{}".format(platform.platform()),
    #     "status":"{}".format(status),
    #     }
    tasks_list = 'task:{}'.format(uid)
    tasks = [r.hgetall(host) for host in r.keys(tasks_list)]
    for task in tasks:
        command = r.hget(tasks_list, 'command')
        if command == 'kill':
            process = r.hget(tasks_list, 'process')
            signal = r.hget(tasks_list, 'signal') or 'term'
            killAttack(process, signal)
        elif command == 'cpu':
            core = r.hget(tasks_list, 'core')
            load = r.hget(tasks_list, 'load')
            timer = r.hget(tasks_list, 'timer')
            set_as_busy(uid, timer)
            cpuAttack(core, load,timer, tasks_list)
        elif command == 'memory':
            core = r.hget(tasks_list, 'core')
            load = r.hget(tasks_list, 'load')
            timer = r.hget(tasks_list, 'timer')
            set_as_busy(uid, timer)
            memoryAttack(core, load,timer, tasks_list)
        else:
            logging.warning("Command not found")
            r.delete(tasks_list)


while True:
    time.sleep(3)
    alive()
    check_channel()


