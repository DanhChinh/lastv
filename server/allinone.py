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

