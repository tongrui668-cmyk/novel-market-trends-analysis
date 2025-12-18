import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Sunburst
import os

def build_sunburst_data(data, total_count):
    """
    构建旭日图数据的嵌套结构，并为每个一级分类设置独特颜色
    
    参数:
    data: DataFrame - 包含一级分类、二级分类和数量的数据集
    total_count: int - 总书籍数量
    
    返回:
    list - 符合旭日图要求的嵌套数据结构
    """
    # 为每个一级分类定义独特颜色
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
    # 遍历一级分类
    for first_level in data['一级分类'].unique():
        first_level_data = data[data['一级分类'] == first_level]
        first_level_total = first_level_data['数量'].sum()  # 一级分类总量
        
        children = []
        # 遍历二级分类
        for _, row in first_level_data.iterrows():
            percentage = row['数量'] / total_count * 100  # 计算百分比
            children.append({
                "name": row['二级分类'] if percentage >= 2.5 else "",  # 小于2.5%的隐藏名称
                "value": row['数量'],
                "tooltip": {"formatter": f"{row['二级分类']}: {row['数量']} ({percentage:.2f}%)"},  # 鼠标悬停显示详细信息
                "label": {"show": percentage >= 5}  # 小于5%的文字隐藏
            })
        
        result.append({
            "name": first_level,
            "value": first_level_total,  # 一级分类总量
            "children": children,
            "itemStyle": {"color": color_map.get(first_level, "#d9d9d9")},  # 设置一级分类颜色
            "tooltip": {"formatter": f"{first_level}: {first_level_total} ({first_level_total / total_count * 100:.2f}%)"}  # 一级分类百分比
        })
    
    return result

def generate_sunburst_chart(input_file, output_html):
    """
    生成小说分类的旭日图可视化
    
    参数:
    input_file: str - 输入Excel文件路径
    output_html: str - 输出HTML文件路径
    """
    # 加载数据
    df = pd.ExcelFile(input_file).parse('Sheet1')
    
    # 按一级分类和二级分类统计书籍数量
    category_counts = df.groupby(['一级分类', '二级分类']).size().reset_index(name='数量')
    total_count = category_counts['数量'].sum()
    
    # 构建旭日图数据
    sunburst_data = build_sunburst_data(category_counts, total_count)
    
    # 创建旭日图
    sunburst_chart = (
        Sunburst()
        .add(
            series_name="小说分类",
            data_pair=sunburst_data,
            radius=["10%", "90%"],
            label_opts=opts.LabelOpts(
                font_size=12,
                formatter="{b}",  # 显示分类名称
                position="inside",  # 将文字放置在区域内部
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="小说分类旭日图（隐藏小于5%的分类名称）"),
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"),  # 显示百分比
        )
    )
    
    # 保存为HTML文件
    sunburst_chart.render(output_html)
    print(f"动态交互的旭日图已生成并保存为 {output_html}")

def main():
    """
    主函数，执行旭日图生成流程
    """
    # 使用相对路径，确保在不同环境下都能正常运行
    input_file = '../data/飞卢小说数据.xlsx'
    output_html = '../visualizations/charts/hidden_small_labels_sunburst_chart.html'
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    
    generate_sunburst_chart(input_file, output_html)

if __name__ == "__main__":
    main()
