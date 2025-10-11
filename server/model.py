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




class Model:
    def __init__(self, model ,model_name):
        self.model = model
        self.model_name = model_name
        self.reset()
    def reset(self, data, label):
        self.predict = None
        self.predict_fix = None
        self.history = []
        self.isSelect = False
        indices = np.random.choice(len(data), size=1000, replace=False)
        self.model.fit(data[indices], label[indices])
    def make_predict(self, sid, x_pred):
        self.predict = int(self.model.predict(x_pred)[0])
        self.score = getScore(self.history)
        if self.score>0:
            self.predict_fix = int(not self.predict)
        else:
            self.predict_fix = self.predict
            self.score = abs(self.score)

    def check(self, result, sid):
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
            'isSelect':self.isSelect,
            'history': f"{self.history}"
        }





def my_predict(sid, progress):
    x_pred = handle_progress(progress, isEnd=False)
    print(x_pred)
    c1 = 0
    c2 = 0
    table = []
    for idx, (name, model) in enumerate(classifiers.items()):
        model.make_predict(sid, [x_pred])
        table.append(model.to_dict())
        if not model.isSelect:
            continue
        if model.predict_fix == 1:
            c1+=model.score
        else:
            c2+=model.score

    return (1, c1 - c2, table) if c1 > c2 else (2, c2 - c1, table)

def check(sid, result):
    table = []
    for name, model in classifiers.items():
        model.check(result, sid)
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

    for i in range(16):
        index = i%8
        classifiers[f"{i}"] = Model(models[index], f"{i}_{i%8}")




data, label = make_data()
classifiers = {}
khoiTao()
x_test = [] 
y_test = []




