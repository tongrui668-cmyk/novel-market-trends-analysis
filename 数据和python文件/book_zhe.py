import pandas as pd
import json

# 1. 数据清洗
# 加载数据
df = pd.read_excel('D:/飞卢小说数据.xlsx', sheet_name='Sheet1')

# 清理列名
df.columns = df.columns.str.replace('\n', '')  # 去掉列名中的换行符

# 转换日期格式
df['首次上榜日期(双榜)'] = pd.to_datetime(df['首次上榜日期(双榜)'], errors='coerce')
df['末次上榜日期(双榜)'] = pd.to_datetime(df['末次上榜日期(双榜)'], errors='coerce')
df['入库时间'] = pd.to_datetime(df['入库时间'], errors='coerce')

# 提取月份
df['首次上榜月份'] = df['首次上榜日期(双榜)'].dt.to_period('M').astype(str)
df['末次上榜月份'] = df['末次上榜日期(双榜)'].dt.to_period('M').astype(str)
df['入库月份'] = df['入库时间'].dt.to_period('M').astype(str)

# 按月份统计首次上榜、末次上榜和入库书籍数量
first_counts = df.groupby('首次上榜月份').size().reset_index(name='首次上榜数量')
last_counts = df.groupby('末次上榜月份').size().reset_index(name='末次上榜数量')
storage_counts = df.groupby('入库月份').size().reset_index(name='入库书籍数量')

# 合并数据，确保每个月都有数据
all_months = pd.concat(
    [first_counts['首次上榜月份'], last_counts['末次上榜月份'], storage_counts['入库月份']]
).drop_duplicates().sort_values()

final_data = pd.DataFrame({'月份': all_months})
final_data = (
    final_data.merge(first_counts, left_on='月份', right_on='首次上榜月份', how='left')
    .merge(last_counts, left_on='月份', right_on='末次上榜月份', how='left')
    .merge(storage_counts, left_on='月份', right_on='入库月份', how='left')
)

# 保留需要的列，并填充缺失值为 0
final_data = final_data[['月份', '首次上榜数量', '末次上榜数量', '入库书籍数量']].fillna(0)

# 转换为 JSON 格式
final_data_json = final_data.to_dict(orient='records')
with open('book_trend_with_storage.json', 'w', encoding='utf-8') as f:
    json.dump(final_data_json, f, ensure_ascii=False, indent=4)

print("数据清洗完成，已生成 JSON 文件：book_trend_with_storage.json")

# 2. HTML 文件制作
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
        var data = {json.dumps(final_data_json, ensure_ascii=False)};

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

# 保存 HTML 文件
with open('书籍动态趋势对比.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML 文件已生成：书籍动态趋势对比.html")
