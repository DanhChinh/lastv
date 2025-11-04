import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from env import make_data, handle_progress
import json
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
import copy
def getScore(history):
    l = len(history)
    return sum(history) - (l/2)

def cumulative_sum(arr):
    result = []
    total = 0
    for num in arr:
        if num == 1:
            total += num
        else:
            total -= num
        result.append(total)
    return result



class Model:
    def __init__(self, model ,model_name):
        self.model = model
        self.model_name = model_name
        self.reset()
    def reset(self):
        self.predict = None
        self.predict_fix = None
        self.history = []
        self.score = 0
        self.model.fit(data, label)
    def make_predict(self, x_pred):
        self.predict = int(self.model.predict(x_pred)[0])
        self.score = getScore(self.history)
        if self.score>0:
            self.predict_fix = int(not self.predict)
        else:
            self.predict_fix = self.predict
            self.score = abs(self.score)

    def check(self, result):
        if self.predict is None:
            return
        self.history.append(int(self.predict == result))
        self.history = self.history[-30:]
        self.predict = None
        self.predict_fix = None
    def to_dict(self):
        return {
            "name": f"{self.model_name}",
            'predict':self.predict,
            'predictf': self.predict_fix ,
            'score':self.score,
            'history': self.history,
            'cumulative_sum': cumulative_sum(self.history)
        }





def my_predict( progress):
    x_pred = handle_progress(progress, isEnd=False)
    print(x_pred)
    c1 = 0
    c2 = 0
    table = []
    for idx, (name, model) in enumerate(classifiers.items()):
        model.make_predict( [x_pred])
        table.append(model.to_dict())
        if model.predict_fix == 1:
            c1+=model.score
        else:
            c2+=model.score

    return (1, c1 - c2, table) if c1 > c2 else (2, c2 - c1, table)



def check(result):
    table = []
    for name, model in classifiers.items():
        model.check(result)
        table.append(model.to_dict())
    return table

def reRenderTable():
    table = []
    for name, model in classifiers.items():
        table.append(model.to_dict())
    return table


def khoiTao():
    models = [
        KNeighborsClassifier(n_neighbors=5),
        LogisticRegression(max_iter=1000),
        SVC(probability=True, kernel='rbf'),
        DecisionTreeClassifier(max_depth=5),
        GaussianNB(),
        MLPClassifier(hidden_layer_sizes=(50,), max_iter=500),
        GradientBoostingClassifier(n_estimators=100, max_depth=3),
        AdaBoostClassifier(n_estimators=50)
    ]

    for model in models:
        name = model.__class__.__name__
        classifiers[name] = Model(model, name)






def split_array(arr, frac=0.8, random=False, seed=None):
    arr = np.array(arr)
    n = len(arr)

    if random:
        rng = np.random.default_rng(seed)
        indices = np.arange(n)
        rng.shuffle(indices)
        split_point = int(n * frac)
        idx1, idx2 = indices[:split_point], indices[split_point:]
        return arr[idx1], arr[idx2]
    else:
        split_point = int(n * frac)
        return arr[:split_point], arr[split_point:]


def test_predict(x_pred):
    c1 = 0
    c2 = 0
    for idx, (name, model) in enumerate(classifiers.items()):
        model.make_predict([x_pred])
        if model.predict_fix == 1:
            c1+=model.score
        else:
            c2+=model.score

    return (1, c1 - c2) if c1 > c2 else (0, c2 - c1)
def test_check(result):
    for name, model in classifiers.items():
        model.check(result)

import numpy as np
import matplotlib.pyplot as plt

def plot_array_and_cumsum(Arr):
    # Chuyển về numpy array
    Arr = np.array(Arr)
    
    # Tính tổng cộng dồn
    cum_sum = np.cumsum(Arr)
    
    # Tạo biểu đồ
    plt.figure(figsize=(8, 4))
    
    # Biểu đồ cột (giá trị gốc)
    plt.bar(range(len(Arr)), Arr, color='skyblue', label='Giá trị gốc')
    
    # Biểu đồ đường (tổng cộng dồn)
    plt.plot(range(len(cum_sum)), cum_sum, color='red', marker='o', label='Tổng cộng dồn')
    
    # Trang trí
    plt.title("Biểu đồ giá trị gốc và tổng cộng dồn")
    plt.xlabel("Chỉ số phần tử")
    plt.ylabel("Giá trị")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.show()
    
    return cum_sum



data, label = make_data()
classifiers = {}
khoiTao()




# data, label = make_data()
# print("Luu y: label thuoc [0, 1]")
# xtrain, xtest = split_array(data)
# ytrain, ytest = split_array(label)
# classifiers = {}
# khoiTao()


# l = len(xtest)
# profits = []
# for i in range(l):
#     choice, value =  test_predict(xtest[i])

#     test_check(ytest[i])
#     if choice == ytest[i]:
#         print(choice, ytest[i], value)
#         profits.append(value)
#     else:
#         profits.append(-value)
#         print(choice, ytest[i], -value)
# print(profits)
# plot_array_and_cumsum(profits)