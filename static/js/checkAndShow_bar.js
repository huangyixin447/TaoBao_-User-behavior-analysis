function checkdData(data, elementid,inter_name,title) {
    console.log('checkdDataR')
    var status = JSON.parse(data)
    console.log(status)
    let inst = echarts.init(document.getElementById(elementid));
    let opt = drawpie(status['percentage']);
    inst.setOption(opt);
    if ((status['isrunning'] == false) && (status['percentage'] > 99.9)) {
        console.log('clearInterval');
        clearInterval(inter_name);
        // 开始数据展示
        $.post("http://127.0.0.1:5001/getdata", function (data) {
            getdata(title,data, elementid);
        })

    }
}

function getdata(title,data, elementid) {
    var tmpdata = JSON.parse(data);
    var xdata = tmpdata['xdata']
    var ydata = tmpdata['ydata']
    console.log(elementid)
    let inst = echarts.init(document.getElementById(elementid))
    let opt = drawbar(title, xdata, ydata)
    inst.setOption(opt)

}


function drawbar(title, xdata, ydata) {
    console.log('drawbar')
    // 定义颜色数组
    var colors = ['#ff7f50', '#87cefa', '#da70d6', '#32cd32', '#6495ed', '#ff69b4', '#ffa500', '#40e0d0', '#1e90ff', '#ff6347'];

    // 将 ydata 转换为包含颜色信息的对象数组
    var coloredData = ydata.map((value, index) => ({
        value: value,
        itemStyle: {
            color: colors[index % colors.length] // 使用模运算来循环颜色
        }
    }));

    var opt = {
        title: {
            text: title,
            textStyle: {

                color: 'green', // 设置标题颜色为绿色
                fontSize: 12
            }
        },
        grid: {
            top: "30px",
            bottom: "20px",
            left: '20px',
            right: '5px'
        },
        xAxis: {
            type: 'category',
            data: xdata,
            axisLabel: {
                fontSize: 9
            }
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                fontSize: 8
            }
        },
        series: [{
            name: 'barchart',
            type: 'bar',
            barWidth: 6,
            data: coloredData
        }]
    };
    return opt;

}

function drawpie(percentage) {
    var opt = {
        animation: false,
        title: {
            text: "进度:"+percentage.toString() + "%",
            textStyle: {
                color:"green"
            }
        },
        color: ['green', 'white'],
        series: {
            name: 'progress',
            type: 'pie',
            radius: ['60%', '90%'],
            label: {
                show: false
            },
            data: [
                {name: 'fished', value: percentage},
                {name: 'unfinished', value: 100 - percentage},

            ]
        }
    }
    return opt;

}


function drawLine_time01(result1){
    var option = {
    title: {
        text: '用户行为统计',
        textStyle:{
            color:"white"
        }
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['购买', '加购', '收藏', '点击'],
        textStyle: {
                        color: 'white',  // 设置图例字体颜色
                        fontSize: 12      // 设置图例字体大小
                    }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: result1["Dates"]
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '购买',
            type: 'line',
            data: result1["daily_Buy"]
        },
        {
            name: '加购',
            type: 'line',
            data: result1["daily_Cart"]
        },
        {
            name: '收藏',
            type: 'line',
            data: result1["daily_Fav"]
        },
        {
            name: '点击',
            type: 'line',
            data: result1["daily_Pv"]
        }
    ]
}
    return option;


}


function drawLine_time02(result1){
    var option = {
    title: {
        text: '分时行为统计',
        textStyle:{
            color:"white"
        }
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['购买', '加购', '收藏', '点击'],
        textStyle: {
                        color: 'white',  // 设置图例字体颜色
                        fontSize: 12      // 设置图例字体大小
                    }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: result1["Hours"]
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '购买',
            type: 'line',
            data: result1["Hour_Buy"]
        },
        {
            name: '加购',
            type: 'line',
            data: result1["Hour_Cart"]
        },
        {
            name: '收藏',
            type: 'line',
            data: result1["Hour_Fav"]
        },
        {
            name: '点击',
            type: 'line',
            data: result1["Hour_Pv"]
        }
    ]
}
    return option;


}
