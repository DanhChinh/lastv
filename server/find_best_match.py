import numpy as np
import matplotlib.pyplot as plt

def find_best_match_ncc(short_array, long_array):
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
    
    return best_match_index, max_ncc_score, ncc_scores

def plot_correlation(short_array, long_array, best_index, ncc_scores):
    """
    Vẽ biểu đồ hiển thị mảng dữ liệu, mẫu, cửa sổ khớp tốt nhất và điểm NCC.
    """
    S = np.array(short_array, dtype=float)
    L = np.array(long_array, dtype=float)
    N = len(S)
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # --- Biểu đồ 1: Dữ liệu và Khớp Mẫu (Data and Template Match) ---
    ax1 = axes[0]
    ax1.plot(L, label='Mảng Long (Dữ liệu Lớn)', color='gray', linestyle='--')
    
    # Lấy cửa sổ khớp tốt nhất
    best_match_window = L[best_index : best_index + N]
    
    # Chuẩn hóa (trừ trung bình) mảng S và cửa sổ khớp để so sánh hình dạng
    # Chúng ta dịch chuyển mẫu S để trùng với độ lớn của cửa sổ khớp tốt nhất
    # Chỉ dịch chuyển trung bình để hình dạng khớp nhau trên biểu đồ
    shifted_S = S - np.mean(S) + np.mean(best_match_window)
    
    # Vẽ Mẫu (Template) tại vị trí khớp tốt nhất
    ax1.plot(range(best_index, best_index + N), shifted_S, 
             label='Mẫu Short (Dịch chuyển để so sánh)', 
             color='orange', linewidth=2)
             
    # Đánh dấu cửa sổ khớp tốt nhất trên mảng Long
    ax1.plot(range(best_index, best_index + N), best_match_window, 
             label='Cửa sổ Khớp Tốt nhất', 
             color='red', marker='o', linestyle='None', markersize=5)
             
    ax1.set_title('Hình dạng Mẫu Short so với Cửa sổ Khớp Tốt nhất trong Mảng Long')
    ax1.set_xlabel('Chỉ số')
    ax1.set_ylabel('Giá trị')
    ax1.legend()
    ax1.grid(True)
    
    # --- Biểu đồ 2: Điểm Tương quan chéo Chuẩn hóa (NCC Scores) ---
    ax2 = axes[1]
    match_indices = np.arange(len(ncc_scores))
    ax2.plot(match_indices, ncc_scores, 
             label='Điểm NCC', 
             color='blue', marker='o', linestyle='-')
             
    # Đánh dấu vị trí tối đa
    ax2.plot(best_index, ncc_scores[best_index], 
             marker='*', markersize=15, color='red', 
             label=f'NCC Max: {ncc_scores[best_index]:.4f} tại Index {best_index}')
             
    ax2.set_title('Biểu đồ Tương quan chéo Chuẩn hóa (NCC)')
    ax2.set_xlabel('Vị trí Bắt đầu Khớp')
    ax2.set_ylabel('Điểm NCC (Từ -1 đến 1)')
    ax2.axhline(1, color='green', linestyle='--', linewidth=0.5, label='Khớp Hoàn hảo (1)')
    ax2.axhline(0, color='black', linestyle='--', linewidth=0.5)
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

