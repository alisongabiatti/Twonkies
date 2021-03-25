from flask import Flask, jsonify, render_template
from flask_restful import reqparse, abort, Api, Resource
import redis
import os


r = redis.from_url(url=os.getenv("DBAAS_REDIS_ENDPOINT", "redis://localhost:6379/0"), charset="utf-8", decode_responses=True)
if os.getenv("TSURU_APPNAME"):
    url = "poc-chaos.gcloud.dev.globoi.com"
else:
    url="127.0.0.1:5000"

# APP
# Inicialização da app
def create_app(config=None,environment=None):
    app = Flask(__name__)
    # app.config.from_object('settings')
    return app

app = create_app() 
api = Api(app)

def check_if_host_exist(uuid):
    host = r.keys("host:{}".format(uuid))
    
    if len(host) == 1:
        return True
    else:
        return False

def check_if_task_not_exist(uuid):
    task = r.keys("task:{}".format(uuid))
    if len(task) > 0:
        return False
    else:
        return True



def task(uuid, command, opts):
    task = {
        "uuid": uid,
        "command":"{}".format(gma()), 
        "opts": "{}".format(platform.platform()),
        "status":"{}".format(status),
        }
    task_id = "task:{}".format(uid)
    r.hmset(task_id, task)


def abort_if_task_doesnt_exist(task_id):
    if task_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(task_id))


# TaskCPU
# shows a list of all tasks, and lets you POST to add new tasks for CPU experiment
class TaskCPU(Resource):
    def get(self):
        tasks = [r.hgetall(host) for host in r.keys("task:*")]
        return jsonify(tasks)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid')
        parser.add_argument('command')
        parser.add_argument('core')
        parser.add_argument('load')
        parser.add_argument('timer')
        args = parser.parse_args()
        task = {
            "uuid": args['uuid'],
            "command": args['command'] , 
            "core": args['core'],
            "load": args['load'],
            "timer": args['timer'],
            "status":"wait",
        }
        host_uuid =  task['uuid']
        if check_if_host_exist(host_uuid) and check_if_task_not_exist(host_uuid):
            task_id = "task:{}".format(host_uuid)
            r.hmset(task_id, task)
            return task, 201
        else:
            return '{"problem": "Host not exists or task is duplicated"}', 400


# TaskMemory
# shows a list of all tasks, and lets you POST to add new tasks for Memory experiment
class TaskMemory(Resource):
    def get(self):
        tasks = [r.hgetall(host) for host in r.keys("task:*")]
        return jsonify(tasks)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid')
        parser.add_argument('command')
        parser.add_argument('core')
        parser.add_argument('load')
        parser.add_argument('timer')
        args = parser.parse_args()
        task = {
            "uuid": args['uuid'],
            "command": args['command'] , 
            "core": args['core'],
            "load": args['load'],
            "timer": args['timer'],
            "status":"wait",
        }
        host_uuid =  task['uuid']
        if check_if_host_exist(host_uuid) and check_if_task_not_exist(host_uuid):
            task_id = "task:{}".format(host_uuid)
            r.hmset(task_id, task)
            return task, 201
        else:
            return '{"problem": "Host not exists or task is duplicated"}', 400


# TaskKill
# shows a list of all tasks, and lets you POST to add new tasks for Kill experiment
class TaskKill(Resource):
    def get(self):
        tasks = [r.hgetall(host) for host in r.keys("task:*")]
        return jsonify(tasks)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid')
        parser.add_argument('command')
        parser.add_argument('process')
        parser.add_argument('signal')
        args = parser.parse_args()
        task = {
            "uuid": args['uuid'],
            "command": args['command'] , 
            "process": args['process'],
            "signal": args['signal'],
            "status":"wait",
        }
        host_uuid =  task['uuid']
        if check_if_host_exist(host_uuid) and check_if_task_not_exist(host_uuid):
            task_id = "task:{}".format(host_uuid)
            r.hmset(task_id, task)
            return task, 201
        else:
            return '{"problem": "Host not exists or task is duplicated"}', 400




# TaskList
# shows a list of all tasks, and lets you POST to add new tasks
class TaskList(Resource):
    def get(self):
        tasks = [r.hgetall(host) for host in r.keys("task:*")]
        return jsonify(tasks)


# Host List
# shows a list of all hosts
class HostList(Resource):
    def get(self):
        hosts = [r.hgetall(host) for host in r.keys("host:*")]
        return jsonify(hosts)


##
## Actually setup the Api resource routing here
##

# List all hosts
api.add_resource(HostList, '/hosts')

# List all tasks
api.add_resource(TaskList, '/tasks')

# CPU experiment
api.add_resource(TaskCPU, '/task/cpu')

# Memory experiment
api.add_resource(TaskMemory, '/task/memory')

# kill experiment
api.add_resource(TaskKill, '/task/kill')

# Home
@app.route('/')
def index():
    return render_template('interface.html', url=url)

if __name__ == '__main__':
    app.run(debug=True)
