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
    // dataZoom: [
    //     {
    //         type: 'slider',
    //         start: 70,
    //         end: 100,
    //         xAxisIndex: 0
    //     },
    //     {
    //         type: 'inside',
    //         start: 70,
    //         end: 100,
    //         xAxisIndex: 0
    //     }
    // ],
    series: [
        {
            type: 'candlestick',
            data: candleData,
            itemStyle: {
                color: '#00b050',
                color0: '#ff0000',
                borderColor: '#00b050',
                borderColor0: '#ff0000'
            },
            markPoint: {
                label: {
                    formatter: '{b}\n{c}'
                },
                data: [
                    { type: 'max', name: 'Max',valueDim: 'close' },
                    { type: 'min', name: 'Min',valueDim: 'close' }
                ]
            }
        },
        {
            type: 'line',
            symbol: 'none',
            data: [],
            smooth: true,
            lineStyle: {
                width: 1,
                color: '#330066'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'line',
                    lineStyle: {
                        color: '#ff9900'
                    }
                }
            }
        }
    ]
};

chart.setOption(option);

// Hàm tính nến từ giá trị mới
function calcCandle(open, change) {
    const close = open + change;
    if (close >= +document.getElementById('DOM_target').value) {
        isPlay = false;
        DOM_isPlay.style.backgroundColor = "black";
    }
    let low = Math.min(open, close) - Math.random() * 2;
    let high = Math.max(open, close) + Math.random() * 2;
    if(open==0 && change==0){
        low = 0;
        high= 0;
    }
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

    const result = calcCandle(+lastClose, +newChange || 0);
    candleData.push(result.candle);
    labels.push(candleData.length);

    // Tính lineData theo quy tắc: tăng 97.5%, giảm 100%
    const lineData = [];
    let lastLineValue = parseFloat(candleData[0][1]);
    lineData.push(lastLineValue);

    for (let i = 1; i < candleData.length; i++) {
        const open = parseFloat(candleData[i][0]);
        const close = parseFloat(candleData[i][1]);
        const delta = close - open;

        let adjustedDelta = delta;
        // if (delta > 0) {
        //     adjustedDelta = delta * 0.975;
        // }

        lastLineValue = lastLineValue + adjustedDelta;
        lineData.push(parseFloat(lastLineValue.toFixed(6)));
    }
    let smoothLine = smoothData(lineData)
    chart.setOption({
        xAxis: { data: labels },
        series: [
            { data: candleData },  // candlestick
            { data: smoothLine }     // line
        ]
    });
}

function smoothData(data, windowSize=3) {
    const result = [];
    const half = Math.floor(windowSize / 2);

    for (let i = 0; i < data.length; i++) {
        let sum = 0;
        let count = 0;

        for (let j = i - half; j <= i + half; j++) {
            if (j >= 0 && j < data.length) {
                sum += data[j];
                count++;
            }
        }

        result.push(Math.round(sum / count,2));
    }

    return result;
}

function getCurrentTime() {
    const now = new Date();

    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');

    return `${hours}:${minutes}:${seconds}`;
}