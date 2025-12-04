var isConnectGame = false;
var isConnectMyServer = false;
var accessToken = "";
var isFollow = true;
var socket_io = undefined;
var accessTokenStorege = localStorage.getItem("accessToken");
DOM_accessToken.value = accessTokenStorege;

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

DOM_isFollow.onclick = (e) => {
  isFollow = !isFollow;
  e.target.style.backgroundColor = isFollow ? "green" : "red";
}



DOM_connectPyserver.onclick = (e) => {
  socket_io = io("http://localhost:5000");

  socket_io.on("connect", () => {
    e.target.style.backgroundColor = "green";
  });

  socket_io.on('handle_longChart', (data) => {
    LONG = data.LONG;
    const xData = Array.from({ length: LONG.length }, (_, i) => i);

    longChart.setOption({
      xAxis: { data: xData },
      series: [{ data: LONG }]
    });
  });

  socket_io.on('update_chart1', (data)=>{
    addDataToChart1(data.change)
  })
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
    let predict = msg.predict;
    document.getElementById("DOM_choice").innerText = predict;
    let value = +DOM_value.value;
    if (!isFollow){
      predict = predict==1?2:1;
    }
    console.log({
      "predict":predict,
      'value':value
    })
    if (predict  && value) {
      sendMessageToGame(
        value*1000, 
        msg.sid, 
        predict)
    }
    DOM_value.value = '';
  });
};




