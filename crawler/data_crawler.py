# import numpy as np
import requests
import json
import time
import os
import csv
import random
from tqdm import tqdm
import pandas
from cnsenti import Sentiment

def get_ip():
    api_url = "url_to_get_proxy_IP"
    try:
        api_res = requests.get(api_url).json()['data']['proxy_list']
    except Exception:
        api_res = requests.get(api_url).text.split("\r\n")
    print(api_res)
    proxy = random.choice(api_res)
    return proxy
proxy = get_ip()

def get_info(url):
    global proxy
    page_url = url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
        username = "1301948431"
        password = "i9azoxuy"

        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password, 'proxy': proxy},
            "https": "https://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password, 'proxy': proxy}
        }



        response = requests.get(url=page_url, timeout=10,headers=headers,proxies=proxies)
        return response.text
    except:
        proxy = get_ip()
        print('产生异常',url)
        return get_info(url)


def get_json(url):
    global proxy
    page_url = url
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
        username = "1301948431"
        password = "i9azoxuy"

        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password, 'proxy': proxy},
            "https": "https://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password, 'proxy': proxy}
        }


        r = requests.get(url, timeout=10,headers=headers,proxies=proxies)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        s = r.content
        s.decode('utf-8')
        return json.loads(s)
    except:
        proxy = get_ip()
        print('产生异常',url)
        return get_json(url)





def get_user(mid):
    user_data =  {}
    info_url = "http://api.bilibili.com/x/web-interface/card?mid={}".format(mid)
    info_data = get_json(info_url)
    data = info_data['data']
    user_data['fans'] = data['card']['fans']
    user_data['follow'] = data['card']['attention']
    user_data['like_num'] = data['like_num']
    

    info_url_2 = "https://api.bilibili.com/x/space/navnum?mid={}".format(mid)
    info_data_2 = get_json(info_url_2)
    data_2 = info_data_2['data']
    user_data['bangumi'] = data_2['bangumi']
    user_data['cinema'] = data_2['cinema']
    user_data['upload_video'] = data['video']
    return user_data

def add_user_info():
    area = ['综艺','明星综合','粉丝创作','娱乐杂谈']
    for a in area:
        df = pandas.read_csv('reply_{}.csv'.format(a))
        df.insert(10,'fans',0,allow_duplicates=False)
        df.insert(10,'follow',0,allow_duplicates=False)
        df.insert(10,'like_num',0,allow_duplicates=False)
        df.insert(10,'bangumi',0,allow_duplicates=False)
        df.insert(10,'cinema',0,allow_duplicates=False)
        df.insert(10,'upload_video',0,allow_duplicates=False)
        df.insert(10,'word',0,allow_duplicates=False)
        df.insert(10,'pos',0,allow_duplicates=False)
        df.insert(10,'neg',0,allow_duplicates=False)
        df.insert(10,'pos_score',0,allow_duplicates=False)
        df.insert(10,'neg_score',0,allow_duplicates=False)
        for i,row in df.iterrows():
            senti = Sentiment()
            res = senti.sentiment_count(row['message'])
            df.loc[i,'pos'] = res['pos']
            df.loc[i,'neg'] = res['neg']
            df.loc[i,'word'] = res['words']
            res2 = senti.sentiment_calculate(row['message'])
            df.loc[i,'pos_score'] = res2['pos']
            df.loc[i,'neg_score'] = res2['neg']
            info = get_user(row['uid'])
            df.loc[i,'fans'] = info['fans']
            df.loc[i,'follow'] = info['follow']
            df.loc[i,'like_num'] = info['like_num']
            df.loc[i,'bangumi'] = info['bangumi']
            df.loc[i,'cinema'] = info['cinema']
            df.loc[i,'upload_video'] = info['upload_video']
        df.to_csv('user_{}.csv'.format(a))
        







def get_av(bv):
    bv_url = "https://api.bilibili.com/x/web-interface/view?bvid="+bv
    
    bv_data = get_json(bv_url)
    reply_num = bv_data['data']['stat']['reply']
    oid = bv_data['data'].get('aid')
    title = bv_data['data']['title']
    return oid,reply_num,title


