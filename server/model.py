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
def getScore(percent, length):
    length = min(length, 13)
    p = length/13
    if percent== 0 or percent==1 :
        return 0
    score = (percent - 0.5)*p
    return int(score*100)



class Model:
    def __init__(self, model, model_name):
        self.model = model
        self.model_name = model_name
        self.profit = 0
        self.reset()
    def reset(self):
        self.profit = 0
        self.predict = None
        self.predict_fix = None
        self.percent = 0
        self.isTrue = 0
        self.isFalse = 0
        self.score = 0
        self.state = "WT"
        self.sid = None
        self.model.fit(data, label)
    def make_predict(self, sid, x_pred):
        self.sid = sid
        self.state = "BT"
        self.predict = int(self.model.predict(x_pred)[0])

        self.score = getScore(self.percent, self.isTrue+ self.isFalse)
        if self.score>0:
            self.predict_fix = int(not self.predict)
        else:
            self.predict_fix = self.predict
            self.score = abs(self.score)

    def check(self, result, sid):
        if self.sid is None or self.sid != sid:
            self.state = "ERR"
            return
        self.state = "UPDATE"

        if self.predict == result:
            self.isTrue+=1
        else:
            self.isFalse+=1

        if self.predict_fix == result:
            self.profit += self.score
        else:
            self.profit -= self.score
        self.percent = round(self.isTrue/(self.isFalse+self.isTrue), 3)
        self.predict = ''
        self.predict_fix = ''
    def to_dict(self):
        return {
            "name": f"{self.model_name}",
            "true": self.isTrue,
            "false": self.isFalse,
            "percent": float(self.percent),
            'profit':self.profit,
            'predictf': self.predict_fix 
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
    classifiers["KNN"] = Model(KNeighborsClassifier(n_neighbors=5), "KNN")
    classifiers["LogR"] = Model(LogisticRegression(max_iter=1000), "LogR")
    classifiers["SVC"] = Model(SVC(probability=True, kernel='rbf'), "SVC")
    classifiers["DT"] = Model(DecisionTreeClassifier(max_depth=5), "DT")
    classifiers["GNB"] = Model(GaussianNB(), "GNB")
    classifiers["MLP"] = Model(MLPClassifier(hidden_layer_sizes=(50,), max_iter=500), "MLP")
    classifiers["GB"] = Model(GradientBoostingClassifier(n_estimators=100, max_depth=3), "GB")
    classifiers["Ada"] = Model(AdaBoostClassifier(n_estimators=50), "Ada")



#main
data, label = make_data()
classifiers = {}
khoiTao()
x_test = [] 
y_test = []




