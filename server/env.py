from collections import defaultdict
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
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
    """
    Tách mảng thành 2 phần theo tỉ lệ cho trước (mặc định 7:3).
    
    Parameters:
        arr (list hoặc np.array): Mảng đầu vào.
        ratio (float): Tỉ lệ phần đầu tiên (0 < ratio < 1).
        shuffle (bool): Nếu True thì trộn ngẫu nhiên trước khi chia.

    Returns:
        tuple: (phần 1, phần 2)
    """
    
    arr = np.array(arr)
    if shuffle:
        np.random.shuffle(arr)

    split_idx = int(len(arr) * ratio)
    return arr[:split_idx], arr[split_idx:]

#return model
def filtered(X,y,knn ):
    if knn is None:
        knn = KNeighborsClassifier(n_neighbors=8)
        knn.fit(X, y)
    y_pred = knn.predict(X)

    # Chỉ giữ những mẫu dự đoán đúng
    mask = y_pred == y
    X_filtered = X[mask]
    y_filtered = y[mask]
    return X_filtered, y_filtered, knn



from sklearn.neighbors import NearestNeighbors
import numpy as np

def filter_reliable_predictions(X_train, x_pred_array, y_pred_array, knn, threshold_factor=2.0):
    """
    Lọc các mẫu đáng tin cậy dựa trên khoảng cách tới tập huấn luyện.

    Args:
        X_train (ndarray): Tập huấn luyện (n_samples_train, n_features).
        x_pred_array (ndarray): Tập mẫu cần lọc (n_samples_pred, n_features).
        y_pred_array (ndarray or list): Nhãn dự đoán ứng với từng dòng trong x_pred_array.
        knn (KNeighborsClassifier): Mô hình KNN đã huấn luyện.
        threshold_factor (float): Hệ số nhân với std để xác định ngưỡng.

    Returns:
        filtered_x (ndarray): Các mẫu đầu vào đã qua lọc.
        filtered_y (ndarray): Nhãn dự đoán tương ứng.
        filtered_indices (list[int]): Vị trí ban đầu trong x_pred_array của các mẫu được giữ lại.
    """

    # 1. Tính ngưỡng khoảng cách tin cậy từ X_train
    nn = NearestNeighbors(n_neighbors=9)
    nn.fit(X_train)
    distances_all, _ = nn.kneighbors(X_train)
    nearest_distances = distances_all[:, 1]  # Bỏ khoảng cách với chính nó

    mean_dist = nearest_distances.mean()
    std_dist = nearest_distances.std()
    threshold = mean_dist + threshold_factor * std_dist

    print(f"📊 Ngưỡng khoảng cách tin cậy (auto): {threshold:.4f}")

    # 2. Tính khoảng cách mẫu mới đến hàng xóm gần nhất trong X_train
    distances_new, _ = nn.kneighbors(x_pred_array)
    distance_to_nearest = distances_new[:, 0]

    # 3. Lọc ra các mẫu đáng tin cậy
    filtered_x = []
    filtered_y = []
    filtered_indices = []

    for i, dist in enumerate(distance_to_nearest):
        if dist <= threshold:
            filtered_x.append(x_pred_array[i])
            filtered_y.append(y_pred_array[i])
            filtered_indices.append(i)
            print(f"✅ Mẫu {i} OK - Nhãn: {y_pred_array[i]}, Khoảng cách: {dist}")
        else:
            print(f"⚠️ Mẫu {i} bị loại - Khoảng cách: {dist:.4f}")

    return np.array(filtered_x), np.array(filtered_y), filtered_indices







history4 = pd.DataFrame(columns=["sid", "progress", "rs"])
isInit = False

import pandas as pd

# Tạo DataFrame ban đầu (ví dụ)
history4 = pd.DataFrame(columns=["sid", "progress", "rs"])

def addHistory(sid, progress, rs):
    global history4
    # Kiểm tra nếu sid đã có trong DataFrame
    if sid in history4["sid"].values:
        # Nếu sid đã có, cập nhật rs
        history4.loc[history4["sid"] == sid, "rs"] = rs
    else:
        # Nếu sid chưa có, thêm một dòng mới với sid, progress và rs
        new_row = pd.DataFrame({"sid": [sid], "progress": [progress], "rs": [rs]})
        
        # Loại bỏ các cột có toàn giá trị NA hoặc trống (nếu có)
        new_row = new_row.dropna(axis=1, how="all")
        
        # Thực hiện concat sau khi xử lý
        history4 = pd.concat([history4, new_row], ignore_index=True)
    
    # Lấy 4 hàng cuối của DataFrame
    last_4_rows = history4.tail(4)
    
    # Kiểm tra nếu số dòng là 4 và không có giá trị NaN trong dữ liệu
    if len(last_4_rows) == 4 and not last_4_rows.isna().any().any():
        # Trả về 2 cột 'progress' và 'rs'
        result = last_4_rows[["progress", "rs"]]
        print(result)
        return result
    else:
        print("Không thỏa mãn điều kiện (số dòng khác 4 hoặc có NaN).")
        return None


