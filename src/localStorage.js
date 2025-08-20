// Hàm đọc history từ localStorage
function getHistory() {
    const raw = localStorage.getItem("history");
    if (!raw) return [];
    try {
      return JSON.parse(raw);
    } catch (e) {
      console.error("Lỗi khi parse localStorage:", e);
      return [];
    }
  }
  
  // Hàm lưu history vào localStorage
  function saveHistory(data) {
    localStorage.setItem("history", JSON.stringify(data));
  }
  
  // Hàm thêm hoặc cập nhật 1 item theo sid
  function updateHistory(sid, progress, rs) {
    if(progress === null || rs === null){return}
    const history = getHistory();
    while(history.length >=4){
      history.shift();
    }
  
    const index = history.findIndex(item => item.sid === sid);
    if (index !== -1) {
      history[index].progress = progress;
      history[index].rs = rs;
    } else {
      // Thêm mới nếu chưa có
      history.push({ sid, progress, rs });
    }
    console.log(history)
    saveHistory(history);
  }
  
  // Hàm in ra toàn bộ history
  function printHistory() {
    const history = getHistory();
    console.log("History:", history);
  }
  
  // Hàm xóa toàn bộ history
  function clearHistory() {
    localStorage.removeItem("history");
    console.log("Đã xóa history.");
  }
  


  function getLast4CompleteRecords() {
    const history = getHistory();
    
    // Lấy 4 phần tử cuối cùng từ history
    const last4 = history.slice(-4); 
  
    // Kiểm tra tính liên tục của sid
    const isContinuous = last4.every((item, index, arr) => {
      if (index === 0) return true;  // Bỏ qua phần tử đầu tiên
      return arr[index].sid === arr[index - 1].sid + 1; // Kiểm tra liệu sid có tăng dần
    });
  
    // Kiểm tra các phần tử có đầy đủ dữ liệu và sid liên tục
    const isValid = last4.length === 4 && last4.every(
      item => item.sid != null && item.progress != null && item.rs != null
    ) && isContinuous; // Thêm kiểm tra tính liên tục của sid
  
    if (!isValid) {
      // Thông báo rõ ràng trong các trường hợp lỗi
      if (last4.length < 4) {
        console.log("Chưa đủ 4 bản ghi hợp lệ.");
      } else if (!isContinuous) {
        console.log("sid không liên tục. Các giá trị sid cần phải tăng dần mà không có khoảng trống.");
      } else {
        console.log("Một hoặc nhiều trường hợp không hợp lệ. Kiểm tra lại dữ liệu của các trường progress và rs.");
      }
      return null;
    }
  
    // Nếu hợp lệ, trả về 4 bản ghi với progress và rs
    return last4.map(({ progress, rs }) => ({ progress, rs }));
  }
  
  

var historyGame = getHistory()
console.log(historyGame)
