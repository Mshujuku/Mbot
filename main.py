import itchat
from itchat.content import *

@itchat.msg_register(itchat.content.TEXT)
def handle_friend_msg(msg):
    pass
    

@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def handle_group_msg(msg):
    if u'熊猫' in msg['Content']:
        itchat.send_msg( "二货熊猫天天催更！", msg['FromUserName'])

if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2,hotReload=True)
    itchat.send("文件助手你好哦", toUserName="filehelper")
    itchat.run()