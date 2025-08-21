import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler

# Đọc file CSV

def handle_progress(progress, isEnd = True):
    progress_arr = json.loads(progress)
    if isEnd and len(progress_arr) != 49:
        return None
    pair = progress_arr[34]
    # data = []
    # for pair in sublist:
    #     data.extend([pair[0]['bc'], pair[1]['bc'], pair[0]['v'],pair[1]['v']])
    return [pair[0]['bc']- pair[1]['bc'], pair[0]['v']-pair[1]['v']]

def make_data():
    df = pd.read_csv("data.csv")
    data_perfect = []
    label_perfect = []
    for index, row in df.iterrows():
        formater = handle_progress(row['progress'])
        if formater:
            data_perfect.append(formater)
            rs18 = row['d1']+row['d2']+row['d3']
            label_perfect.append(1 if rs18>10 else 0)


    data = np.array(data_perfect)
    label = np.array(label_perfect)

    scaler = RobustScaler()
    data = scaler.fit_transform(data)
    data = np.round(data, 1)
    return scaler, data, label

def split_array(arr, ratio=0.7, shuffle=False):

    
    arr = np.array(arr)
    if shuffle:
        np.random.shuffle(arr)

    split_idx = int(len(arr) * ratio)
    return arr[:split_idx], arr[split_idx:]

