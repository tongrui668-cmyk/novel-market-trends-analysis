import pandas as pd
import json  # 如果需要生成 JSON 格式数据

# 加载清洗后的分类数据
category_data = pd.read_csv('清洗后的分类数据.csv')

# 转换为 JSON 格式
scatter_data = category_data.to_dict(orient='records')
scatter_data_json = json.dumps(scatter_data, ensure_ascii=False)

# 生成 HTML 文件
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>二级分类分析</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
</head>
<body>
    <div id="chart" style="width: 100%; height: 600px;"></div>
    <script>
        var chartDom = document.getElementById('chart');
        var myChart = echarts.init(chartDom);

        // 数据
        var data = {scatter_data_json};

        // 转换数据格式
        var scatterData = data.map(function (item) {{
            return {{
                name: item["二级分类"],
                value: [item["总上榜次数"], item["平均名次"], item["书籍数量"]],
                itemStyle: {{
                    color: item["颜色"]
                }}
            }};
        }});

        // 配置项
        var option = {{
            title: {{
                text: '二级分类分析',
                left: 'center'
            }},
            tooltip: {{
                formatter: function (params) {{
                    return '分类: ' + params.data.name +
                        '<br>总上榜次数: ' + params.data.value[0] +
                        '<br>平均名次: ' + params.data.value[1] +
                        '<br>书籍数量: ' + params.data.value[2];
                }}
            }},
            xAxis: {{
                name: '总上榜次数',
                type: 'value'
            }},
            yAxis: {{
                name: '平均名次',
                type: 'value',
                inverse: true
            }},
            series: [{{
                name: '分类分析',
                type: 'scatter',
                data: scatterData,
                symbolSize: function (data) {{
                    return Math.sqrt(data[2]) * 10;  // 点大小与书籍数量相关
                }}
            }}]
        }};

        // 绘制图表
        myChart.setOption(option);
    </script>
</body>
</html>
"""

# 保存 HTML 文件
with open('二级分类分析.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML 文件已生成：二级分类分析.html")
