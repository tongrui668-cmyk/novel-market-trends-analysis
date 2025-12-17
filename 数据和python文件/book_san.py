import pandas as pd

# 加载原始数据
df = pd.read_excel('D:/飞卢小说数据.xlsx', sheet_name='Sheet1')

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

# 保存清洗后的数据（可选）
category_data.to_csv('清洗后的分类数据.csv', index=False, encoding='utf-8-sig')

print("数据清洗完成并保存为 '清洗后的分类数据.csv'")
