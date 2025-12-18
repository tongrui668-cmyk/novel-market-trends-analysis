import pandas as pd
import json
import os

def clean_data(input_file, output_json):
    """
    清洗小说数据，按月份统计首次上榜、末次上榜和入库书籍数量
    
    参数:
    input_file: str - 输入Excel文件路径
    output_json: str - 输出JSON文件路径
    
    返回:
    list - 处理后的月度统计数据
    """
    # 加载数据
    df = pd.read_excel(input_file, sheet_name='Sheet1')
    
    # 清理列名，去掉换行符
    df.columns = df.columns.str.replace('\n', '')
    
    # 转换日期格式
    df['首次上榜日期(双榜)'] = pd.to_datetime(df['首次上榜日期(双榜)'], errors='coerce')
    df['末次上榜日期(双榜)'] = pd.to_datetime(df['末次上榜日期(双榜)'], errors='coerce')
    df['入库时间'] = pd.to_datetime(df['入库时间'], errors='coerce')
    
    # 提取月份
    df['首次上榜月份'] = df['首次上榜日期(双榜)'].dt.to_period('M').astype(str)
    df['末次上榜月份'] = df['末次上榜日期(双榜)'].dt.to_period('M').astype(str)
    df['入库月份'] = df['入库时间'].dt.to_period('M').astype(str)
    
    # 按月份统计各类型书籍数量
    first_counts = df.groupby('首次上榜月份').size().reset_index(name='首次上榜数量')
    last_counts = df.groupby('末次上榜月份').size().reset_index(name='末次上榜数量')
    storage_counts = df.groupby('入库月份').size().reset_index(name='入库书籍数量')
    
    # 合并所有月份，确保每个月都有数据
    all_months = pd.concat(
        [first_counts['首次上榜月份'], last_counts['末次上榜月份'], storage_counts['入库月份']]
    ).drop_duplicates().sort_values()
    
    # 构建最终数据集
    final_data = pd.DataFrame({'月份': all_months})
    final_data = (
        final_data.merge(first_counts, left_on='月份', right_on='首次上榜月份', how='left')
        .merge(last_counts, left_on='月份', right_on='末次上榜月份', how='left')
        .merge(storage_counts, left_on='月份', right_on='入库月份', how='left')
    )
    
    # 保留需要的列，并填充缺失值为0
    final_data = final_data[['月份', '首次上榜数量', '末次上榜数量', '入库书籍数量']].fillna(0)
    
    # 转换为JSON格式并保存
    final_data_json = final_data.to_dict(orient='records')
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(final_data_json, f, ensure_ascii=False, indent=4)
    
    print(f"数据清洗完成，已生成 JSON 文件：{output_json}")
    return final_data_json

def generate_html(data, output_html):
    """
    生成书籍动态趋势对比的HTML可视化页面
    
    参数:
    data: list - 月度统计数据
    output_html: str - 输出HTML文件路径
    """
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>书籍动态趋势对比</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
</head>
<body>
    <div id="trend-chart" style="width: 100%; height: 600px;"></div>
    <script>
        // 加载数据
        var data = {json.dumps(data, ensure_ascii=False)};

        // 提取数据
        var months = data.map(item => item.月份);
        var firstCounts = data.map(item => item.首次上榜数量);
        var lastCounts = data.map(item => item.末次上榜数量);
        var storageCounts = data.map(item => item.入库书籍数量);

        // 配置折线图
        var chartDom = document.getElementById('trend-chart');
        var myChart = echarts.init(chartDom);

        var option = {{
            title: {{
                text: '书籍动态趋势对比'
            }},
            tooltip: {{
                trigger: 'axis'
            }},
            legend: {{
                data: ['首次上榜数量', '末次上榜数量', '入库书籍数量']
            }},
            xAxis: {{
                type: 'category',
                data: months
            }},
            yAxis: {{
                type: 'value',
                name: '书籍数量'
            }},
            series: [
                {{
                    name: '首次上榜数量',
                    type: 'line',
                    data: firstCounts
                }},
                {{
                    name: '末次上榜数量',
                    type: 'line',
                    data: lastCounts
                }},
                {{
                    name: '入库书籍数量',
                    type: 'line',
                    data: storageCounts
                }}
            ]
        }};

        // 渲染图表
        myChart.setOption(option);
    </script>
</body>
</html>
"""
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    
    # 保存HTML文件
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML 文件已生成：{output_html}")

def main():
    """
    主函数，执行小说市场趋势分析数据处理和可视化流程
    """
    # 使用相对路径，确保在不同环境下都能正常运行
    input_file = '../data/飞卢小说数据.xlsx'
    output_json = '../visualizations/charts/book_trend_with_storage.json'
    output_html = '../visualizations/charts/书籍动态趋势对比.html'
    
    # 执行数据清洗
    data = clean_data(input_file, output_json)
    
    # 生成可视化HTML
    generate_html(data, output_html)

if __name__ == "__main__":
    main()
