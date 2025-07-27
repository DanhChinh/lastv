const rawData = [];
const candleData = [];
const labels = [];

const chart = echarts.init(document.getElementById('echart'));

// Khởi tạo 1 cây nến đầu tiên với tất cả giá trị = 0
const initialCandle = [0, 0, 0, 0]; // [open, close, low, high]
candleData.push(initialCandle);
labels.push(1); // chỉ số 0 cho trục X


const option = {
    title: { text: 'Biểu đồ Nến Nhật Cập Nhật Trực Tiếp' },
    tooltip: { trigger: 'axis' },
    xAxis: {
        type: 'category',
        data: labels,
        scale: true
    },
    yAxis: { scale: true },
    series: [{
        type: 'candlestick',
        data: candleData,
        itemStyle: {
            color: '#00b050',       // Nến tăng (Xanh lá)
            color0: '#ff0000',      // Nến giảm (Đỏ tươi)
            borderColor: '#00b050',
            borderColor0: '#ff0000'
        }

    }]
};

chart.setOption(option);

// Hàm tính nến từ giá trị mới
function calcCandle(open, change) {
    const close = open + change;
    if(close>= +document.getElementById('DOM_target').value){
        isPlay = false;
        DOM_isPlay.style.backgroundColor =  "black";
    }
    const delta = Math.random() * 2;
    const low = Math.min(open, close) - delta;
    const high = Math.max(open, close) + delta;

    return {
        candle: [
            open.toFixed(2),
            close.toFixed(2),
            low.toFixed(2),
            high.toFixed(2)
        ],
        close: close
    };
}

// Hàm thêm dữ liệu mới và cập nhật biểu đồ

function addData(newChange) {
    rawData.push(newChange);

    const lastCandle = candleData[candleData.length - 1];
    const lastClose = parseFloat(lastCandle[1]); // lấy close của nến cuối
    console.log("lastClose", lastClose)

    const result = calcCandle(+lastClose, +newChange||0);
    candleData.push(result.candle);
    labels.push(candleData.length );

    chart.setOption({
        xAxis: { data: labels },
        series: [{ data: candleData }]
    });
}
function getCurrentTime() {
    const now = new Date();

    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');

    return `${hours}:${minutes}:${seconds}`;
}

