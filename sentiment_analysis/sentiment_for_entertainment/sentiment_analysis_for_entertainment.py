from cnsenti import Sentiment
import pandas
import csv
# area = ['日常','手工','家居房产','绘画','搞笑']
area = ['娱乐杂谈','综艺','明星综合','粉丝创作']
# area = ['原创音乐','翻唱','演奏','VOCALOID','音乐现场','MV','乐评盘点','音乐教学','音乐综合']

title = 'sentiment_analysis_per_video_entertainment.csv'
csvfile = open(title, 'w')
writer = csv.writer(csvfile)
writer.writerow(['area','bv_id','positive','negative','total_words','pos_rate','neg_rate','pos/neg'])
for a in area:
    df = pandas.read_csv('reply_{}.csv'.format(a))
    df.insert(10,'word',0,allow_duplicates=False)
    df.insert(10,'pos',0,allow_duplicates=False)
    df.insert(10,'neg',0,allow_duplicates=False)
    # print(df.head())

    print(df.shape[0])
    for i,row in df.iterrows():
        senti = Sentiment()
        res = senti.sentiment_count(row['message'])
        # print(res)
        df.loc[i,'pos'] = res['pos']
        df.loc[i,'neg'] = res['neg']
        df.loc[i,'word'] = res['words']
        # if row['pos'] != 0 or row['neg'] != 0
    for bv in list(df['bv_id'].unique()):
        pos_num = df.loc[(df['bv_id'] == bv),'pos'].sum()
        neg_num = df.loc[(df['bv_id'] == bv),'neg'].sum()
        word_num = df.loc[(df['bv_id'] == bv),'word'].sum()
        print("In video {}区,{}, positive words rate is {}%, negative words rate is {}%, pos/neg is {}.".format(a,bv,round(pos_num/word_num*100,2),round(neg_num/word_num*100,2),round(pos_num/neg_num,2)))
        print("the number of positive words is {}, the number of negative words is {}, number of total words are {}.".format(pos_num,neg_num,word_num))
        print("______________________________")
        writer.writerow([a,bv,pos_num,neg_num,word_num,round(pos_num/word_num*100,2),round(neg_num/word_num*100,2),round(pos_num/neg_num,2)])
csvfile.close()






