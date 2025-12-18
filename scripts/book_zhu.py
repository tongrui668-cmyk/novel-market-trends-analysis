import pandas as pd
import json

# 1. 加载数据
df = pd.read_excel('D:/飞卢小说数据.xlsx', sheet_name='Sheet1')

# 2. 清理列名
df.columns = df.columns.str.replace('\n', '')  # 去掉列名中的换行符

# 检查实际列名
print("数据的列名：")
print(df.columns)

# 3. 数据清洗
# 转换 "首次上榜日期(双榜)" 为 datetime 格式
df['首次上榜日期(双榜)'] = pd.to_datetime(df['首次上榜日期(双榜)'], errors='coerce')

# 添加 "首次上榜月份" 列
df['首次上榜月份'] = df['首次上榜日期(双榜)'].dt.to_period('M').astype(str)

# 按 "一级分类" 和 "首次上榜月份" 分组统计书籍数量
grouped = df.groupby(['一级分类', '首次上榜月份']).size().reset_index(name='书籍总数')

# 获取所有月份
months = grouped['首次上榜月份'].unique().tolist()

# 构建动态数据和分类顺序
data_by_month = {}
categories_by_month = {}
for month in months:
    temp = grouped[grouped['首次上榜月份'] == month]
    data = {row['一级分类']: row['书籍总数'] for _, row in temp.iterrows()}
    sorted_categories = sorted(data.items(), key=lambda x: x[1], reverse=True)
    categories = [cat[0] for cat in sorted_categories]
    values = [cat[1] for cat in sorted_categories]
    data_by_month[month] = values
    categories_by_month[month] = categories

# 转换为 JSON 格式
months_json = json.dumps(months, ensure_ascii=False)
data_by_month_json = json.dumps(data_by_month, ensure_ascii=False)
categories_by_month_json = json.dumps(categories_by_month, ensure_ascii=False)

# 4. 生成 HTML 文件
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>动态排序柱状图</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
</head>
<body>
    <div id="dynamic-bar" style="width: 100%; height: 600px;"></div>
    <script>
        var chartDom = document.getElementById('dynamic-bar');
        var myChart = echarts.init(chartDom);

        // 数据
        var months = {months_json};
        var dataByMonth = {data_by_month_json};
        var categoriesByMonth = {categories_by_month_json};

        // 动态排序柱状图配置
        var option = {{
            baseOption: {{
                timeline: {{
                    axisType: 'category',
                    autoPlay: true,
                    playInterval: 2000,
                    data: months
                }},
                tooltip: {{
                    trigger: 'axis',
                    axisPointer: {{ type: 'shadow' }}
                }},
                xAxis: {{
                    type: 'value',
                    name: '首次上榜书籍总数'
                }},
                yAxis: {{
                    type: 'category',
                    inverse: true
                }},
                series: [{{
                    type: 'bar',
                    label: {{
                        show: true,
                        position: 'right',
                        formatter: '{{c}}'
                    }}
                }}]
            }},
            options: months.map(month => {{
                return {{
                    yAxis: {{
                        data: categoriesByMonth[month]
                    }},
                    series: [{{
                        data: dataByMonth[month]
                    }}]
                }};
            }})
        }};

        // 渲染图表
        myChart.setOption(option);
    </script>
</body>
</html>
"""

# 保存 HTML 文件
with open('动态排序柱状图.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML 文件已生成：动态排序柱状图.html")
