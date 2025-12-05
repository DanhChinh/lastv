from flask import Flask, jsonify
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
    emit('handle_predict', {"predict": predict, 'sid': msg.get('sid')}) 


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

    short_array = np.cumsum(history)
    data = find_best_match_ncc(short_array, LONG_ARRAY)
    emit("calculateAndPlot", {'data': data})
    






@socketio.on('connect')
def handle_connect():
    print('✅ Client connected')
    import random
    test_short = np.cumsum([random.choice([-1, 1]) for i in range(30)])

    data = FIND_BEST_MATCH(test_short)
    emit("calculateAndPlot", {'data': data})

@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)


