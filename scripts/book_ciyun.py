import pandas as pd
import jieba
import json

# 数据清洗和 HTML 文件生成部分
def process_book_titles(input_file, output_json, output_html):
    # 读取 Excel 文件
    excel_data = pd.ExcelFile(input_file)
    data = excel_data.parse('Sheet1')
    
    # 提取书名列
    data['书名'] = data['书名'].astype(str)  # 确保书名为字符串
    all_titles = ' '.join(data['书名'])
    
    # 分词
    words = jieba.lcut(all_titles)
    
    # 统计词频
    word_freq = {}
    for word in words:
        if len(word.strip()) > 1:  # 过滤单字
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # 过滤低频词
    word_freq = {word: freq for word, freq in word_freq.items() if freq >= 70}
    
    # 保存词频数据为 JSON 文件
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(word_freq, f, ensure_ascii=False)
    
    # 生成 HTML 文件
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>词云图</title>
        <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
    </head>
    <body>
        <h1>基于书名的词云图</h1>
        <div id="main" style="width: 800px; height: 600px;"></div>
        <script>
            // 加载词频数据
            var wordFreq = {json.dumps(word_freq, ensure_ascii=False)};
            var data = Object.entries(wordFreq).map(([name, value]) => {{ return {{ name, value }}; }});

            // 配置词云图
            var chartDom = document.getElementById('main');
            var myChart = echarts.init(chartDom);
            var option = {{
                tooltip: {{
                    show: true
                }},
                series: [{{
                    type: 'wordCloud',
                    gridSize: 2,
                    sizeRange: [12, 50],
                    rotationRange: [-90, 90],
                    shape: 'circle',
                    width: 800,
                    height: 600,
                    drawOutOfBound: true,
                    textStyle: {{
                        fontFamily: 'sans-serif',
                        fontWeight: 'bold',
                        color: function() {{
                            return 'rgb(' + [
                                Math.round(Math.random() * 255),
                                Math.round(Math.random() * 255),
                                Math.round(Math.random() * 255)
                            ].join(',') + ')';
                        }}
                    }},
                    data: data
                }}]
            }};
            myChart.setOption(option);
        </script>
    </body>
    </html>
    """
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML 文件已生成: {output_html}")


# 文件路径设置
input_file = "../data/飞卢小说数据.xlsx"  # 替换为您的文件路径
output_json = "word_freq.json"  # 替换为输出 JSON 的路径
output_html = "book_titles_wordcloud.html"  # 替换为输出 HTML 的路径

# 运行程序
process_book_titles(input_file, output_json, output_html)
