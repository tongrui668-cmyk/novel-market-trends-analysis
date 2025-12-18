import pandas as pd
import json

# 数据清洗部分
def clean_scatter_data(input_file, output_csv):
    # 加载原始数据
    df = pd.read_excel(input_file, sheet_name='Sheet1')
    
    # 数据清洗
    # 确保数值字段为数值类型
    df['总次数'] = pd.to_numeric(df['总次数\n(双榜)'], errors='coerce')
    df['最好名次'] = pd.to_numeric(df['最好名次\n(双榜)'], errors='coerce')
    df['最差名次'] = pd.to_numeric(df['最差名次\n(双榜)'], errors='coerce')
    
    # 计算平均名次
    df['平均名次'] = (df['最好名次'] + df['最差名次']) / 2
    
    # 按二级分类聚合数据
    category_data = df.groupby('二级分类').agg(
        总上榜次数=('总次数', 'sum'),  # x轴
        平均名次=('平均名次', 'mean'),  # y轴
        书籍数量=('书名', 'count')  # 点大小
    ).reset_index()
    
    # 为每个分类分配颜色（基于分类名称的唯一性）
    category_data['颜色'] = category_data.index.map(lambda x: f"hsl({x * 30 % 360}, 70%, 50%)")  # HSL颜色
    
    # 保存清洗后的数据
    category_data.to_csv(output_csv, index=False, encoding='utf-8-sig')
    return category_data

# 加载清洗后的分类数据
# category_data = pd.read_csv('清洗后的分类数据.csv')

# HTML 文件生成部分
def generate_html(category_data, output_html):
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
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

# 主函数
def main():
    # 设置文件路径
    input_file = '../data/飞卢小说数据.xlsx'
    output_csv = '../data/清洗后的分类数据.csv'
    output_html = '../visualizations/charts/二级分类分析_散点图.html'
    
    # 执行数据清洗
    category_data = clean_scatter_data(input_file, output_csv)
    print("数据清洗完成，已生成 CSV 文件：", output_csv)
    
    # 生成 HTML 文件
    generate_html(category_data, output_html)
    print("HTML 文件已生成：", output_html)

# 执行主函数
if __name__ == "__main__":
    main()
