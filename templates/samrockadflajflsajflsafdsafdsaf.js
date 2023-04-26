

//     // ChartJs cdn binding
    let chartJsScript = document.createElement('script');
    chartJsScript.setAttribute('src','https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js');
    document.head.appendChild(chartJsScript);
    let jqueryScript = document.createElement('script');
    jqueryScript.setAttribute('src','https://code.jquery.com/jquery-3.5.1.min.js');
    document.head.appendChild(jqueryScript);
    let chartJsScript2 = document.createElement('script');
    chartJsScript2.setAttribute('src','https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js');
    document.head.appendChild(chartJsScript2);
    let chartJsCss = document.createElement('link');
    chartJsCss.setAttribute('rel','stylesheet');
    chartJsCss.setAttribute('href','https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.css');
    document.head.appendChild(chartJsCss);

    let _dataStr = [{"graphData":{"type":"line","data":{"labels":["2022-07-13","2022-07-14","2022-07-15","2022-07-16","2022-07-17","2022-07-18","2022-07-19","2022-07-20","2022-07-21"],"datasets":[{"label":"High","fill":false,"backgroundColor":"#5292a1","borderColor":"#5292a1","lineTension":0.1,"data":["20223.052734375","20789.89453125","21138.244140625","21514.404296875","21600.640625","22633.033203125","23666.962890625","24196.818359375","23368.9140625"],"yAxisID":"yAxis1"},{"label":"Low","fill":false,"backgroundColor":"#fb704d","borderColor":"#fb704d","lineTension":0.1,"data":["18999.953125","19689.2578125","20397.0","20518.8984375","20778.1796875","20781.912109375","21683.40625","23009.94921875","22707.509765625"],"yAxisID":"yAxis1"},{"label":"Open","fill":false,"backgroundColor":"#66bb6a","borderColor":"#66bb6a","lineTension":0.1,"data":["19325.97265625","20211.466796875","20573.15625","20834.103515625","21195.041015625","20781.912109375","22467.849609375","23393.19140625","23260.98828125"],"yAxisID":"yAxis1"},{"label":"Close","fill":false,"backgroundColor":"#fba730","borderColor":"#fba730","lineTension":0.1,"data":["20212.07421875","20569.919921875","20836.328125","21190.31640625","20779.34375","22485.689453125","23389.43359375","23231.732421875","22998.384765625"],"yAxisID":"yAxis1"},{"label":"Volume","fill":false,"backgroundColor":"#7e57c2","borderColor":"#7e57c2","lineTension":0.1,"data":["33042430345","31158743333","25905575359","24302954056","22927802083","39974475562","48765202697","42932549127","43243278336"],"yAxisID":"yAxis1"},{"label":"Adj Close","fill":false,"backgroundColor":"#5292a1","borderColor":"#5292a1","lineTension":0.1,"data":["20212.07421875","20569.919921875","20836.328125","21190.31640625","20779.34375","22485.689453125","23389.43359375","23231.732421875","22998.384765625"],"yAxisID":"yAxis1"}]},"options":{"animation":{},"title":{"display":true,"text":"safdasdf"},"scales":{"yAxes":[{"id":"yAxis1","ticks":{"beginAtZero":true,"fontSize":12},"scaleLabel":{"display":true,"labelString":"Count","fontSize":16}}],"xAxes":[{"ticks":{"fontSize":12},"scaleLabel":{"display":true,"labelString":""}}]},"tooltips":{"callbacks":{}}}},"graphBackground":"#0e243136","defaultFontColor":"#ffffff","ticksPreference":"Clip Text"}];

    function getAllGraphsData() {
        return new Promise((rsv, rej) => {
            setTimeout(() => {
                rsv(_dataStr || []);
            }, 1000);
        });
    }
    let _data = _dataStr;

    const drawGraph = (divId, _data) => {
        let chartCanvas = document.createElement('canvas');
        chartCanvas.setAttribute('style', "width: 100%; height: 100%;");
        chartCanvas.setAttribute('id', "sampleCanvas"+divId);
        document.getElementById(divId).appendChild(chartCanvas);

        let ctx = document.getElementById("sampleCanvas"+divId).getContext('2d');
        Chart.defaults.global.defaultFontColor = _data.defaultFontColor;
        Chart.defaults.global.defaultFontSize = 16;
        Chart.plugins.register({
            beforeDraw: function(chartInstance) {
                let ctx = chartInstance.chart.ctx;
                ctx.fillStyle = _data.graphBackground;
                ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
            }
        });
        const truncate = (input, max_length = 17) => {
            if (input.length > max_length)
               return input.substring(0,max_length) + '...';
            else
               return input;
        };
        function abbreviate_number(number, fixed) {
            if(!Date.parse(number)){
                let num = parseFloat(number)
                const COUNT_ABBRS = [ '', 'K', 'M', 'B', 'T'];
                var format = /[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)/g;
                if (isNaN(num)) { return null; } 
                if (num === null) { return null; } 
                if (num === 0) { return '0'; } 
                // if value is exponential fixed it to 2 points after decimal and return 
                if(format.test(num)){
                    return Number.parseFloat(num).toExponential(fixed);
                }
                // if value is not exponential fixed it to 2 points after decimal and return 
                fixed = (!fixed || fixed < 0) ? 0 : fixed; 
                var values = (num).toPrecision(2).split("e"), 
                    index = values.length === 1 ? 0 : Math.floor(Math.min(values[1].slice(1), 14) / 3), 
                    fixedValue = index < 1 ? num.toFixed(0 + fixed) : (num / Math.pow(10, index * 3) ).toFixed(1 + fixed), 
                    result = fixedValue < 0 ? fixedValue : Math.abs(fixedValue), 
                    valueWithUnit = result + COUNT_ABBRS [index]; 
                return valueWithUnit;
            }
            return number
        }
        function truncateValues(value, index, values) {
            // check if value is date or number
            if (!isNaN(Date.parse(value)) || !isNaN(value)) {
              return abbreviate_number(value, 2);
            } else if (_data.ticksPreference == 'Clip Text') {
              return truncate(`${value}`, 10);
            } else {
                return value;
            }
        }
        _data.graphData.options.scales.xAxes[0].ticks.callback = truncateValues;

        let myBarChart = new Chart(ctx, _data.graphData);
    }