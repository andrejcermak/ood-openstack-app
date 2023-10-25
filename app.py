from flask import Flask, render_template, request
from flask import session as flask_session
from flask_socketio import SocketIO
from os_handler import *
import os
from python_terraform import Terraform

MyApp = Flask(__name__, static_url_path='/static', static_folder='./static')
MyApp.secret_key = os.urandom(12).hex()
socketio = SocketIO(MyApp)

@MyApp.route("/", methods=['GET'])
def hello():
        user = os.environ.get('USER')
        print(user)
        token = open("/home/" + str(user) + "/token.txt", "r").read().strip()
        unscoped_token = get_unscoped_token(token)
        user_id=get_user_id(token)
        flask_session['token'] = unscoped_token
        flask_session['user_id'] = user_id
        projects = list_projects(unscoped_token, user_id)
        print(projects)
        return render_template('index.html', data=projects)

@MyApp.route("/scoped", methods=['POST'])
def scope_project():
        print(request.form)
        project_id = request.form.get('selectedOption')
        flask_session['scoped_token'] = get_scoped_token(flask_session['token'], project_id)
        return render_template('show_selected_project.html', data=project_id)

@MyApp.route("/new-instance",  methods=['POST'])
def hello2():
        return render_template('instance_launched.html')

@MyApp.route("/somethingsomething",  methods=['POST'])
def launch_vm():
    print("tf launched")
    t = Terraform("./terraform/test")
    t.init()
    return_code, stdout, stderr = t.apply(skip_plan=True, var={"token": flask_session['scoped_token'] })
    return stdout + stderr

@socketio.on('compute')
def compute_task():
    output = launch_vm()
    socketio.emit('result', output)