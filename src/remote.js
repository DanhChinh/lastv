var isPlay = false;
var isConnectGame = false;
var isConnectMyServer = false;
var accessToken = "";
var isReverse = false;
var accessTokenStorege = localStorage.getItem("accessToken");
DOM_accessToken.value = accessTokenStorege;


DOM_isPlay.onclick = (e) => {
  isPlay = !isPlay;
  e.target.textContent = isPlay ? "Playing..." : "play";
  e.target.style.backgroundColor = isPlay ? "green" : "red";
};


DOM_isConnectGame.onclick = (e) => {
  if (DOM_accessToken.value) {
    accessToken = DOM_accessToken.value;
    localStorage.setItem("accessToken", accessToken);
  } else {
    return;
  }
  isConnectGame = !isConnectGame;
  e.target.textContent = isConnectGame ? "Connected" : "Connect";
  e.target.style.backgroundColor = isConnectGame ? "green" : "red";

  isConnectGame ? socket_connect() : socket.close();
};
const slider = document.getElementById("slider");
const valueDisplay = document.getElementById("valueDisplay");

slider.addEventListener("input", function () {
  valueDisplay.textContent = slider.value;
});
DOM_reverse.onclick = (e) => {
  isReverse = !isReverse;
  e.target.textContent = isReverse ? "Reverse..." : "no Reverse";
  e.target.style.backgroundColor = isReverse ? "black" : "blue";
};
var socket_io = undefined;

DOM_connectPyserver.onclick = (e) => {
  socket_io = io("http://localhost:5000");

  socket_io.on("connect", () => {
    console.log("✅ Đã kết nối tới server!");
    e.target.textContent = "Connected" ;
    e.target.style.backgroundColor = "green" ;
  });
  socket_io.on("server_message", (msg) => {
    // console.log("📩 Server: " + JSON.stringify(msg));
    prd = msg.predict
    value = msg.value
    if(prd && value){
      DOM_choice.innerText = prd;
      DOM_value.innerText = value;
      if(isReverse){
        prd = prd == 1? 2: 1;
      }
      sendMessageToGame(slider.value * value, record.sid, prd);
    }

    const tableData = msg.table; // hoặc data.value nếu bạn gửi cái đó
    if (Array.isArray(tableData)) {
      renderTable(tableData);
    }
});
};




function renderTable(data) {
  const container = document.getElementById("table-container");
  if (!data.length) {
    container.innerHTML = "<p>Không có dữ liệu</p>";
    return;
  }

  const headers = Object.keys(data[0]);
  let html = "<table border='1' cellpadding='5'><thead><tr>";
  headers.forEach(key => {
    html += `<th>${key}</th>`;
  });
  html += "</tr></thead><tbody>";

  data.forEach(row => {
    if(row['score']==0){
      html += `<tr class="None">`;

    }else{
      html += "<tr>";

    }
    headers.forEach(key => {
      let val = row[key];
      if (Array.isArray(val) || typeof val === "object") {
        val = JSON.stringify(val);
      }
      if(val == 'None'){
        val='';
      }
      html += `<td>${val}</td>`;
    });
    html += "</tr>";
  });

  html += "</tbody></table>";
  container.innerHTML = html;
}
