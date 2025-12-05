import numpy as np
import random as rd
from env import make_data, handle_progress
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
class MYMODEL:
    def __init__(self,model):
        self.model = model
        self.reload()
    def reload(self):
        self.model.fit(data_train, label_train)
        pred_p2 = self.model.predict(data_long)
        compare = np.where(pred_p2 == label_long, 1, -1)
        self.LONG_ARRAY = np.cumsum(compare)
        self.history = [rd.choice([-1,1]) for i in range(15)]
        self.short_array = np.cumsum(self.history)
        self.predict = None
        return self.LONG_ARRAY
    def predict(self, x_pred):
        self.predict = 1 if int(self.model.predict([x_pred])[0]) ==1 else 2
        return self.predict

    def check(self, result):
        if self.predict == None:
            return
        if self.predict == result:
            self.history.append(1)
        else:
            self.history.append(-1)
        self.history = self.history[-15:]
        self.short_array = np.cumsum(self.history)

def find_best_match_ncc(short_array, long_array):
    S = np.array(short_array, dtype=float)
    L = np.array(long_array, dtype=float)
    N = len(S)
    
    S_mean = np.mean(S); S_std = np.std(S)
    ncc_scores = []
    
    for i in range(len(L) - N + 1):
        window = L[i:i + N]
        L_mean = np.mean(window); L_std = np.std(window)
        if S_std == 0 or L_std == 0: ncc = 0.0
        else:
            numerator = np.sum((window - L_mean) * (S - S_mean))
            denominator = (N * L_std * S_std)
            ncc = numerator / denominator
        ncc_scores.append(ncc)
        
    ncc_scores = np.array(ncc_scores)
    best_match_index = np.argmax(ncc_scores)
    max_ncc_score = ncc_scores[best_match_index]
    
    # ----------------------------------------------------
    # SỬA ĐỔI CHÍNH: Xây dựng CỬA SỔ HIỂN THỊ CỤC BỘ
    # ----------------------------------------------------
    
    K = 10  # Số lượng phần tử tương lai muốn hiển thị
    P = 5   # Số lượng phần tử quá khứ muốn hiển thị (ngữ cảnh)
    
    start_index_int = int(best_match_index)
    
    # Xác định phạm vi hiển thị (từ P điểm trước đến K điểm sau đoạn khớp)
    local_start_index = max(0, start_index_int - P)
    local_end_index = min(len(L), start_index_int + N + K)
    
    # Cắt đoạn dữ liệu cục bộ
    local_data = L[local_start_index : local_end_index].tolist()
    
    # Xây dựng dữ liệu cho các series vẽ
    
    # 1. Đoạn khớp (Match Segment)
    match_data_local = []
    for i in range(len(local_data)):
        global_index = local_start_index + i
        if global_index >= start_index_int and global_index < start_index_int + N:
            match_data_local.append([global_index, local_data[i]])
        else:
            match_data_local.append(['-', '-']) # Dùng '-' để ECharts vẽ đường rời rạc
    
    # 2. Dữ liệu Tương lai (Prediction Segment)
    predicted_data_local = []
    for i in range(len(local_data)):
        global_index = local_start_index + i
        if global_index >= start_index_int + N and global_index < start_index_int + N + K:
            predicted_data_local.append([global_index, local_data[i]])
        else:
            predicted_data_local.append(['-', '-'])

    # Chuẩn bị dữ liệu cho biểu đồ 2 (Hình dạng)
    best_match_window = L[start_index_int : start_index_int + N]
    S_centered = S - np.mean(S)
    W_centered = best_match_window - np.mean(best_match_window)

    return {
        # Dữ liệu chính
        "best_index": start_index_int,       
        "max_score": float(max_ncc_score),    
        "n_points": int(N),
        
        # Dữ liệu cục bộ cho Biểu đồ 1
        "local_data": local_data,
        "local_start_index": local_start_index,
        "match_data_local": match_data_local,
        "predicted_data_local": predicted_data_local,
        
        # Dữ liệu cho Biểu đồ 2
        "S_centered": S_centered.tolist(),
        "W_centered": W_centered.tolist(),
    }






def FIND_BEST_MATCHS(): 
    data = []
    for name, model in models.items():
        data.append(
            find_best_match_ncc(model.short_array, model.LONG_ARRAY)
        )
    return data
def PREDICT(x_pred):
    predicts = []
    for name, model in models.items():
        predicts.append(model.predict(x_pred))
    return predicts
def CHECK(result):
    for name, model in models.items():
        model.check(result)
# ===============================
# 1. TẠO DỮ LIỆU
# ===============================
# Lấy dữ liệu
data, label = make_data()
N = len(label)

# Chia thành 2 phần
train_ratio = 0.7
split_idx = int(N * train_ratio)

# Part 1: Train
data_train = data[:split_idx]
label_train = label[:split_idx]

# Part 2: Long
data_long = data[split_idx:]
label_long = label[split_idx:]

# In kiểm tra
print("Train size:", len(label_train))
print("Long size :", len(label_long))



# ===============================
# 2. TRAIN RANDOM FOREST
# ===============================


models = {
   "Random Forest": MYMODEL( RandomForestClassifier(n_estimators=100) ),
   "K-Nearest Neighbors": MYMODEL(KNeighborsClassifier(n_neighbors=5)),
   "Naive Bayes (Gaussian)":MYMODEL( GaussianNB())
}


LONGS = []
for name, model in models.items():
    LONGS.append(model.reload())
