Data Crawler of Bilibili
=========================

Author: Casters (118010022 Tonglei Chen)


This is a document for data_crawler.py. Thousands of Proxy IP is needed, because of the anti-crawling mechanism of Bilibili. Tecent Cloud Server is used to accelerate process.

# Main Funcitons

## get_hot_list(num)

This is a function to get Top (number) video in 16 Areas. Output is hot_video.csv.

num is a interger.

sample usage: 

`get_hot_list(10)`

get Top10 video in 16 Areas. 


## get_list()

This is a function to get Top 100 video in subareas of Life or Entertainment. 

To change the subarea, change line 301 cate_id_list.

Output is hot_video_life_entertainment.csv. Name can be changed in line 295.

## get_reply_top()

This is a function to get the reply of video in subareas of Life/Movie/Entertainment/Music/Game. 

To change the subarea, change line 386 cate_id_list.

Output is reply_{name of subarea}.csv.


## add_user_info()

This is a function to get the sentiment of message and the detailed condition of the user. (In area of Entertainment.)

reply_{name of subarea}.csv should be put under the same file. 

Output is user_{name of subarea}.csv. 

To change the subarea, change line 99 area.




