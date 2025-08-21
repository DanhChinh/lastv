from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os, json
from model import * #my_predict,check
app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn


@socketio.on('xulydulieu')
def handle_xulydulieu(msg):
    sid = msg.get('sid')
    progress = msg.get('progress')
    prd, value, table = my_predict(sid, progress)
    emit('server_message', {"predict": prd, "value":value, "table":table})

@socketio.on('kiemtradulieu')
def handle_kiemtradulieu(msg):
    sid = msg.get('sid')
    rs = msg.get('rs')
    table = check(sid, rs)
    emit('server_message', {"predict": 0, "value":0, "table":table})

@socketio.on('khoitao')
def handle_khoitao(msg):
    data4 = msg.get('data4')
    handleData4(data4)
    canBangTiLe()
    # make_dict()      
    # emit('server_message', {"predict": 0, "value":0, "table":reRenderTable()}) 
@socketio.on('reLoadAgl')
def handle_reLoadAgl(msg):
    name = msg.get('name') 
    action = msg.get('action')
    print(name, action)
    if action == 'reload':
        classifiers[name].reset()
    else:
        del classifiers[name]       
    emit('server_message', {"predict": 0, "value":0, "table":reRenderTable()})

@socketio.on('reLoadDict')
def handle_reLoadDict(msg):
    make_dict()      
    emit('server_message', {"predict": 0, "value":0, "table":reRenderTable()})      


@socketio.on('connect')
def handle_connect():
    print('✅ Client connected')
    emit('server_message', {"predict": 0, "value":0, "table":reRenderTable()})

@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
