import pandas
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
area = ['日常','手工','家居房产','绘画','搞笑','综艺','明星综合','粉丝创作','娱乐杂谈']
list_bv = []
for a in area:
    df = pandas.read_csv('data/reply_{}.csv'.format(a))
    list_unique = list(df['bv_id'].unique())
    list_bv += list_unique
    for video in list_unique:
        path = 'video_message/{}_message.txt'.format(video)
        with open(path, 'w') as f:
            df_ = df[df['bv_id'].isin([video])]
            for i,row in df_.iterrows():
                line = df.loc[i,'message']
                f.write(line)
                f.write('\n')


area = list_bv
for a in area:
    
    path = 'video_message/{}_message.txt'.format(a)
    text = open(path, "r",encoding='utf-8', errors='ignore').read()

    cut_text= jieba.cut(text)
    result = "/".join(cut_text)  
    stopwords = set()
    content = [line.strip() for line in open('stop_words.txt','r').readlines()]
    stopwords.update(content)


    wc = WordCloud(font_path='/System/Library/fonts/PingFang.ttc', background_color='white', width=400,
                height=300, max_font_size=50,
                max_words=100,stopwords = stopwords) 
    wc.generate(result)
    wc.to_file("pictures/wordcloud_{}.png".format(a)) 
    # plt.figure("词云图") 
    # plt.imshow(wc)  # 以图片的形式显示词云
    # plt.axis("off")  # 关闭图像坐标系
    # plt.show()


