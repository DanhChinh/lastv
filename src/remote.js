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

  // --- Nhận index từ server (highlight) ---
  socket_io.on('best_matchs', (msg)=>{
    calculateAndPlot(msg.best_matchs)

  })

  socket_io.on("handle_predict", (msg) => {
    let predicts = msg.predicts;
    for(let i=0; i<3; i++){
      DOM_predicts[i].innerText = predicts[i];
    }
    // document.getElementById("DOM_choice").innerText = predict;
    // let value = +DOM_value.value;
    // if (!isFollow){
    //   predict = predict==1?2:1;
    // }
    // console.log({
    //   "predict":predict,
    //   'value':value
    // })
    // if (predict  && value) {
    //   sendMessageToGame(
    //     value*1000, 
    //     msg.sid, 
    //     predict)
    // }
    // DOM_value.value = '';
  });
};




