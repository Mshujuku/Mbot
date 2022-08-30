# -*- coding: utf-8 -*-
# CreaetDate: 2022/8/17
# UpdateDate: 2022/8/28
# Author: M叔
# version: '0.0.2'
import sqlite3
import re
import os
import shutil
import time
import itchat
from itchat.content import *
from apscheduler.schedulers.background import BackgroundScheduler

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

    conn = sqlite3.connect('/app/Db/db.sqlite3')
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
        conn = sqlite3.connect('/app/Db/db.sqlite3')
        curs = conn.cursor()
        cursor = curs.execute("SELECT title, mshuyunpan FROM Idb_idb WHERE title LIKE"+ "'%" + title + "%'")
        for t in cursor:
            msgt=''.join(t) # 元组转字符串
            time.sleep(2)
            itchat.send_msg(msgt, msg['FromUserName'])

        curs.close()
        conn.close()


    if u'熊猫' in msg['Content']:
        itchat.send_msg( "二货熊猫天天催更！", msg['FromUserName'])

    if u'荣日' in msg['Content']:
        itchat.send_msg( "能容能日，男女通吃！", msg['FromUserName'])

if __name__ == '__main__':
    # if not os.path.exists(rev_tmp_dir): 
    #     os.mkdir(rev_tmp_dir)
    itchat.auto_login(enableCmdQR=2,hotReload=True)
    itchat.send("文件助手你好哦", toUserName="filehelper")
    itchat.run()