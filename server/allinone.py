import numpy as np
from env import make_data, handle_progress
from sklearn.ensemble import RandomForestClassifier

import numpy as np

def find_best_match_ncc(short_array, long_array):
    """
    Tính Tương quan chéo Chuẩn hóa (NCC) và trả về dữ liệu cần thiết cho ECharts.
    Đã sửa lỗi JSON serialization bằng cách dùng .item(), int(), float().
    """
    S = np.array(short_array, dtype=float)
    L = np.array(long_array, dtype=float)
    N = len(S)
    
    # 1. Tính toán NCC
    S_mean = np.mean(S); S_std = np.std(S)
    ncc_scores = []
    
    for i in range(len(L) - N + 1):
        window = L[i:i + N]
        L_mean = np.mean(window); L_std = np.std(window)
        if S_std == 0 or L_std == 0: 
            ncc = 0.0
        else:
            numerator = np.sum((window - L_mean) * (S - S_mean))
            denominator = (N * L_std * S_std)
            ncc = numerator / denominator
        ncc_scores.append(ncc)
        
    ncc_scores = np.array(ncc_scores)
    best_match_index = np.argmax(ncc_scores)
    max_ncc_score = ncc_scores[best_match_index]
    
    # 2. Chuẩn bị dữ liệu cho biểu đồ ECharts
    best_match_window = L[best_match_index : best_match_index + N]
    
    # Chuẩn hóa để so sánh hình dạng (trừ trung bình)
    S_centered = S - np.mean(S)
    W_centered = best_match_window - np.mean(best_match_window)
    
    start_index_int = int(best_match_index)
    end_index_int = int(best_match_index + N - 1)
    
    # Dữ liệu cho biểu đồ 1: Segment cần float() cho giá trị và int() cho chỉ mục
    match_segment = [
        {'coord': [start_index_int, float(LONG_ARRAY[start_index_int])]}, 
        {'coord': [end_index_int, float(LONG_ARRAY[end_index_int])]}
    ]
                     
    return {
        # Sửa lỗi JSON: Chuyển các giá trị số NumPy đơn lẻ sang kiểu Python gốc
        "best_index": start_index_int,       
        "max_score": float(max_ncc_score),    
        
        # .tolist() tự động xử lý kiểu NumPy trong mảng
        "long_array": LONG_ARRAY.tolist(),
        "match_segment": match_segment,
        "S_centered": S_centered.tolist(),
        "W_centered": W_centered.tolist(),
        "n_points": int(N)                    
    }

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
LONG_ARRAY = np.cumsum(compare)
history = []
predict = None