def ctime_time(ctime):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(ctime))

def output_csv(title,column_name,content):
    csvfile = open(title, 'w')
    writer = csv.writer(csvfile)
    writer.writerow(column_name)
    writer.writerows(content)
    csvfile.close()


def get_reply(bv,writer):
    output_data = []
    av,reply_num,title = get_av(bv)
    if reply_num%20 == 0:
        pages = reply_num//20
    else:
        pages = reply_num//20+1
    for page in tqdm(range(1,pages)):
        video_api = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={}&type=1&oid={}&sort=2'.format(page,av)
        # info = get_info(video_api)
        response = get_json(video_api)
        if response['data']['replies']:
            for i in response['data']['replies']:
                data_line = []
                data_line.append(bv)
                data_line.append(title)
                data_line.append(i['content']['message'])
                data_line.append(ctime_time(i['ctime']))
                data_line.append(i['like'])
                data_line.append(i['mid'])
                data_line.append(i['member']['uname'])
                data_line.append(i['member']['sex'])
                data_line.append(i['member']['level_info']['current_level'])
                data_line.append(i['member']['vip']['label']['text'])
                # print(i['mid'])
                # data_line.append(get_user(i['mid']))

                writer.writerow(data_line)
    return output_data


def get_all_reply(hot_list):
    
    for key in hot_list.keys():
        for bv in hot_list[key]:
            csvfile = open('reply_'+ key + bv + '.csv', 'w')
            writer = csv.writer(csvfile)
            column_name = ['bv_id','title','message','time','like','uid','name','sex','level','vip']
            writer.writerow(column_name)
            get_reply(bv,writer)
            csvfile.close()





def get_author(uid):
    info_url = "https://api.bilibili.com/x/relation/stat?vmid={}".format(uid)
    
    info_data = get_json(info_url)
    author_data = info_data['data']
    return author_data['follower']

def get_hot_list(num):
    hot_list = {}
    hot_code = [168,1,3,129,4,36,188,234,223,160,211,217,119,155,5,181]
    # hot_code = [223,5]

    hot_corr = {
        168:'国创相关',
        1:'动画',
        3:'音乐',
        129:'舞蹈',
        4:'游戏',
        36:'知识',
        188:'科技',
        234:'运动',
        223:'汽车',
        160:'生活',
        211:'美食',
        217:'动物圈',
        119:'鬼畜',
        155:'时尚',
        5:'娱乐',
        181:'影视'
    }
    output_data = []
    
    for code in hot_code:
        print(code)
        hot_url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid={}&type=all".format(code)
        response = get_info(hot_url)
        response = json.loads(response)['data']
        count = 0
        for i in response['list']:
            count += 1
            data_line = []
            if count > num:
                break
            data_line.append(hot_corr[code])
            data_line.append(i['tname'])
            data_line.append(i['bvid'])
            data_line.append(i['title'])
            data_line.append(i['duration'])
            data_line.append(i['stat']['view'])
            data_line.append(i['stat']['danmaku'])
            data_line.append(i['stat']['reply'])
            data_line.append(i['stat']['favorite'])
            data_line.append(i['stat']['coin'])
            data_line.append(i['stat']['share'])
            data_line.append(i['stat']['like'])
            data_line.append(i['owner']['mid'])
            data_line.append(i['owner']['name'])
            data_line.append(get_author(i['owner']['mid']))
            # download_pic(i['pic'],hot_corr[code],i['bvid'])
            if hot_corr[code] in hot_list:
                hot_list[hot_corr[code]].append(i['bvid'][2:])
            else:
                hot_list[hot_corr[code]] = []
                hot_list[hot_corr[code]].append(i['bvid'][2:])
            output_data.append(data_line)

    output_csv('hot_video.csv',['area','tag','bv_id','title','duration','view','danmaku','reply','favorite','coin','share', "like","author_uid","author_name","author_follower"],output_data)
    print('end')
    return hot_list



