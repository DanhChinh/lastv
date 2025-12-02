var isPlay = false;
var isConnectGame = false;
var isConnectMyServer = false;
var accessToken = "";
var accessTokenStorege = localStorage.getItem("accessToken");
DOM_accessToken.value = accessTokenStorege;


DOM_isPlay.onclick = (e) => {
  isPlay = !isPlay;
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
  e.target.style.backgroundColor = isConnectGame ? "green" : "red";

  isConnectGame ? socket_connect() : socket.close();
};
const slider = document.getElementById("slider");
const valueDisplay = document.getElementById("valueDisplay");

slider.addEventListener("input", function () {
  valueDisplay.textContent = slider.value;
});

var socket_io = undefined;


DOM_fixMGold.onclick = (e) => {
  BOT.gold = +DOM_fixM.value
  BOT.updateDom()
}
DOM_connectPyserver.onclick = (e) => {
  socket_io = io("http://localhost:5000");

  socket_io.on("connect", () => {
    e.target.style.backgroundColor = "green";
  });
  socket_io.on('handle_connect', (data) => {
    console.log("Received LONG:", data.LONG);

    LONG = data.LONG;
    const xData = Array.from({ length: LONG.length }, (_, i) => i);

    longChart.setOption({
      xAxis: { data: xData },
      series: [{ data: LONG }]
    });
  });
  // --- Nhận index từ server (highlight) ---
  socket_io.on('highlight_index', (data) => {
    highlightIdx = data.indices;  // server gửi: {indices: [5,10,15,...]}

const markPoints = highlightIdx.map((i, order) => ({
        xAxis: i,
        yAxis: LONG[i],
        symbol: 'circle',
        symbolSize: 6,           // nhỏ lại
        label: {
            show: true,
            position: 'top',     // hiện trên điểm, không che line
            offset: [0, -50],    // nâng label lên cao hơn
            formatter: (order + 1).toString(),
            fontSize: 20,        // nhỏ hơn
            color: 'black',
            fontWeight: 'bold'
        },
        itemStyle: {
            color: 'red'
        }
    }));

    longChart.setOption({
      series: [{
        markPoint: { data: markPoints }
      }]
    });
  });

  socket_io.on("handle_predict", (msg) => {

    BOT.predict = +msg.predict;
    BOT.value = 1;
    BOT.bet = Math.min(
      lamTronXuongHangNghin(BOT.gold),
      lamTronXuongHangNghin(+slider.value * BOT.value)
    );
    BOT.updateDom("server mess")

    if (BOT.predict && BOT.value) {
      sendMessageToGame(BOT.bet, record.sid, BOT.predict);
    }

    const tableData = msg.table; // hoặc data.value nếu bạn gửi cái đó
    if (Array.isArray(tableData)) {
      renderTable(tableData);
    }
  });
};

function lamTronXuongHangNghin(so) {
  return Math.floor(so / 1000) * 1000;
}



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

  data.sort(
    (a, b) => +a.isSelect - (+b.isSelect)
  )

  data.forEach(row => {
    html += "<tr>";
    headers.forEach(key => {
      let val = row[key];
      if (Array.isArray(val) || typeof val === "object") {
        val = JSON.stringify(val);
      }
      if (val == 'None') {
        val = '';
      }
      html += `<td>${val}</td>`;
    });

    html += `<td>
              <button onclick="handleReLoadAgl('${row['name']}', 'reload' )">⟲</button>
            </td>`
    html += `<td>
            <button onclick="handleReLoadAgl('${row['name']}', 'select')">✖</button>
          </td>`
    html += "</tr>";
  });

  html += "</tbody></table>";
  container.innerHTML = html;
}
function formatCurrency(num, locale = 'en-US', currency = 'USD') {
  return num.toLocaleString(locale, {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  });
}

function handleReLoadAgl(name, action) {
  console.log(name, action)
  socket_io.emit("reLoadAgl", {
    'name': name,
    'action': action
  })
}

function roundToThousand(num) {
  return Math.round(num / 1000) * 1000;
}