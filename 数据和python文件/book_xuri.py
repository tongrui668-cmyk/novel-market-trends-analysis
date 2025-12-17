import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Sunburst

# 从Excel文件加载数据
data_path = 'D:/飞卢小说数据.xlsx'
df = pd.ExcelFile(data_path).parse('Sheet1')

# 按一级分类和二级分类统计数量
category_counts = df.groupby(['一级分类', '二级分类']).size().reset_index(name='数量')
total_count = category_counts['数量'].sum()

# 构建旭日图数据的嵌套结构，并为每个一级分类设置独特颜色
def build_sunburst_data(data):
    color_map = {
        "都市言情": "#8dd3c7",
        "玄幻奇幻": "#ffffb3",
        "历史军事": "#bebada",
        "同人小说": "#fb8072",
        "科幻网游": "#80b1d3",
        "悬疑灵异": "#fdb462",
        "其他": "#b3de69"
    }
    result = []
    for first_level in data['一级分类'].unique():
        first_level_data = data[data['一级分类'] == first_level]
        first_level_total = first_level_data['数量'].sum()  # 一级分类总量
        children = []
        for _, row in first_level_data.iterrows():
            percentage = row['数量'] / total_count * 100  # 按总数计算的百分比
            children.append({
                "name": row['二级分类'] if percentage >= 2.5 else "",  # 小于5%的隐藏名称
                "value": row['数量'],
                "tooltip": {"formatter": f"{row['二级分类']}: {row['数量']} ({percentage:.2f}%)"},  # 显示详细信息
                "label": {"show": percentage >= 5}  # 小于5%的文字隐藏
            })
        result.append({
            "name": first_level,
            "value": first_level_total,  # 一级分类总量
            "children": children,
            "itemStyle": {"color": color_map.get(first_level, "#d9d9d9")},  # 默认灰色
            "tooltip": {"formatter": f"{first_level}: {first_level_total} ({first_level_total / total_count * 100:.2f}%)"}  # 一级分类百分比
        })
    return result

# 生成旭日图数据
sunburst_data = build_sunburst_data(category_counts)

# 绘制动态交互的旭日图
sunburst_chart = (
    Sunburst()
    .add(
        series_name="分类",
        data_pair=sunburst_data,
        radius=["10%", "90%"],
        label_opts=opts.LabelOpts(
            font_size=12,  # 调整字体大小
            formatter="{b}",  # 显示分类名称
            position="inside",  # 将文字放置在区域内部
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="分类旭日图（隐藏小于5%的分类名称）"),
        tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"),  # 显示百分比
    )
)

# 保存为HTML文件
sunburst_chart.render("hidden_small_labels_sunburst_chart.html")

print("动态交互的旭日图（隐藏小于5%的分类名称）已生成并保存为 hidden_small_labels_sunburst_chart.html")
