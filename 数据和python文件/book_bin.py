import pandas as pd
import json

# 1. 数据清洗
# 加载数据
df = pd.read_excel('D:/飞卢小说数据.xlsx', sheet_name='Sheet1')

# 清理列名
df.columns = df.columns.str.replace('\n', '')  # 去掉列名中的换行符

# 提取相关列
df_cleaned = df[['一级分类', '首日打赏']].copy()

# 转换打赏列为数值类型
df_cleaned['首日打赏'] = pd.to_numeric(df_cleaned['首日打赏'], errors='coerce')

# 按一级分类汇总打赏总额
summary = df_cleaned.groupby('一级分类')['首日打赏'].sum().reset_index()

# 填充缺失值为0
summary['首日打赏'] = summary['首日打赏'].fillna(0)

# 转换为适合 ECharts 的数据格式
chart_data = summary.to_dict(orient='records')

# 保存为 JSON 文件
with open('category_rewards.json', 'w', encoding='utf-8') as f:
    json.dump(chart_data, f, ensure_ascii=False, indent=4)

print("数据清洗完成，已生成 JSON 文件：category_rewards.json")
