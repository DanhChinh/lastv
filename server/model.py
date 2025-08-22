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


def hamdanhgia(mang, alpha=1.0, beta=1.0):
    # Tính cumulative sum
    cum = np.cumsum(mang)
    
    # Tính số lần đổi dấu (dao động quanh 0)
    sign_cum = np.sign(cum)
    sign_diff = np.diff(sign_cum)
    
    # Đếm số lần đổi dấu không qua zero (tức là ±1 → ∓1)
    crossings = np.sum((sign_diff != 0) & (sign_cum[:-1] != 0) & (sign_cum[1:] != 0))

    # Tính phương sai của cumulative sum
    var = np.var(cum)
    
    # Tiêu chí đánh giá:
    # Ưu tiên nhiều lần cắt qua 0 (crossings cao) và phương sai nhỏ (var thấp)
    # Tăng alpha để nhấn mạnh crossings, tăng beta để nhấn mạnh var
    score = alpha * crossings - beta * var
    return score

class Model:
    def __init__(self, model, model_name):
        self.model = model
        self.model_name = model_name
        self.profit = 0
        self.profits = []
        self.reset()
    def reset(self):
        self.profit = 0
        self.balance = 0
        self.sid = 0
        self.predict = None
        self.predict_fix = None
        self.percent = 0
        self.isTrue = 1
        self.isFalse = 1
        self.score = 0
        self.state = "WT"
        self.bestScore = -999
        self.bestModel = None
        for  i in range(20):
            x_train, _, y_train, _ = train_test_split(
                data, label,
                train_size=0.2,
                test_size=0.1#
            )
            self.model.fit(x_train, y_train)
            y_pred = self.model.predict(x_test)
            mask = y_pred == y_test
            moi = [1 if x != 0 else -1 for x in mask]
            score = hamdanhgia(moi)
            if score> self.bestScore:
                self.bestScore = score
                self.bestModel = copy.deepcopy(self.model)
                print(self.model_name, score)
        self.model = self.bestModel

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
            if self.profit >=30:
                self.reset:
                return
        else:
            self.profit -= self.score
            if self.profit<=-10:
                self.reset()
                return
        self.percent = round(self.isTrue/(self.isFalse+self.isTrue), 3)
        self.predict = ''
        self.predict_fix = ''
    def to_dict(self):
        profits = self.profits
        if len(profits) == 0:
            profits = ''
        return {
            "name": f"{self.model_name}",
            "true": self.isTrue,
            "false": self.isFalse,
            "percent": float(self.percent),
            'profit':self.profit
        }





def my_predict(sid, progress):
    x_pred = handle_progress(progress, isEnd=False)
    x_pred = scaler.transform([x_pred])
    x_pred = np.round(x_pred, 1)

    c1 = 0
    c2 = 0
    table = []
    for idx, (name, model) in enumerate(classifiers.items()):
        model.make_predict(sid, x_pred)
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

def handleData4(data4):
    global x_test, y_test
    x_test=[]
    y_test=[]
    for data in data4:
        x_pred = handle_progress(data['progress'], isEnd=False)
        x_pred = scaler.transform([x_pred])
        x_pred = np.round(x_pred, 1)

        x_test.append(x_pred[0])
        y_test.append(data['rs'])
    x_test = np.array(x_test)
    y_test = np.array(y_test)
def canBangTiLe():
    classifiers["KNN"] = Model(KNeighborsClassifier(n_neighbors=5), "KNN")
    classifiers["LogR"] = Model(LogisticRegression(max_iter=1000), "LogR")
    classifiers["SVC"] = Model(SVC(probability=True, kernel='rbf'), "SVC")
    classifiers["DT"] = Model(DecisionTreeClassifier(max_depth=5), "DT")
    classifiers["GNB"] = Model(GaussianNB(), "GNB")
    classifiers["MLP"] = Model(MLPClassifier(hidden_layer_sizes=(50,), max_iter=500), "MLP")
    classifiers["GB"] = Model(GradientBoostingClassifier(n_estimators=100, max_depth=3), "GB")
    classifiers["Ada"] = Model(AdaBoostClassifier(n_estimators=50), "Ada")

    classifiers["KNN1"] = Model(KNeighborsClassifier(n_neighbors=5), "KNN1")
    classifiers["LogR1"] = Model(LogisticRegression(max_iter=1000), "LogR1")
    classifiers["SVC1"] = Model(SVC(probability=True, kernel='rbf'), "SVC1")
    classifiers["DT1"] = Model(DecisionTreeClassifier(max_depth=5), "DT1")
    classifiers["GNB1"] = Model(GaussianNB(), "GNB1")
    classifiers["MLP1"] = Model(MLPClassifier(hidden_layer_sizes=(50,), max_iter=500), "MLP1")
    classifiers["GB1"] = Model(GradientBoostingClassifier(n_estimators=100, max_depth=3), "GB1")
    classifiers["Ada1"] = Model(AdaBoostClassifier(n_estimators=50), "Ada1")



#main
classifiers = {}
scaler, data, label = make_data()
x_test = [] 
y_test = []




