# -*- coding: utf-8 -*-
# Date: 2022/8/25
# Author: M叔
# version: '0.0.1'

import time
import itchat
from itchat.content import *
from apscheduler.schedulers.background import BackgroundScheduler


from Mbot.utils.data_collection import (
    get_weather_info,
    get_dictum_info,
    get_diff_time,
    get_calendar_info,
    get_constellation_info
)

from Mbot.utils.group_helper import (
    handle_group_helper
)
from Mbot.utils.friend_helper import (
    handle_friend
)


'''
@itchat.msg_register([TEXT])
def text_reply(msg):
    """ 监听用户消息，用于自动回复 """
    handle_friend(msg)
'''

    # 下面这段代码，可以很直观打印出返回的消息的数据结构。
    # 把打印的数据复制到  https://www.json.cn/ 可查看详细的内容。群消息同理
    # import json
    # print(json.dumps(msg, ensure_ascii=False))


@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def text_group(msg):
    """ 监听用户消息，用于自动回复 """
    handle_group_helper(msg)

def handle_group_msg(msg):
    msg_id = msg['MsgId']
    msg_create_time = msg['CreateTime']
    msg_from_user = msg['User']['NickName']
    msg_content = msg['Content']
    msg_type = msg['Type']

    print(msg_id,msg_create_time,msg_from_user,msg_content,msg_type)
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
    if u'熊猫' in msg['Content']:
        itchat.send_msg( "二货熊猫天天催更！", msg['FromUserName'])

    if u'荣日' in msg['Content']:
        itchat.send_msg( "能容能日，男女通吃！", msg['FromUserName'])

if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2,hotReload=True)
    itchat.send("文件助手你好哦", toUserName="filehelper")
    itchat.run()