def get_list():
    csvfile = open('hot_video_top500.csv', 'w')
    writer = csv.writer(csvfile)
    column_name = ['area','tag','bv_id','time','title','duration','view','danmaku','reply','favorite','coin','share', "like","author_uid","author_name","author_follower",'width','height','landscape']
    writer.writerow(column_name)
    # url = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=scores&copy_right=-1&cate_id=239&page=1&pagesize=20&jsonp=jsonp&time_from=20220310&time_to=20220409'
    # url = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id=241&page=1&pagesize=20&jsonp=jsonp&time_from=20220409&time_to=20220416'
    cate_id_list = [241,242,137,71]
    

    # cate_id_name = {
    #     241:'娱乐杂谈',
    #     242:'粉丝创作',
    #     137:'明星综合',
    #     71:'综艺'
    # }
    cate_id_name = {
        241:'娱乐杂谈',
        242:'粉丝创作',
        137:'明星综合',
        21:'日常',
        71:'综艺',
        162:'绘画',
        161:'手工',
        138:'搞笑'
    }
    for cate in cate_id_list:
        print(cate)
        url = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id={}&page=1&pagesize=100&jsonp=jsonp&time_from=20220310&time_to=20220409'.format(cate)
        info = get_info(url=url)
        response = json.loads(info)['result']
        for i in response:
            data_line = []
            data_line.append(cate_id_name[cate])
            data_line.append(i['tag'].strip('"'))
            data_line.append(i['bvid'])
            data_line.append(i['pubdate'])

            # download_pic('http:'+i['pic'],cate_id_name[cate],i['bvid'])
            data = get_video_info(i['bvid'][2:])
            data_line += data
            writer.writerow(data_line)

    csvfile.close()
def get_video_info(bv_id):
    data_line = []
    bv_url = "https://api.bilibili.com/x/web-interface/view?bvid="+bv_id
    i = get_json(bv_url)['data']
    data_line.append(i['title'])
    data_line.append(i['duration'])
    data_line.append(i['stat']['view'])
    data_line.append(i['stat']['danmaku'])
    data_line.append(i['stat']['reply'])
    data_line.append(i['stat']['favorite'])
    data_line.append(i['stat']['coin'])
    data_line.append(i['stat']['share'])
    data_line.append(i['stat']['like'])
    data_line.append(i['owner']['mid'])
    data_line.append(i['owner']['name'])
    data_line.append(get_author(i['owner']['mid']))
    data_line.append(i['dimension']['width'])
    data_line.append(i['dimension']['height'])
    if(i['dimension']['height']>i['dimension']['width']):
        data_line.append('Y')
    else:
        data_line.append('N')
    return data_line


    
            

def get_reply_top50():
    bv_id_list = {}
    # cate_id_list = [138]
    # cate_id_name = {

    # }
    # cate_id_list = [137,71]
    

    cate_id_name = {
        241:'娱乐杂谈',
        242:'粉丝创作',
        137:'明星综合',
        71:'综艺',
        239:'家居房产',
        21:'日常',
        162:'绘画',
        161:'手工',
        138:'搞笑',
        17:'单机游戏',
        171:'电子竞技',
        172:'手机游戏',
        65:'网络游戏',
        173:'桌游棋牌',
        121:'GMV',
        136:'音游',
        19:'MUGEN'
    }

    cate_id_list = [172,173,121,136,19]
    

    # cate_id_name = {
        
    # }
    for cate in cate_id_list:
        print(cate)
        url = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id={}&page=1&pagesize=10&jsonp=jsonp&time_from=20220310&time_to=20220409'.format(cate)
        info = get_info(url=url)
        response = json.loads(info)['result']
        # count = 0
        for i in response:
            # if count < 4:
            #     count += 1
            #     continue
            
            if cate_id_name[cate] in bv_id_list:
                bv_id_list[cate_id_name[cate]].append(i['bvid'])
            else:
                bv_id_list[cate_id_name[cate]] =  []
                bv_id_list[cate_id_name[cate]].append(i['bvid'])
    get_all_reply(bv_id_list)
    

