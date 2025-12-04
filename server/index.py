from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os, json
from allinone import *
from env import handle_progress
app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả nguồn


@socketio.on('predict')
def handle_predict(msg):
    global predict
    progress = msg.get('progress')
    x_pred = handle_progress(progress, isEnd=False)
    predict = 1 if int(model.predict([x_pred])[0]) ==1 else 2
    print("predict", predict)
    emit('handle_predict', {"predict": predict})


@socketio.on('check')
def handle_check(msg):
    global history, indices
    result = msg.get('rs')
    if predict == None:
        return
    if predict == result:
        history.append(1)
    else:
        history.append(-1)
    history = history[-30:]
    print("history", history)
    indices.append(best_match_index(np.cumsum(history), LONG))
    indices = indices[-5:]
    print("indices", indices)
    emit('highlight_index', {"indices": indices})
    





@socketio.on('connect')
def handle_connect():
    print('✅ Client connected')
    emit('handle_connect', {"LONG":LONG.tolist()})

@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
