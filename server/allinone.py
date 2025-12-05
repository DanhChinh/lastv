import numpy as np
from env import make_data, handle_progress
from sklearn.ensemble import RandomForestClassifier

import numpy as np

def best_match_index(SHORT, LONG):
    """
    Tìm index trong LONG có đoạn giống SHORT nhất về HÌNH DẠNG.
    Trả về index cuối của đoạn match (index + len(SHORT)).

    Args:
        SHORT: mảng 1 chiều (list hoặc np.array)
        LONG: mảng 1 chiều (list hoặc np.array)

    Returns:
        index cuối của đoạn match tốt nhất trong LONG
    """
    SHORT = np.array(SHORT)
    LONG = np.array(LONG)
    n = len(SHORT)

    # Chuẩn hóa SHORT về z-score
    SHORT_std = (SHORT - np.mean(SHORT)) / (np.std(SHORT) + 1e-8)

    best_score = float('inf')
    best_idx = 0

    for i in range(len(LONG) - n + 1):
        window = LONG[i:i+n]
        window_std = (window - np.mean(window)) / (np.std(window) + 1e-8)
        score = np.sum(np.abs(window_std - SHORT_std))  # MAE theo hình dạng

        if score < best_score:
            best_score = score
            best_idx = i

    return best_idx + n  # trả về index cuối của đoạn match

# def find_best_match_ncc(short_array, long_array):
def best_match_index(short_array, long_array):
    """
    Tính Tương quan chéo Chuẩn hóa (NCC) để tìm vị trí khớp tốt nhất.
    """
    S = np.array(short_array, dtype=float)
    L = np.array(long_array, dtype=float)
    N = len(S)
    
    S_mean = np.mean(S)
    S_std = np.std(S)
    
    ncc_scores = []
    
    # Trượt mảng S qua mảng L (chế độ 'valid')
    for i in range(len(L) - N + 1):
        window = L[i:i + N]
        
        L_mean = np.mean(window)
        L_std = np.std(window)
        
        if S_std == 0 or L_std == 0:
            ncc = 0.0
        else:
            # NCC = (tích chấm của mảng đã trừ trung bình) / (tích độ lệch chuẩn)
            numerator = np.sum((window - L_mean) * (S - S_mean))
            denominator = (N * L_std * S_std)
            ncc = numerator / denominator
        
        ncc_scores.append(ncc)
        
    ncc_scores = np.array(ncc_scores)
    best_match_index = np.argmax(ncc_scores)
    max_ncc_score = ncc_scores[best_match_index]
    
    # return best_match_index, max_ncc_score, ncc_scores
    return best_match_index + N


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
model = RandomForestClassifier(
    n_estimators=300,
    n_jobs=-1
)
model.fit(data_train, label_train)


# ===============================
# 3. TẠO LONG (DỰA VÀO P2)
# ===============================
pred_p2 = model.predict(data_long)

compare = np.where(pred_p2 == label_long, 1, -1)
LONG = np.cumsum(compare)
history = [1]
predict = None
indices = []

