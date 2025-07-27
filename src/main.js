

function sendMessageToGame(b, sid, eid) {
  if (!b || !sid || !eid || !isPlay ) {
    return 0;
  }

  let message = JSON.stringify(MESSAGE_WS.bet(b, sid, eid));
  addMessage(`${b} ->${eid}`, "player")

  socket.send(message);
}
var MESSAGE_WS = {
  url: "wss://mynylifes.hytsocesk.com/websocket_live",
  login: (accessToken) => [
    1,
    "MiniGame2",
    "",
    "",
    { agentId: "1", accessToken: accessToken, reconnect: false },
  ],

  info: ["6", "MiniGame2", "taixiu_live_gateway_plugin", { cmd: 15000 }],
  result: (counter) => ["7", "MiniGame2", "1", counter],
  bet: (b, sid, eid) => [
    "6",
    "MiniGame2",
    "taixiu_live_gateway_plugin",
    { cmd: 15002, b: b, sid: sid, aid: 1, eid: eid },
  ],
};

function sendDataToThuhuyenFun(record) {
  if (record.progress.length === 0) {
    return;
  }
  let data = new FormData();
  data.append("sid", record.sid);
  data.append("progress", JSON.stringify(record.progress));
  data.append("d1", record.d1);
  data.append("d2", record.d2);
  data.append("d3", record.d3);
  axios
    .post("https://thuhuyen.fun/xg79/post_data.php", data)
    .then((response) => {
      if (response.data.success) {
        addMessage("save->done", "server");
      } else {
        console.error("Lỗi: " + response.data.message);
      }
      // console.groupEnd()
    })
    .catch((error) => {
      console.error("Lỗi kết nối:", error);
    });
}
var sendInterval;
var counter_send = 0;
var socket;
var is_betting = false;
var is_bet_success = false;
var initRecord = (
  sid = undefined,
  progress = [],
  d1 = undefined,
  d2 = undefined,
  d3 = undefined
) => {
  return { sid, progress, d1, d2, d3 };
};
var record = initRecord();

function socket_connect() {
  socket = new WebSocket(MESSAGE_WS.url);

  socket.onopen = function (event) {
    addMessage("WebSocket ->opened", "server");
    socket.send(JSON.stringify(MESSAGE_WS.login(accessToken)));
  };

  socket.onmessage = async function (event) {
    let mgs = JSON.parse(event.data)[1];

    if (typeof mgs === "object") {
      //betting
      if (mgs.cmd === 15007 && is_betting) {
        record.progress.push(JSON.parse(JSON.stringify(mgs.bs)));

        if (record.progress.length === 35) {
          // [prd, value] = await predict(JSON.parse(JSON.stringify(record.progress)));
          socket_io.emit("xulydulieu",{
            'sid':record.sid ||1,
            'progress':JSON.stringify(record.progress)
          });
        }
        return;
      }
      //ending
      if (mgs.cmd === 15006) {
        record.sid = mgs.sid;
        record.d1 = mgs.d1;
        record.d2 = mgs.d2;
        record.d3 = mgs.d3;
        // sendDataToThuhuyenFun(JSON.parse(JSON.stringify(record)));
        is_betting = false;
        let rs = mgs.d1 + mgs.d2 + mgs.d3;
        addMessage(`${rs}`, "server")
        rs = rs > 10 ? 1 : 2;
        checkPrd(prd, rs, value);
        socket_io.emit("kiemtradulieu", {
          'sid':record.sid ||1,
          'rs':rs==1?1:0
        })
        return;
      }
      //start
      if (mgs.cmd === 15005) {
        record = initRecord();
        record.sid = mgs.sid;
        // console.group(record.sid);
        is_betting = true;
        is_bet_success = false;
        return;
      }
      //sended
      if (mgs.cmd === 15002) {
        addMessage("Accept", "server")
        is_bet_success = true;
        return;
      }

      if (mgs.cmd === 100) {
        addMessage(JSON.stringify(mgs), "server")
        return;
      }
    } else {
      if (mgs === true) {
        socket.send(JSON.stringify(MESSAGE_WS.info));
        addMessage("sendInterval keep ws", "player");
        setTimeout(() => {
          sendInterval = setInterval(() => {
            socket.send(JSON.stringify(MESSAGE_WS.result(counter_send)));
            counter_send++;
          }, 5000);
        }, 5000);
      }
    }
  };

  socket.onclose = function (event) {
    clearInterval(sendInterval);
    // alert('Kết nối WebSocket đã đóng.');
    setTimeout(() => {
      socket_connect();
    }, 1000);
  };

  socket.onerror = function (error) {
    console.error("Lỗi WebSocket:", error);
  };
  return socket;
}


var prd = undefined;
var value = 0;
function checkPrd(prd, rs, value) {
  let reward = value;
  if (prd != rs) {
    reward *= -1
  }
  addData(reward)
}
