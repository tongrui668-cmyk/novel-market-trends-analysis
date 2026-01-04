import pandas as pd
import json

# 数据清洗部分
def clean_data(input_file, output_json):
    # 读取数据
    excel_data = pd.ExcelFile(input_file)
    data = excel_data.parse('Sheet1')
    
    # 规范列名
    data.columns = data.columns.str.replace('\n', '').str.strip()
    
    # 提取需要的列并清洗数据
    data_cleaned = data[['一级分类', '首日打赏']].copy()
    data_cleaned['首日打赏'] = pd.to_numeric(data_cleaned['首日打赏'], errors='coerce')
    
    # 按一级分类汇总首日打赏
    summary = data_cleaned.groupby('一级分类', as_index=False)['首日打赏'].sum()
    
    # 填充缺失值为0
    summary['首日打赏'] = summary['首日打赏'].fillna(0)
    
    # 保存为 JSON 文件
    summary.to_json(output_json, orient='records', force_ascii=False, indent=4)
    return summary

# HTML 文件生成部分
def generate_html(input_json, output_html):
    # 加载数据
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 生成用于 ECharts 的数据格式
    chart_data = [{"name": item["一级分类"], "value": item["首日打赏"]} for item in data]
    
    # HTML 模板
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reward Visualization</title>
        <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
    </head>
    <body>
        <div id="main" style="width: 600px; height: 400px;"></div>
        <script>
            var chartDom = document.getElementById('main');
            var myChart = echarts.init(chartDom);
            var option;

            option = {{
                title: {{
                    text: '分类打赏总额占比',
                    left: 'center'
                }},
                tooltip: {{
                    trigger: 'item'
                }},
                legend: {{
                    orient: 'vertical',
                    left: 'left'
                }},
                series: [
                    {{
                        name: '打赏总额',
                        type: 'pie',
                        radius: '50%',
                        data: {chart_data},
                        emphasis: {{
                            itemStyle: {{
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }}
                        }}
                    }}
                ]
            }};

            option && myChart.setOption(option);
        </script>
    </body>
    </html>
    """
    
    # 保存 HTML 文件
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)

# 执行清洗和生成
input_file = '../data/飞卢小说数据.xlsx'
output_json = 'cleaned_data.json'
output_html = 'reward_visualization.html'

# 数据清洗
clean_data(input_file, output_json)

# 生成 HTML
generate_html(output_json, output_html)

print(f"HTML 文件已生成: {output_html}")
