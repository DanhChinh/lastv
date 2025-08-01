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
        self.profits = []
        self.reset()
    def reset(self):
        self.profit = 0
        self.balance = 0
        self.sid = 0
        self.predict = None
        self.predict_fix = None
        self.percent = 0
        self.isTrue = 0
        self.isFalse = 0
        self.score = 0
        self.state = "WT"
        while self.balance > 0.51 or self.balance< 0.49:
            x_train, self.x_test, y_train, y_test = train_test_split(
                data, label,
                train_size=0.5,
                test_size=0.1#,
                #shuffle=True,
                # stratify=label
            )
            self.model.fit(x_train, y_train)
            y_pred = self.model.predict(self.x_test)
            self.mask = y_pred == y_test
            self.balance = round(sum(self.mask) / len(self.mask), 2)
        print("Khoi tao:", self.model_name)

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
            if self.profit <-100:
                self.profits.append(self.profit)
                self.reset()
                return
        self.percent = round(self.isTrue/(self.isFalse+self.isTrue), 3)
        if self.percent==0.5 and (self.isTrue+self.isFalse)>=30:
            self.profits.append(self.profit)
            self.reset()
        self.predict = ''
        self.predict_fix = ''
    def to_dict(self):
        profits = self.profits
        if len(profits) == 0:
            profits = ''
        return {
            "sid": self.sid,
            "state":self.state,
            "name": f"{self.model_name}",
            "true": self.isTrue,
            "false": self.isFalse,
            "percent": float(self.percent),
            "predict": f"{self.predict}{self.predict_fix}",
            'score':self.score,
            'profit':self.profit,
            'profits': profits
        }


# Chuẩn bị dữ liệu
scaler, data, label = make_data()

# Tạo các mô hình


classifiers = {}

classifiers[f"RandomForest"] = Model(RandomForestClassifier(n_estimators=100, max_depth=5, random_state=i), f"RF")
classifiers[f"KNN"] = Model(KNeighborsClassifier(n_neighbors=5), f"KN")
classifiers[f"LogReg"] = Model(LogisticRegression(max_iter=1000), f"LR")
classifiers[f"SVC"] = Model(SVC(probability=True, kernel='rbf'), f"SVC")
classifiers[f"DT"] = Model(DecisionTreeClassifier(max_depth=5, random_state=i), f"DT")
classifiers[f"GNB"] = Model(GaussianNB(), f"GNB")
classifiers[f"MLP"] = Model(MLPClassifier(hidden_layer_sizes=(50,), max_iter=500, random_state=i), f"MLP")
classifiers[f"GB"] = Model(GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=i), f"GB")
classifiers[f"Ada"] = Model(AdaBoostClassifier(n_estimators=50, random_state=i), f"Ada")





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




#reset persent