import pandas as pd
from wordcloud import WordCloud
import jieba
from collections import Counter
import string

# 从Excel文件加载数据
data_path = 'D:/飞卢小说数据.xlsx'
df = pd.ExcelFile(data_path).parse('Sheet1')

# 从"书名"列提取数据，并去除空值
book_titles = df['\u4e66\u540d'].dropna().tolist()

# 加载停用词表（可以使用自己定义的停用词表）
stop_words = set(["我", "的", "了", "是", "在", "和", "就", "也", "有", "吧", "这", "那", "你", "他", "她", "它", "他们", "我们", "什么", "一个", "不会", "可以", "没有"])  # 示例停用词
stop_words.update(string.punctuation)  # 添加标点符号作为停用词
stop_words.update(["\n", "\u3000", "\xa0"])  # 添加特殊字符

# 使用jieba对书名进行分词处理
words = []
for title in book_titles:
    # 去除标点符号
    title = ''.join([char for char in title if char not in string.punctuation])
    # 分词
    for word in jieba.lcut(title):
        if word not in stop_words and len(word) > 1:  # 过滤停用词和单字
            words.append(word)

# 使用Counter统计每个词的出现频率
word_counts = Counter(words)

# 过滤出出现次数不少于50次的词语，去除噪音
filtered_words = {word: count for word, count in word_counts.items() if count >= 40}

# 根据过滤后的词频生成词云
# font_path需要指定支持中文的字体文件，例如simhei.ttf
try:
    wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400, background_color='white').generate_from_frequencies(filtered_words)

    # 将生成的词云保存为PNG图片
    wordcloud.to_file('wordcloud.png')

    # 创建一个HTML文件用于展示词云图片
    html_content = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <title>书名词云图</title>
    </head>
    <body>
        <h1>书名词云图</h1>
        <img src=\"wordcloud.png\" alt=\"Word Cloud\">
    </body>
    </html>
    """

    # 将HTML内容写入文件
    with open('wordcloud.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 打印成功信息，提示任务完成
    print("词云图和HTML文件生成成功。")

except ModuleNotFoundError as e:
    print("需要安装缺失的模块。运行以下命令来解决：")
    print("pip install wordcloud")
    print("pip install jieba")
