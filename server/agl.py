import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA

from env import filtered, filter_reliable_predictions, make_data, handle_progress
# ---------------- Hàm vẽ kết quả phân loại ----------------
def plot_per_classifier(x_train, x_test, y_train, y_test, classifiers):
    if x_train.shape[1] > 2:
        X_all = np.vstack((x_train, x_test))
        X_all_2d = PCA(n_components=2).fit_transform(X_all)
        x_test_2d = X_all_2d[len(x_train):]
        print("🔷 Dữ liệu > 2 chiều → dùng PCA để trực quan.")
    else:
        x_test_2d = x_test
        print("🔷 Dữ liệu đã là 2 chiều → không dùng PCA.")

    num_models = len(classifiers)
    fig, axes = plt.subplots(num_models, 2, figsize=(14, 5 * num_models))
    if num_models == 1:
        axes = np.expand_dims(axes, axis=0)

    for idx, (name, model) in enumerate(classifiers.items()):
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        acc = accuracy_score(y_test, y_pred) * 100
        print(f"✅ {name} - Accuracy: {acc:.2f}%")

        # Vẽ scatter
        ax_s = axes[idx, 0]
        ax_s.scatter(x_test_2d[:, 0], x_test_2d[:, 1], c=y_pred, cmap='tab10', s=20)
        ax_s.set_title(f'{name} - Dự đoán (Acc: {acc:.2f}%)')
        ax_s.set_xlabel('Dim 1')
        ax_s.set_ylabel('Dim 2')
        ax_s.grid(True)

        # Vẽ cộng dồn
        point = np.where(y_pred == y_test, 1, -1)
        cum_point = np.cumsum(point)

        ax_c = axes[idx, 1]
        ax_c.plot(cum_point, label='Cộng dồn điểm đúng/sai')
        ax_c.axhline(0, color='gray', linestyle='--')
        ax_c.set_title(f'{name} - Cộng dồn đúng/sai')
        ax_c.set_xlabel('Mẫu')
        ax_c.set_ylabel('Tổng điểm')
        ax_c.grid(True)
        ax_c.legend()

    fig.tight_layout()
    fig.suptitle("So sánh các thuật toán phân loại", fontsize=18, y=1.02)
    # plt.show()


# ---------------- Hàm dự đoán mẫu mới ----------------
def predict_new_point(x_new, scaler, classifiers, x_train, x_test, y_train):
    if scaler:
        x_new_scaled = scaler.transform([x_new])
    else:
        x_new_scaled = [x_new]

    # Kiểm tra lọc
    y_new_pred = is_pass_filtered(scaler, x_new, X, true_labels)
    if y_new_pred is None:
        return

    print(f"🎯 Mẫu mới vượt qua lọc. Tiến hành dự đoán bằng các mô hình...")

    # PCA nếu cần
    if x_train.shape[1] > 2:
        X_all = np.vstack((x_train, x_test, x_new_scaled))
        X_all_2d = PCA(n_components=2).fit_transform(X_all)
        x_test_2d = X_all_2d[len(x_train):-1]
        x_new_2d = X_all_2d[-1]
    else:
        x_test_2d = x_test
        x_new_2d = x_new_scaled[0]

    # Vẽ điểm mới trên từng mô hình
    num_models = len(classifiers)
    fig, axes = plt.subplots(num_models, 1, figsize=(10, 5 * num_models))
    if num_models == 1:
        axes = [axes]

    for idx, (name, model) in enumerate(classifiers.items()):
        model.fit(x_train, y_train)
        y_pred_test = model.predict(x_test)
        y_pred_new = model.predict([x_new_scaled[0]])[0]

        print(f"🔍 {name}: dự đoán mẫu mới là → {y_pred_new}")

        ax = axes[idx]
        ax.scatter(x_test_2d[:, 0], x_test_2d[:, 1], c=y_pred_test, cmap='tab10', s=20, label='Tập test')
        ax.scatter(x_new_2d[0], x_new_2d[1], c='red', s=120, marker='X', label='Mẫu mới')
        ax.set_title(f'{name} - Nhãn dự đoán mẫu mới: {y_pred_new}')
        ax.set_xlabel('Dim 1')
        ax.set_ylabel('Dim 2')
        ax.grid(True)
        ax.legend()

    fig.tight_layout()
    fig.suptitle("Dự đoán và vị trí mẫu mới trên các mô hình", fontsize=18, y=1.02)
    plt.show()


#thu x,y->split-> filter(x_train)->filter(x_test)->percent
def my_predict(msg):
    x_pred = handle_progress(msg, isEnd=False)
    x_pred = scaler.transform([x_pred])
    x_pred = np.round(x_pred, 1)
    if x_train is None:
        load_polot_data()

    y_pred, _, _ = filter_reliable_predictions(x_train, x_pred, [0], knn)
    if len(y_pred)==0:
        return 1, 0
    c1 = 0
    c2 = 0
    for idx, (name, model) in enumerate(classifiers.items()):
        y_pred = int(model.predict(x_pred)[0])
        print(name, y_pred)
        if y_pred == 1:
            c1+=1
        else:
            c2+=1
    if c1>c2:
        return 1, c1-c2
    return 2, c2-c1

scaler, data, label= make_data()
classifiers = {
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "DecisionTree": DecisionTreeClassifier(),
    "RandomForest": RandomForestClassifier()
}

plot_data = {}
x_train = None
knn = None
def load_polot_data():
    global x_train, knn
    x_train, x_test, y_train, y_test = train_test_split(
    data, label, 
    train_size=0.19,
    test_size=0.019,
    shuffle=True,
    stratify=label)
    x_train, y_train, knn  = filtered(x_train, y_train, None)
    x_test, y_test, index = filter_reliable_predictions(x_train, x_test, y_test, knn)
    # x_test, y_test, knn = filtered(x_test, y_test, knn)
    for idx, (name, model) in enumerate(classifiers.items()):
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        acc = accuracy_score(y_test, y_pred) * 100
        print(f"✅ {name} - Accuracy: {acc:.2f}%")

        # Danh sách điểm để scatter
        scatter_points = []
        for i in range(len(x_test)):
            scatter_points.append({
                "x": float(x_test[i][0]),
                "y": float(x_test[i][1]),
                "pred": int(y_pred[i]),
                "true": int(y_test[i])
            })

        # Cộng dồn điểm đúng/sai
        point = np.where(y_pred == y_test, 1, -1)
        cum_point = np.cumsum(point).tolist()  # chuyển sang list JSON-compatible

        # Ghi vào dict kết quả
        plot_data[name] = {
            "accuracy": round(acc, 2),
            "scatter": scatter_points,
            "cumsum": cum_point
        }


# load_polot_data()


# Vẽ kết quả phân loại
# plot_per_classifier(x_train, x_test, y_train, y_test, classifiers)

# Dự đoán và vẽ điểm mới
# x_new = [100, 110233242 - 192246358]  # bạn có thể thay bằng bất kỳ giá trị nào
# predict_new_point(x_new, scaler, classifiers, x_train, x_test, y_train)
