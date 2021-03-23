from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
import redis
import os


r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0)


app = Flask(__name__)
api = Api(app)


def check_if_host_exist(uuid):
    host = r.keys("host:{}".format(uuid))
    
    if len(host) == 1:
        return True
    else:
        return False

def check_if_task_not_exist(uuid):
    task = r.keys("host:{}:task".format(uuid))
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
    task_id = "host:{}:task".format(uid)
    r.hmset(task_id, task)


def abort_if_task_doesnt_exist(task_id):
    if task_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(task_id))


# TaskList
# shows a list of all tasks, and lets you POST to add new tasks
class TaskCPU(Resource):
    def get(self):
        tasks = [r.hgetall(host) for host in r.keys("host:*:task")]
        return jsonify(tasks)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid')
        parser.add_argument('command')
        parser.add_argument('opts')
        args = parser.parse_args()
        task = {
            "uuid": args['uuid'],
            "command": args['command'] , 
            "opts": args['opts'],
            "status":"wait",
        }
        host_uuid =  task['uuid']
        if check_if_host_exist(host_uuid) and check_if_task_not_exist(host_uuid):
            task_id = "host:{}:task".format(host_uuid)
            r.hmset(task_id, task)
            return task, 201
        else:
            return '{"problem": "Host not exists or task is duplicated"}', 400


# TaskList
# shows a list of all tasks, and lets you POST to add new tasks
class TaskList(Resource):
    def get(self):
        tasks = [r.hgetall(host) for host in r.keys("host:*:task")]
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

# Post test CPU
api.add_resource(TaskCPU, '/task/cpu')

if __name__ == '__main__':
    app.run(debug=True)