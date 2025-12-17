import pandas as pd
import json

# 1. 加载数据
df = pd.read_excel('D:/飞卢小说数据.xlsx', sheet_name='Sheet1')

# 2. 清理列名
df.columns = df.columns.str.replace('\n', '')  # 去掉列名中的换行符

# 检查实际列名
print("数据的列名：")
print(df.columns)

# 更新列名列表
columns_to_clean = ['总次数(双榜)', '最好名次(双榜)', '首日鲜花', '首日评价', '首日字数(千)']

# 转换为数值类型
for col in columns_to_clean:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 3. 筛选出至少有 5 本书的作者
author_book_count = df.groupby('作者').size()
valid_authors = author_book_count[author_book_count > 5].index

# 筛选出符合条件的作者数据
filtered_df = df[df['作者'].isin(valid_authors)]

# 4. 分组统计
author_stats = filtered_df.groupby('作者').agg(
    平均上榜次数=('总次数(双榜)', 'mean'),
    平均最好名次=('最好名次(双榜)', 'mean'),
    平均首日鲜花=('首日鲜花', 'mean'),
    平均首日评价=('首日评价', 'mean'),
    平均首日字数=('首日字数(千)', 'mean')  # 此处匹配实际列名
).reset_index()

# 让所有数值保留两位小数
for col in ['平均上榜次数', '平均最好名次', '平均首日鲜花', '平均首日评价', '平均首日字数']:
    author_stats[col] = author_stats[col].round(2)

# 5. 准备雷达图数据
categories = ['平均上榜次数', '平均最好名次', '平均首日鲜花', '平均首日评价', '平均首日字数']
categories_json = json.dumps([{"name": cat} for cat in categories], ensure_ascii=False)

# 构建雷达图数据格式
radar_data = []
for _, row in author_stats.iterrows():
    radar_data.append({
        "name": row['作者'],
        "value": row[categories].tolist()
    })

# 6. 生成 HTML 文件
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>多作者雷达图对比</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
</head>
<body>
    <div style="text-align: center; font-size: 20px; margin-bottom: 20px;">超过5本书籍的作者维度对比</div>
    <div id="radar-chart" style="width: 100%; height: 600px;"></div>
    <script>
        var chartDom = document.getElementById('radar-chart');
        var myChart = echarts.init(chartDom);

        var option = {{
            title: {{
                text: '多作者维度雷达图',
                left: 'center'
            }},
            tooltip: {{
                trigger: 'item'
            }},
            legend: {{
                top: 'bottom',
                data: {json.dumps(author_stats['作者'].tolist(), ensure_ascii=False)}
            }},
            radar: {{
                indicator: {categories_json}
            }},
            series: [{{
                name: '作者对比',
                type: 'radar',
                data: {json.dumps(radar_data, ensure_ascii=False)}
            }}]
        }};
        myChart.setOption(option);
    </script>
</body>
</html>
"""

# 保存 HTML 文件
with open('多作者雷达图对比.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML 文件已生成：多作者雷达图对比.html")
