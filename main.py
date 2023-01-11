# -*- coding: utf-8 -*-
# CreaetDate: 2022/8/17
# UpdateDate: 2023/1/11
# Author: M叔
# version: '0.2'
import sqlite3
import re
import os
import shutil
import time
import itchat
from itchat.content import *
#from apscheduler.schedulers.background import BackgroundScheduler

import requests
from requests.packages import urllib3
import json
import re
import urllib.parse

#  关闭告警信息
urllib3.disable_warnings()


yan_lists = [6890802,6890793,6890783,6890771,6890751,6890732,6890718,6890711]




#    舔狗兄妹
def xiongmao():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    response = requests.get('https://api.oick.cn/dog/api.php', headers=headers, verify=False)
    data = response.text    
    return data


#    猴哥短视频美女
def houge():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    response = requests.get('https://ml.v3.api.aa1.cn/girl-11-02/v3.php?wpon=2', headers=headers, verify=False)
    data = response.text
    data = json.loads(response.text)
    ydz = urllib.parse.quote(data['ydz'].replace('//',''))
    return ydz


#    杨菊黄图
def yangju():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    response = requests.get('https://jiejie.uk/taotu/random.php', headers=headers, verify=False)
    data = json.loads(response.text)
    imgs = data['imgs']
    lil = []
    for img in imgs:
        lil.append(img)
    lil = ("\n".join(lil))
    return lil

#   大师兄讲哲学
def bigxiong():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    response = requests.get('https://www.btstu.cn/yan/api.php?charset=utf-8&encode=json', headers=headers, verify=False)
    data = json.loads(response.text)
    text = data['text']
    return text

#   yiso搜索阿里云盘
def yiso(m):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    response = requests.get('https://yiso.fun/api/search?name=' + m, headers=headers)
    data = json.loads(response.text)
    lists = data['data']['list']
    lil = []
    for l in lists:
        ll = l['url']
        lil.append(ll)
    lil = ("\n".join(lil))
    return lil

#   磁力黄片
def cangjingkong(m):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    response = requests.get('https://www.givemetips.com/api/es/searchv2?order=0&page=1&size=10&content=' + m, headers=headers)
    data = json.loads(response.text)
    lists = data['data']['hashInfos']
    lil = []
    for l in lists:
        ll = l['infohash']
        lil.append('magnet:?xt=urn:btih:' + ll)
    lil = ("\n".join(lil))
    return lil


#   茶杯狐在线
def cupfox(m):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    
    response = requests.get('https://cupfox.app/s/'+m, headers=headers)
    html = response.text
    re_urls = re.findall(r'"url":"https://.*?"',html)
    lil = []
    for xin_urls in re_urls:
        lil.append(xin_urls.replace('"url":','').replace('"',''))
    lil = ("\n".join(lil))
    return lil





from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
PARENT_DIR = BASE_DIR.parent
DB_DIR = str(PARENT_DIR) + '/' + 'Db'


# {msg_id:(msg_from,msg_to,msg_time,msg_time_rec,msg_type,msg_content,msg_share_url)}
msg_dict = {}

# 文件临时存储页
# rec_tmp_dir = os.path.join(os.getcwd(), 'tmp/')

# 表情有一个问题 | 接受信息和接受note的msg_id不一致 巧合解决方案
face_bug = None

'''
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handle_friend(msg):
    msg_id = msg['MsgId']
    msg_from_user = msg['User']['NickName']
    msg_content = msg['Content']
    msg_create_time = msg['CreateTime']
    msg_type = msg['Type']
    print("收到信息: ", msg_id, msg_from_user, msg_content, msg_create_time,msg_type)
'''



