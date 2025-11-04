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
    prd, value, table = my_predict( progress)
    print(sid, prd, value)
    emit('server_message', {"predict": prd, "value":value, "table":table})

@socketio.on('kiemtradulieu')
def handle_kiemtradulieu(msg):
    sid = msg.get('sid')
    rs = msg.get('rs')
    if rs !=1:
        rs = 0
    table = check(rs)
    emit('server_message', {"predict": 0, "value":0, "table":table})




@socketio.on('connect')
def handle_connect():
    print('✅ Client connected')
    emit('server_message', {"predict": 0, "value":0, "table":reRenderTable()})

@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
