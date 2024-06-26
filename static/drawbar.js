function drawbar(title, xdata, ydata){
    var opt = {
        title:{
            text: title//{{title}}//{{variable}}
        },
        xAxis:{
            type: 'category',
            data: xdata//{{xdata|safe}}//{{variable|safe}}
        },
        yAxis:{
            type: 'value'
        },
        series:{
            name: 'barchart',
            type: 'bar',
            data: ydata//{{ydata|safe}}
        }
    };
    return opt;
}
function  drawpie(percentage){
    var opt={
        title: {
            text: percentage.toString()+"%"
        },
        color:['red','white'],
        series: {
            name:'progress',
            type:'pie',
            radius:['60%','90%'],
            label:{
                show:false
            },
            data:[
                {name:'fished',value:percentage},
                {name:'unfinished',value: 100 -percentage},

            ]
        }
    }
    return opt;

}