@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def handle_group_msg(msg):
    # 获取本能地时间戳 e: 2022-08-27 21:30:08
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg_id = msg['MsgId']
    msg_group_name = msg['User']['NickName']
    msg_from_user = msg['ActualNickName']
    msg_content = msg['Content']
    msg_create_time = msg['CreateTime']
    msg_type = msg['Type']
    #msg_text = msg['Text']
    #print("群聊信息: ",msg_id, msg_time_rec, msg_group_name , msg_from_user, msg_content, msg_create_time, msg_type)
    msg_list = (msg_id, msg_time_rec, msg_group_name , msg_from_user, msg_content, msg_create_time, msg_type)
    print(msg_list)

    conn = sqlite3.connect('../Db/db.sqlite3')
    curs = conn.cursor()
    curs.execute("INSERT INTO MbotDb_mbotdb (msg_id, msg_time_rec, msg_group_name , msg_from_user, msg_content, msg_create_time, msg_type) VALUES (?, ?, ?, ?, ?, ?, ?);", msg_list)
    conn.commit()
    curs.close()
    conn.close()

    '''
    #print(msg)
        rec_msg_dict.update({
        msg_id: {
            'msg_from_user': msg_from_user,
            'msg_time_rec': msg_time_rec,
            'msg_create_time': msg_create_time,
            'msg_type': msg_type,
            'msg_content': msg_content
        }
    })
    '''
    #curs.execute("INSERT INTO Idb (title, country, genre, summary, episode, end, subgroup, subgroup_from, subgroup_download, mshuyunpan) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    if u'$' in msg['Content']:
        title = msg['Content'][1:]
        conn = sqlite3.connect('../Db/db.sqlite3')
        curs = conn.cursor()
        cursor = curs.execute("SELECT title, mshuyunpan FROM Idb_idb WHERE title LIKE"+ "'%" + title + "%'")
        for t in cursor:
            msgt=''.join(t) # 元组转字符串
            time.sleep(2)
            itchat.send_msg(msgt, msg['FromUserName'])

        curs.close()
        conn.close()
    

    if u'熊猫' in msg['Content']:
        time.sleep(1)
        mxiongmao = xiongmao()
        itchat.send_msg( "《熊猫日记》" + '\n' + mxiongmao, msg['FromUserName'])

    if u'荣日' in msg['Content']:
        itchat.send_msg( "能容能日，男女通吃！", msg['FromUserName'])

    if u'猴' in msg['Content']:
        time.sleep(1)
        mhouge = houge()
        itchat.send_msg( "浴皇大帝猴哥推荐" + '\n' + mhouge, msg['FromUserName'])
        
        
    if u'杨菊' in msg['Content']:
        time.sleep(1)
        itchat.send_msg( "杨菊姐姐最爱的色图来了！测试版2023.1.11"+ '\n' , msg['FromUserName'])
        itchat.send_msg( "本地图用来测试不是网络图每次刷新一样！熊猫请勿沉迷！"+ '\n' , msg['FromUserName'])
        #myangju = yangju() 
        for yan in yan_lists:
            time.sleep(1)
            itchat.send_file('/data/data/com.termux/files/home/mshujuku/Images/'+str(yan)+'.jpg', msg['FromUserName'])


        
#         for yan in yan_lists:
#             time.sleep(1)
#             itchat.send_img('../Images/'+ str(yan) + '.jpg', msg['FromUserName'])

    if u'大师兄' in msg['Content']:
        time.sleep(1)
        mbigxiong = bigxiong()
        itchat.send_msg( "著名哲学家尼古拉斯大师兄如是说：" + mbigxiong, msg['FromUserName'])

    if u'#' in msg['Content']:
        title = msg['Content'][1:]
        time.sleep(3)
        myiso = yiso(m=title)
        mcupfox = cupfox(m=title)
        itchat.send_msg(title + '阿里云盘地址' + '\n' + myiso, msg['FromUserName'])
        itchat.send_msg(title + '在线观看地址' + '\n' + mcupfox, msg['FromUserName'])

    if u'!' in msg['Content']:
        title = msg['Content'][1:]
        time.sleep(3)
        mcangjingkong = cangjingkong(m=title)
        itchat.send_msg(title + '是熊猫小哥的最爱送给你'+ '\n' + mcangjingkong, msg['FromUserName'])


if __name__ == '__main__':
    # if not os.path.exists(rev_tmp_dir): 
    #     os.mkdir(rev_tmp_dir)
    itchat.auto_login(enableCmdQR=2,hotReload=True)
    itchat.send("文件助手你好哦", toUserName="filehelper")
    itchat.run()
