const rawData = [];
const candleData = [];
const labels = [];

const chart = echarts.init(document.getElementById('echart'));

// Khởi tạo 1 cây nến đầu tiên với tất cả giá trị = 0
const initialCandle = [0, 0, 0, 0]; // [open, close, low, high]
candleData.push(initialCandle);
labels.push(1); // chỉ số 0 cho trục X


const option = {
    tooltip: { trigger: 'axis' },
    xAxis: {
        type: 'category',
        data: labels,
        scale: true
    },
    yAxis: { scale: true },
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
                    { type: 'max', name: 'Max', valueDim: 'close' },
                    { type: 'min', name: 'Min', valueDim: 'close' }
                ]
            }
        },
        {
            type: 'line',
            symbol: 'none',
            data: [],
            smooth: true,
            lineStyle: {
                width: 2
                // ,
                // color: '#330066'
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

    let low = Math.min(open, close) - Math.random() * Math.abs(change) * 0.5;
    let high = Math.max(open, close) + Math.random() * Math.abs(change) * 0.5;
    if (open == 0 && change == 0) {
        low = 0;
        high = 0;
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
function addDataToChart1(newChange) {
    rawData.push(newChange);

    const lastCandle = candleData[candleData.length - 1];
    const lastClose = parseFloat(lastCandle[1]); // lấy close của nến cuối

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
    chart.setOption({
        xAxis: { data: labels },
        series: [
            { data: candleData },  // candlestick
        ]
    });
}











function drawChart1(longArray, matchSegment, bestIndex) {
    // Biểu đồ 1: Mảng Long và Đoạn Khớp Tốt nhất
    const longData = longArray.map((value, index) => [index, value]);
    const option1 = {
        title: { text: `Mảng Long và Đoạn Khớp Tốt nhất (Index ${bestIndex})` },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'value', name: 'Chỉ số' },
        yAxis: { type: 'value', name: 'Giá trị' },
        dataZoom: [
            {
                type: 'inside',
                start: 0,
                end: 1000
            },
            {
                show: true,
                type: 'slider',
                top: '90%',
                start: 50,
                end: 100
            }
        ],
        series: [
            {
                name: 'Mảng Long (Dữ liệu)',
                type: 'line',
                data: longData,
                itemStyle: { color: 'gray' },
                lineStyle: { width: 1.5 },
                showSymbol: false,
                z: 1 // Đảm bảo nằm dưới đoạn khớp
            },
            {
                name: 'Đoạn Khớp Tốt nhất',
                type: 'line',
                data: longData.slice(bestIndex, bestIndex + matchSegment[1].coord[0] - matchSegment[0].coord[0] + 1),
                itemStyle: { color: 'red' },
                lineStyle: { width: 3 },
                showSymbol: true,
                symbolSize: 6,
                z: 2 // Đảm bảo nằm trên mảng Long
            },
            // Sử dụng markLine để đánh dấu phân đoạn (tùy chọn)
            /*
            {
                type: 'line',
                markLine: {
                    symbol: ['none', 'none'],
                    data: [
                        { xAxis: matchSegment[0].coord[0], lineStyle: { color: 'red', type: 'dashed' } },
                        { xAxis: matchSegment[1].coord[0], lineStyle: { color: 'red', type: 'dashed' } }
                    ]
                }
            }
            */
        ]
    };
    chart1.setOption(option1);
}

function drawChart2(S_centered, W_centered) {
    // Biểu đồ 2: So sánh Hình dạng (Đã trừ Trung bình)
    const sData = S_centered.map((value, index) => [index, value]);
    const wData = W_centered.map((value, index) => [index, value]);

    const option2 = {
        title: { text: 'So sánh Hình dạng (Đã trừ Trung bình)' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'value', name: 'Vị trí Tương đối' },
        yAxis: { type: 'value', name: 'Giá trị (Trừ Trung bình)' },
        series: [
            {
                name: 'Hình dạng Mẫu Short',
                type: 'line',
                data: sData,
                itemStyle: { color: 'orange' },
                lineStyle: { type: 'dashed', width: 2 },
                showSymbol: false
            },
            {
                name: 'Hình dạng Cửa sổ Khớp',
                type: 'line',
                data: wData,
                itemStyle: { color: 'blue' },
                lineStyle: { width: 2 },
                showSymbol: true,
                symbolSize: 4
            }
        ]
    };
    chart2.setOption(option2);
}

const chart1 = echarts.init(document.getElementById('chart1'));
const chart2 = echarts.init(document.getElementById('chart2'));

function calculateAndPlot(data) {
    // Cập nhật thông tin NCC
    document.getElementById('maxScore').innerText = data.max_score.toFixed(4);
    document.getElementById('bestIndex').innerText = data.best_index;

    // Vẽ biểu đồ
    drawChart1(data.long_array, data.match_segment, data.best_index);
    drawChart2(data.S_centered, data.W_centered);
}